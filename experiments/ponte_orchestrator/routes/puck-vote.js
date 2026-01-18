/**
 * Route: Puck Vote
 * Salva voto di Puck su Notion (parallelo a Council AI)
 */

const { notion, config } = require('../api/clients');

function registerPuckVoteRoute(app) {
  app.post('/api/puck-vote', async (req, res) => {
    try {
      const { context, ideas, vote } = req.body;

      console.log('\n🎺 PUCK VOTE - Starting...');
      console.log(`Ideas pool: ${ideas.length}`);
      console.log(`Puck votes: ${vote.rank1}, ${vote.rank2}, ${vote.rank3}`);

      // Get next session number
      const sessionNumber = await getNextSessionNumber();
      const sessionDate = new Date().toISOString().split('T')[0];

      // STEP 1: Create WAW_SESSION (In Progress)
      console.log(`\n📋 Creating Council Session #${sessionNumber}...`);
      
      const councilPage = await notion.pages.create({
        parent: { database_id: config.WAW_COUNCIL_DB_ID },
        properties: {
          'Name': {
            title: [{ text: { content: `AI Council Session #${sessionNumber}` } }]
          },
          'Date': {
            date: { start: sessionDate }
          },
          'Raw JSON': {
            rich_text: [{ 
              text: { 
                content: JSON.stringify({ puckVote: vote, context, ideas }, null, 2).substring(0, 2000)
              } 
            }]
          },
          'AI Participants': {
            multi_select: [{ name: 'Puck (Human)' }]
          },
          'Build Status': {
            status: { name: 'In Progress' }
          },
          'Context': {
            rich_text: [{ 
              text: { content: typeof context === 'string' ? context : JSON.stringify(context) } 
            }]
          }
        }
      });

      const sessionId = councilPage.id;
      console.log(`✅ Session created: ${councilPage.url}`);

      // STEP 2: Create 3 VOTES for Puck
      console.log(`\n🗳️ Creating Puck's 3 votes...`);
      
      const votesData = [
        { rank: 1, idea: vote.rank1, reasoning: vote.reasoning1, score: 3 },
        { rank: 2, idea: vote.rank2, reasoning: vote.reasoning2, score: 2 },
        { rank: 3, idea: vote.rank3, reasoning: vote.reasoning3, score: 1 }
      ];

      for (const voteData of votesData) {
        try {
          await notion.pages.create({
            parent: { database_id: config.WAW_VOTES_DB_ID },
            properties: {
              'Name': {
                title: [{ text: { content: `${voteData.idea.substring(0, 50)} - Puck` } }]
              },
              'AI Voter': {
                select: { name: 'Puck (Human)' }
              },
              'Score': {
                number: voteData.score
              },
              'Rank': {
                number: voteData.rank
              },
              'Reasoning': {
                rich_text: [{ text: { content: voteData.reasoning.substring(0, 2000) } }]
              },
              'Session': {
                relation: [{ id: sessionId }]
              }
            }
          });
          console.log(`   ✓ Rank #${voteData.rank}: ${voteData.idea} (${voteData.score}pt)`);
        } catch (error) {
          console.error(`   ✗ Failed to create vote #${voteData.rank}: ${error.message}`);
        }
      }

      console.log(`✅ Puck's votes created`);

      // STEP 3: Create new idea (if provided)
      let newIdeaId = null;
      if (vote.newIdea?.title && vote.newIdea?.description) {
        console.log(`\n💡 Creating Puck's new idea...`);
        
        try {
          const newIdeaPage = await notion.pages.create({
            parent: { database_id: config.WAW_IDEAS_DB_ID },
            properties: {
              'Name': {
                title: [{ text: { content: vote.newIdea.title } }]
              },
              'Description': {
                rich_text: [{ text: { content: vote.newIdea.description } }]
              },
              'Proposed By': {
                select: { name: 'Puck (Human)' }
              },
              'Effort': {
                select: { name: vote.newIdea.effort || 'Medium' }
              },
              'Impact': {
                select: { name: vote.newIdea.impact || 'High' }
              },
              'Ideas Status': {
                select: { name: 'Proposed' }
              }
            }
          });
          
          newIdeaId = newIdeaPage.id;
          console.log(`✅ New idea created: ${vote.newIdea.title}`);
        } catch (error) {
          console.error(`✗ Failed to create new idea: ${error.message}`);
        }
      }

      // Summary
      console.log(`\n🎉 PUCK VOTE COMPLETED!`);
      console.log(`   Session: ${councilPage.url}`);
      console.log(`   Status: In Progress (waiting for AI votes)`);

      res.json({ 
        success: true,
        sessionId,
        sessionNumber,
        sessionUrl: councilPage.url,
        votesCreated: 3,
        newIdeaId,
        message: 'Puck vote saved! Waiting for AI Council results...'
      });

    } catch (error) {
      console.error(`\n❌ Error saving Puck vote: ${error.message}`);
      res.status(500).json({ 
        success: false, 
        error: error.message 
      });
    }
  });
}

// Helper: Get next session number
async function getNextSessionNumber() {
  try {
    const response = await notion.databases.query({
      database_id: config.WAW_COUNCIL_DB_ID,
      sorts: [{ property: 'Date', direction: 'descending' }],
      page_size: 1
    });
    
    if (response.results.length === 0) return 1;
    
    const lastTitle = response.results[0].properties.Name.title[0]?.text.content || '';
    const match = lastTitle.match(/#(\d+)/);
    return match ? parseInt(match[1]) + 1 : 1;
  } catch (error) {
    console.log('⚠️ Could not get session number, defaulting to 1');
    return 1;
  }
}

module.exports = { registerPuckVoteRoute };