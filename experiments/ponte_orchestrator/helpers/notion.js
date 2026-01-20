/**
 * Notion Helpers: Funzioni helper per operazioni Notion
 */

const { notion } = require('../api/clients');
const { config } = require('../api/clients');

/**
 * Trova o crea un'idea nel database WAW_IDEAS
 * @param {string} ideaTitle - Titolo dell'idea
 * @returns {Promise<Object>} Pagina Notion dell'idea
 */
async function findOrCreateIdea(ideaTitle) {
  // Query existing ideas
  const existing = await notion.databases.query({
    database_id: config.WAW_IDEAS_DB_ID,
    filter: {
      property: 'Name',
      title: { equals: ideaTitle }
    }
  });
  
  if (existing.results.length > 0) {
    return existing.results[0];
  }
  
  // Create new
  return await notion.pages.create({
    parent: { database_id: config.WAW_IDEAS_DB_ID },
    properties: {
      'Name': {
        title: [{ text: { content: ideaTitle }}]
      },
      'Ideas Status': {
        select: { name: 'In Progress' }
      }
    }
  });
}

/**
 * Ottiene il prossimo numero di sessione
 * @returns {Promise<number>} Numero della prossima sessione
 */
async function getNextSessionNumber() {
  const sessions = await notion.databases.query({
    database_id: config.WAW_COUNCIL_DB_ID,
    sorts: [{ property: 'ID', direction: 'descending' }],
    page_size: 1
  });

  if (sessions.results.length === 0) return 1;

  const session = sessions.results[0];
  const uniqueId = session?.properties?.ID?.unique_id?.number;
  if (typeof uniqueId === 'number') return uniqueId + 1;

  const title = session?.properties?.Name?.title?.[0]?.text?.content || '';
  const match = title.match(/#(\d+)/);
  return match ? parseInt(match[1], 10) + 1 : 1;
}

const WAW_VOTES_RELATION_PROP = 'WAW_VOTES';

async function appendVotesToIdeaRelation(ideaId, voteIds) {
  if (!voteIds.length) return;

  const ideaPage = await notion.pages.retrieve({ page_id: ideaId });
  const relationProp = ideaPage?.properties?.[WAW_VOTES_RELATION_PROP];

  if (!relationProp || relationProp.type !== 'relation') {
    console.warn(`⚠️ Relation property "${WAW_VOTES_RELATION_PROP}" not found on WAW_IDEAS`);
    return;
  }

  const existing = (relationProp.relation || []).map((rel) => rel.id);
  const merged = Array.from(new Set([...existing, ...voteIds])).map((id) => ({ id }));

  await notion.pages.update({
    page_id: ideaId,
    properties: {
      [WAW_VOTES_RELATION_PROP]: { relation: merged }
    }
  });
}

/**
 * Salva i risultati della WAW Council in Notion
 * @param {Object} data - Dati da salvare (context, results, votes, newIdeas)
 * @returns {Promise<Object>} Sessione creata in Notion
 */
async function saveToNotion(data) {
  const { sessionId, context, results, votes, newIdeas } = data;
  const contextObject = context && typeof context === 'object' && !Array.isArray(context) ? context : null;
  
  let session;

  if (sessionId) {
    const updateProperties = {
      'Winner Score': {
        number: votes[0]?.score || 0
      },
      'Winner Idea': {
        rich_text: [{ text: { content: votes[0]?.idea || 'N/A' } }]
      },
      'AI Participants': {
        multi_select: results.map(r => ({ name: r.name }))
      }
    };
    if (contextObject?.techStack) {
      updateProperties['Tech Stack'] = {
        rich_text: [{ text: { content: contextObject.techStack.substring(0, 1999) } }]
      };
    }

    session = await notion.pages.update({
      page_id: sessionId,
      properties: updateProperties
    });
    console.log(`📝 Updating existing session: ${sessionId}`);
  } else {
    // STEP 1: Crea Session
    const sessionProperties = {
      'Name': {
        title: [{ text: { content: `AI Council Session #${await getNextSessionNumber()}` }}]
      },
      'Date': {
        date: { start: new Date().toISOString().split('T')[0] }
      },
      'Raw JSON': {
        rich_text: [{ text: { content: JSON.stringify({ context, results, votes, newIdeas }, null, 2).substring(0, 1999) } }]
      },
      'AI Participants': {
        multi_select: results.map(r => ({ name: r.name }))
      },
      'Winner Score': {
        number: votes[0]?.score || 0
      },
      'Winner Idea': {
        rich_text: [{ text: { content: votes[0]?.idea || 'N/A' } }]
      }
    };

    if (contextObject?.currentFocus) {
      sessionProperties['Current Focus'] = {
        rich_text: [{ text: { content: contextObject.currentFocus.substring(0, 1999) } }]
      };
    }

    if (contextObject?.completed) {
      sessionProperties['Ideas Completed'] = {
        rich_text: [{ text: { content: contextObject.completed.substring(0, 1999) } }]
      };
    }
    if (contextObject?.techStack) {
      sessionProperties['Tech Stack'] = {
        rich_text: [{ text: { content: contextObject.techStack.substring(0, 1999) } }]
      };
    }

    session = await notion.pages.create({
      parent: { database_id: config.WAW_COUNCIL_DB_ID },
      properties: sessionProperties
    });
  }
  
  const ideaVotesMap = new Map();

  // Add full JSON as code blocks
try {
  const fullJson = { context, results, votes, newIdeas };
  const jsonString = JSON.stringify(fullJson, null, 2);
  const maxBlockSize = 1999;
  const jsonChunks = [];
  
  for (let i = 0; i < jsonString.length; i += maxBlockSize) {
    jsonChunks.push(jsonString.substring(i, i + maxBlockSize));
  }

  const blocks = [
    {
      object: 'block',
      type: 'heading_2',
      heading_2: {
        rich_text: [{
          type: 'text',
          text: { content: '📊 Full Council Data' }
        }]
      }
    }
  ];

  jsonChunks.forEach((chunk) => {
    blocks.push({
      object: 'block',
      type: 'code',
      code: {
        language: 'json',
        rich_text: [{
          type: 'text',
          text: { content: chunk }
        }]
      }
    });
  });

  await notion.blocks.children.append({
    block_id: session.id,
    children: blocks
  });
} catch (uploadError) {
  console.error(`⚠️ Failed to save full JSON: ${uploadError.message}`);
}

  // STEP 2: Per ogni idea votata
  for (const vote of votes) {
    // Find or create idea
    const idea = await findOrCreateIdea(vote.idea);
    
    // Crea voto per ogni AI che l'ha votata
    for (const aiVote of vote.votes) {
      const voteProperties = {
        'Name': {
          title: [{ text: { content: `${vote.idea} - ${aiVote.ai}` }}]
        },
        'AI Voter': {
          select: { name: aiVote.ai }
        },
        'Score': {
          number: [3, 2, 1][aiVote.rank - 1] // rank 1=3pt, 2=2pt, 3=1pt
        },
        'Rank': {
          number: aiVote.rank
        },
        'Reasoning': {
          rich_text: [{ text: { content: aiVote.reasoning }}]
        },
        'Session': {
          relation: [{ id: session.id }]
        }
      };

      const votePage = await notion.pages.create({
        parent: { database_id: config.WAW_VOTES_DB_ID },
        properties: voteProperties
      });

      const existing = ideaVotesMap.get(idea.id) || [];
      existing.push(votePage.id);
      ideaVotesMap.set(idea.id, existing);
    }
  }

  for (const [ideaId, voteIds] of ideaVotesMap.entries()) {
    await appendVotesToIdeaRelation(ideaId, voteIds);
  }
  
  // STEP 3: Per ogni nuova idea
  for (const newIdea of newIdeas) {
    await notion.pages.create({
      parent: { database_id: config.WAW_IDEAS_DB_ID },
      properties: {
        'Name': {
          title: [{ text: { content: newIdea.title }}]
        },
        'Description': {
          rich_text: [{ text: { content: newIdea.description }}]
        },
        'Proposed By': {
          select: { name: newIdea.ai }
        },
        'Effort': {
          select: { name: newIdea.effort }
        },
        'Impact': {
          select: { name: newIdea.impact }
        },
        'Ideas Status': {
          select: { name: 'Proposed' }
        }
      }
    });
  }
  
  return session;
}

module.exports = {
  saveToNotion,
  findOrCreateIdea,
  getNextSessionNumber
};
