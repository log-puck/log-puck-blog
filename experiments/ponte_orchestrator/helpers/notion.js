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
  
  const lastId = sessions.results[0].properties.ID.unique_id.number;
  return lastId + 1;
}

/**
 * Salva i risultati della WAW Council in Notion
 * @param {Object} data - Dati da salvare (context, results, votes, newIdeas)
 * @returns {Promise<Object>} Sessione creata in Notion
 */
async function saveToNotion(data) {
  const { context, results, votes, newIdeas } = data;
  
  // STEP 1: Crea Session
  const session = await notion.pages.create({
    parent: { database_id: config.WAW_COUNCIL_DB_ID },
    properties: {
      'Name': {
        title: [{ text: { content: `AI Council Session #${await getNextSessionNumber()}` }}]
      },
      'Date': {
        date: { start: new Date().toISOString().split('T')[0] }
      },
      'Raw JSON': {
        rich_text: [{ text: { content: JSON.stringify({ context, results, votes, newIdeas }, null, 2) } }]
      },
      'AI Participants': {
        multi_select: results.map(r => ({ name: r.name }))
      },
      'Build Status': {
        select: { name: 'Done' }
      },
      'Winner Score': {
        number: votes[0]?.score || 0
      },
      'Winner Idea': {
        rich_text: [{ text: { content: votes[0]?.idea || 'N/A' } }]
      }
    }
  });
  
  // STEP 2: Per ogni idea votata
  for (const vote of votes) {
    // Find or create idea
    const idea = await findOrCreateIdea(vote.idea);
    
    // Crea voto per ogni AI che l'ha votata
    for (const aiVote of vote.votes) {
      await notion.pages.create({
        parent: { database_id: config.WAW_VOTES_DB_ID },
        properties: {
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
          'WAW_IDEAS': {
            relation: [{ id: idea.id }]
          }
        }
      });
    }
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
