// ============================================
// LOAD WAW SESSION TO NOTION
// Usage: node load-waw-session.js <session-file.json>
// ============================================

require('dotenv').config({ path: '../.env' });
const { Client } = require('@notionhq/client');
const fs = require('fs');
const path = require('path');

const NOTION_TOKEN = process.env.NOTION_TOKEN || process.env.NOTION_API_KEY;
if (!NOTION_TOKEN) {
  throw new Error('Missing NOTION_TOKEN (or NOTION_API_KEY) in environment');
}

const notion = new Client({ auth: NOTION_TOKEN });

// Database IDs
const getEnvId = (key, aliases = []) => {
  for (const name of [key, ...aliases]) {
    const value = process.env[name];
    if (value) return value;
  }
  return null;
};

const WAW_COUNCIL_DB_ID = getEnvId('WAW_COUNCIL_DB_ID', ['WAW_COUNCIL_ID']);
const WAW_IDEAS_DB_ID = getEnvId('WAW_IDEAS_DB_ID', ['WAW_IDEAS_ID']);
const WAW_VOTES_DB_ID = getEnvId('WAW_VOTES_DB_ID', ['WAW_VOTES_ID']);

if (!WAW_COUNCIL_DB_ID || !WAW_IDEAS_DB_ID || !WAW_VOTES_DB_ID) {
  throw new Error('Missing WAW DB IDs in environment (.env)');
}

// ============================================
// MAIN FUNCTION
// ============================================

async function loadSession(jsonFilePath) {
  try {
    console.log(`📖 Reading session file: ${jsonFilePath}`);
    
    // Read JSON file
    const fileContent = fs.readFileSync(jsonFilePath, 'utf8');
    const sessionData = JSON.parse(fileContent);
    
    if (!sessionData.success) {
      throw new Error('Session data shows success: false');
    }
    
    console.log('✅ Session file loaded');
    console.log(`   - AI responses: ${sessionData.raw.length}`);
    console.log(`   - Voted ideas: ${sessionData.votes.length}`);
    console.log(`   - New ideas: ${sessionData.newIdeas.length}`);
    
    // Extract context from filename or use defaults
    const dateMatch = jsonFilePath.match(/(\d{4}-\d{2}-\d{2})/);
    const sessionDate = dateMatch ? dateMatch[1] : new Date().toISOString().split('T')[0];
    
    // Get session number
    const sessionNumber = await getNextSessionNumber();
    
    console.log(`\n🎯 Creating Council Session #${sessionNumber}...`);
    
    // STEP 1: Create WAW_COUNCIL record
    const councilPage = await notion.pages.create({
      parent: { database_id: WAW_COUNCIL_DB_ID },
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
              content: JSON.stringify(sessionData, null, 2).substring(0, 2000) // Notion limit
            } 
          }]
        },
        'AI Participants': {
          multi_select: sessionData.raw
            .filter(r => r.data !== null)
            .map(r => ({ name: r.name }))
        },
        'Build Status': {
          status: { name: 'Done' }
        },
        'Winner Score': {
          number: sessionData.votes[0]?.score || 0
        },
        'Winner Idea': {
          rich_text: [{ 
            text: { 
              content: sessionData.votes[0]?.idea || 'N/A' 
            } 
          }]
        },
        'Context': {
          rich_text: [{ 
            text: { 
              content: 'Session loaded from JSON file' 
            } 
          }]
        },
        'Tech Stack': {
          rich_text: [{ 
            text: { 
              content: 'GitHub, Jekyll, Notion, Node.js 20, Python' 
            } 
          }]
        }
      }
    });
    
    console.log(`✅ Council session created: ${councilPage.url}`);
    
    // STEP 2: Create new ideas on WAW_IDEAS
    console.log(`\n💡 Creating ${sessionData.newIdeas.length} new ideas...`);
    
    for (const newIdea of sessionData.newIdeas) {
      try {
        await notion.pages.create({
          parent: { database_id: WAW_IDEAS_DB_ID },
          properties: {
            'Name': {
              title: [{ text: { content: newIdea.title } }]
            },
            'Description': {
              rich_text: [{ text: { content: newIdea.description } }]
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
        console.log(`   ✓ ${newIdea.title} (by ${newIdea.ai})`);
      } catch (error) {
        console.error(`   ✗ Failed to create idea: ${newIdea.title}`);
        console.error(`     Error: ${error.message}`);
      }
    }
    
    console.log(`✅ New ideas created`);
    
    // STEP 3: (Optional) Create detailed votes on WAW_VOTES
    console.log(`\n🗳️ Creating detailed votes...`);
    
    let votesCreated = 0;
    for (const vote of sessionData.votes) {
      for (const aiVote of vote.votes) {
        try {
          await notion.pages.create({
            parent: { database_id: WAW_VOTES_DB_ID },
            properties: {
              'Name': {
                title: [{ text: { content: `${vote.idea.substring(0, 50)}... - ${aiVote.ai}` } }]
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
                rich_text: [{ text: { content: aiVote.reasoning.substring(0, 2000) } }]
              }
            }
          });
          votesCreated++;
        } catch (error) {
          console.error(`   ✗ Failed to create vote for ${aiVote.ai} on "${vote.idea}"`);
          console.error(`     Error: ${error.message}`);
        }
      }
    }
    
    console.log(`✅ ${votesCreated} votes created`);
    
    // Summary
    console.log(`\n🎉 SESSION LOADED SUCCESSFULLY!`);
    console.log(`   Council page: ${councilPage.url}`);
    console.log(`   Winner: ${sessionData.votes[0]?.idea}`);
    console.log(`   Score: ${sessionData.votes[0]?.score} points`);
    
  } catch (error) {
    console.error(`\n❌ Error loading session: ${error.message}`);
    process.exit(1);
  }
}

// ============================================
// HELPER: Get next session number
// ============================================

async function getNextSessionNumber() {
  try {
    const response = await notion.databases.query({
      database_id: WAW_COUNCIL_DB_ID,
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

// ============================================
// RUN
// ============================================

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('❌ Usage: node load-waw-session.js <session-file.json>');
  process.exit(1);
}

const sessionFile = args[0];
if (!fs.existsSync(sessionFile)) {
  console.error(`❌ File not found: ${sessionFile}`);
  process.exit(1);
}

loadSession(sessionFile);
