// ============================================
// PONTE ORCHESTRATOR MULTI-AI v1.1
// Log_Puck Project - Anker2 + WAW Council
// CDC: Struttura emerge quando serve
// ============================================

require('dotenv').config({ path: '../.env' });
const express = require('express');
const { Client } = require('@notionhq/client');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const Anthropic = require('@anthropic-ai/sdk');
const path = require('path');
const axios = require('axios');
const config = require('./ponte_config');

const app = express();
const PORT = 3000;

// ============================================
// SETUP API CLIENTS
// ============================================

const notion = new Client({ auth: process.env.NOTION_API_KEY });
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_AI_API_KEY);
const OpenAI = require('openai');
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});
// xAI (Grok) - usa stesso SDK OpenAI con base URL diverso
const grokClient = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1'
})
// Perplexity - usa formato OpenAI-compatible
const perplexityClient = new OpenAI({
  apiKey: process.env.PERPLEXITY_API_KEY,
  baseURL: 'https://api.perplexity.ai'
});
// DeepSeek - usa formato OpenAI-compatible
const deepseekClient = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: 'https://api.deepseek.com'
});
// Anthropic Claude
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});
// GLM client (custom con axios)
const GLM_API_KEY = process.env.GLM_API_KEY;
const GLM_BASE_URL = config.GLM_BASE_URL;

// Database IDs da config
const DB_TEMPLATES_ID = config.DB_TEMPLATES_ID;
const DB_TASKS_ID = config.DB_TASKS_ID;

// Middleware
app.use(express.json());
app.use(express.static('public')); // Serve index.html da cartella public

// ============================================
// ROUTE: GET TASKS FROM NOTION
// ============================================

// GET templates disponibili
app.get('/api/templates', async (req, res) => {
  try {
    console.log('📋 Fetching templates from Notion...');
    
    const response = await notion.databases.query({
      database_id: DB_TEMPLATES_ID,
      filter: {
        property: 'Testato',
        checkbox: { equals: true }  // Solo template testati
      },
      sorts: [{ property: 'Nome', direction: 'ascending' }]
    });

    const templates = response.results.map(page => ({
      id: page.id,
      nome: page.properties.Nome?.title?.[0]?.plain_text || 'Senza nome',
      categoria: page.properties.Categoria?.select?.name || '',
      aiConsigliata: page.properties['AI Consigliata']?.select?.name || '',
      template: page.properties.Template?.rich_text?.[0]?.plain_text || '',
      variabili: page.properties.Variabili?.rich_text?.[0]?.plain_text || '',
      risultatoAtteso: page.properties['Risultato Atteso']?.rich_text?.[0]?.plain_text || '',
      temaFiles: page.properties.TEMA?.files || []  // Array di file
    }));

    console.log(`✅ Found ${templates.length} templates`);
    res.json(templates);

  } catch (error) {
    console.error('❌ Error fetching templates:', error.message);
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/tasks', async (req, res) => {
  try {
    console.log('📖 Fetching tasks from Notion...');
    
    const response = await notion.databases.query({
      database_id: DB_TASKS_ID,
      filter: {
        or: [
          { property: 'Status', select: { equals: 'Draft' } },
          { property: 'Status', select: { equals: 'In Progress' } }
        ]
      },
      sorts: [{ property: 'ID', direction: 'descending' }]
    });

    const tasks = response.results.map(page => ({
      id: page.id,
      taskId: page.properties.ID?.number || 0,
      title: page.properties.Titolo?.title?.[0]?.plain_text || 'Senza titolo',
      status: page.properties.Status?.select?.name || 'Draft'
    }));

    console.log(`✅ Found ${tasks.length} tasks`);
    res.json(tasks);

  } catch (error) {
    console.error('❌ Error fetching tasks:', error.message);
    res.status(500).json({ error: error.message });
  }
});



// ============================================
// ROUTE: SUBMIT TO AI
// ============================================

app.post('/api/submit-to-ai', async (req, res) => {
  try {
    const { taskId, aiName, instructions } = req.body;

    console.log('\n🎯 NEW REQUEST');
    console.log(`Task: ${taskId}`);
    console.log(`AI: ${aiName}`);
    console.log(`Instructions: ${instructions.substring(0, 100)}...`);

    // Get AI response
    let aiResponse;
    
    switch(aiName) {
      case 'Gemini':
  			aiResponse = await callGemini(instructions);
  			break;
  		case 'Claude':
  			aiResponse = await callClaude(instructions);
  			break;
      case 'ChatGPT':
  			aiResponse = await callChatGPT(instructions);
  			break;     
  		case 'Grok':
  			aiResponse = await callGrok(instructions);
  			break;      
  		case 'GLM':
  			aiResponse = await callGLM(instructions);
  			break;
  		case 'GLM-Search':
  			aiResponse = await callGLMWithSearch(instructions);
  			break;
      case 'Perplexity':
  			aiResponse = await callPerplexity(instructions);
 	 			break;      
      case 'Copilot':
        aiResponse = '⏸️ Copilot integration coming soon';
        break;
      case 'GitHub-Copilot':
        aiResponse = '⏸️ GitHub-Copilot integration coming soon';
        break;
      case 'Notion':
        aiResponse = '⏸️ Notion AI integration coming soon';
        break;
      default:
        throw new Error(`AI ${aiName} not recognized`);
    }

    console.log(`✅ ${aiName} responded (${aiResponse.length} chars)`);

    // Return response for APPROVAL
    res.json({
      success: true,
      aiName,
      response: aiResponse,
      taskId,
      message: '⚠️ APPROVAL REQUIRED - Response ready for Puck review'
    });

  } catch (error) {
    console.error('❌ Error in submit-to-ai:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// ============================================
// ROUTE: WRITE TO NOTION (POST-APPROVAL)
// ============================================

app.post('/api/write-to-notion', async (req, res) => {
  try {
    const { taskId, aiName, content } = req.body;

    console.log('\n✍️ WRITING TO NOTION (APPROVED)');
    console.log(`Task: ${taskId}`);
    console.log(`AI Column: ${aiName}`);

    // Find page by task ID
    const queryResponse = await notion.databases.query({
      database_id: DB_TASKS_ID,
      filter: {
        property: 'ID',
        number: { equals: parseInt(taskId) }
      }
    });

    if (queryResponse.results.length === 0) {
      throw new Error(`Task ID ${taskId} not found`);
    }

    const pageId = queryResponse.results[0].id;

    // Write to AI column
    await notion.pages.update({
      page_id: pageId,
      properties: {
        [aiName]: {
          rich_text: [{
            text: { content: content.substring(0, 2000) } // Notion limit
          }]
        },
        Status: {
          select: { name: 'In Progress' }
        }
      }
    });

    console.log('✅ Written to Notion successfully');
    res.json({ success: true, message: `${aiName} content saved to Notion` });

  } catch (error) {
    console.error('❌ Error writing to Notion:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// ============================================
// ROUTE: WAW COUNCIL (NEW!)
// ============================================
// SPIEGAZIONE: Questa route riceve context + ideas dal form HTML,
// chiama le AI selezionate in PARALLELO, aggrega i voti,
// e ritorna risultati già pronti per display

app.post('/api/waw-council', async (req, res) => {
  try {
    const { context, ideas, selectedAIs } = req.body;

    console.log('\n🎯 WAW COUNCIL REQUEST');
    console.log(`Ideas to vote: ${ideas.length}`);
    console.log(`AIs selected: ${Object.keys(selectedAIs).filter(k => selectedAIs[k]).join(', ')}`);

    // SPIEGAZIONE: Questo prompt viene mandato a TUTTE le AI selezionate
    // Chiediamo: 1) vota top 3, 2) proponi idea nuova
    const prompt = `You are participating in LOG_PUCK - a human-AI collaborative blog experiment.

PROJECT CONTEXT:
- Name: ${context.projectName}
- Tech Stack: ${context.techStack}
- Current Focus: ${context.currentFocus}
- Completed: ${context.completed}

PENDING IDEAS:
${ideas.filter(i => i.trim()).map((idea, i) => `${i + 1}. ${idea}`).join('\n')}

YOUR TASK:
1. Vote: Rank your TOP 3 ideas by priority (1=highest, 2=medium, 3=lower)
2. Propose: Suggest ONE new improvement idea

FORMAT YOUR RESPONSE AS JSON:
{
  "vote": {
    "priority_1": "exact idea title from list",
    "priority_2": "exact idea title from list",
    "priority_3": "exact idea title from list",
    "reasoning": "brief explanation of your ranking"
  },
  "new_idea": {
    "title": "short descriptive title",
    "description": "what it does (1-2 sentences)",
    "effort": "Low/Medium/High",
    "impact": "Low/Medium/High"
  }
}

IMPORTANT: Return ONLY valid JSON, no markdown formatting.`;

    // SPIEGAZIONE: Array di Promise per chiamate PARALLELE
    // Promise.all() fa partire tutte insieme, aspetta che finiscano tutte
    const apiCalls = [];

    if (selectedAIs.claude) {
      apiCalls.push(
        callClaude(prompt)
          .then(text => {
            // Estrae JSON dalla risposta (potrebbe avere testo extra)
            const jsonMatch = text.match(/\{[\s\S]*\}/);
            return {
              id: 'claude',
              name: 'Claude',
              data: jsonMatch ? JSON.parse(jsonMatch[0]) : null
            };
          })
          .catch(err => ({ 
            id: 'claude', 
            name: 'Claude', 
            error: err.message 
          }))
      );
    }

    if (selectedAIs.glm) {
      apiCalls.push(
        callGLM(prompt)
          .then(text => {
            const jsonMatch = text.match(/\{[\s\S]*\}/);
            return {
              id: 'glm',
              name: 'GLM',
              data: jsonMatch ? JSON.parse(jsonMatch[0]) : null
            };
          })
          .catch(err => ({ 
            id: 'glm', 
            name: 'GLM', 
            error: err.message 
          }))
      );
    }

    if (selectedAIs.grok) {
      apiCalls.push(
        callGrok(prompt)
          .then(text => {
            const jsonMatch = text.match(/\{[\s\S]*\}/);
            return {
              id: 'grok',
              name: 'Grok',
              data: jsonMatch ? JSON.parse(jsonMatch[0]) : null
            };
          })
          .catch(err => ({ 
            id: 'grok', 
            name: 'Grok', 
            error: err.message 
          }))
      );
    }

    if (selectedAIs.gemini) {
      apiCalls.push(
        callGemini(prompt)
          .then(text => {
            const jsonMatch = text.match(/\{[\s\S]*\}/);
            return {
              id: 'gemini',
              name: 'Gemini',
              data: jsonMatch ? JSON.parse(jsonMatch[0]) : null
            };
          })
          .catch(err => ({ 
            id: 'gemini', 
            name: 'Gemini', 
            error: err.message 
          }))
      );
    }

    if (selectedAIs.chatgpt) {
      apiCalls.push(
        callChatGPT(prompt)
          .then(text => {
            const jsonMatch = text.match(/\{[\s\S]*\}/);
            return {
              id: 'chatgpt',
              name: 'ChatGPT',
              data: jsonMatch ? JSON.parse(jsonMatch[0]) : null
            };
          })
          .catch(err => ({ 
            id: 'chatgpt', 
            name: 'ChatGPT', 
            error: err.message 
          }))
      );
    }

    if (selectedAIs.perplexity) {
      apiCalls.push(
        callPerplexity(prompt)
          .then(text => {
            const jsonMatch = text.match(/\{[\s\S]*\}/);
            return {
              id: 'perplexity',
              name: 'Perplexity',
              data: jsonMatch ? JSON.parse(jsonMatch[0]) : null
            };
          })
          .catch(err => ({ 
            id: 'perplexity', 
            name: 'Perplexity', 
            error: err.message 
          }))
      );
    }

    if (selectedAIs.deepseek) {
      apiCalls.push(
        callDeepSeek(prompt)
          .then(text => {
            const jsonMatch = text.match(/\{[\s\S]*\}/);
            return {
              id: 'deepseek',
              name: 'DeepSeek-V3',
              data: jsonMatch ? JSON.parse(jsonMatch[0]) : null
            };
          })
          .catch(err => ({ 
            id: 'deepseek', 
            name: 'DeepSeek-V3', 
            error: err.message 
          }))
      );
    }

    // SPIEGAZIONE: Aspetta che TUTTE le chiamate finiscano
    const allResults = await Promise.all(apiCalls);
    console.log(`✅ Received ${allResults.length} responses`);

    // SPIEGAZIONE: Aggregazione voti
    // priority_1 = 3 punti, priority_2 = 2 punti, priority_3 = 1 punto
    const voteScores = {};
    const validResults = allResults.filter(r => r.data && !r.error);

    validResults.forEach(result => {
      const vote = result.data.vote;
      if (vote) {
        [vote.priority_1, vote.priority_2, vote.priority_3].forEach((idea, index) => {
          const points = [3, 2, 1][index];
          if (idea) {
            voteScores[idea] = (voteScores[idea] || 0) + points;
          }
        });
      }
    });

    // SPIEGAZIONE: Ordina idee per punteggio (più alto = più votata)
    const sortedVotes = Object.entries(voteScores)
      .sort(([, a], [, b]) => b - a)
      .map(([idea, score]) => ({
        idea,
        score,
        votes: validResults.map(r => ({
          ai: r.name,
          rank: [r.data.vote.priority_1, r.data.vote.priority_2, r.data.vote.priority_3].indexOf(idea) + 1,
          reasoning: r.data.vote.reasoning
        })).filter(v => v.rank > 0)
      }));

    console.log('✅ WAW Council completed');
    console.log(`🥇 Winner: ${sortedVotes[0]?.idea} (${sortedVotes[0]?.score} points)`);

    // ✨ NEW: Prepara nuove idee per Notion e response
    const newIdeas = validResults.map(r => ({
      ai: r.name,
      ...r.data.new_idea
    }));

    // ✨ NEW: SALVA IN NOTION
    try {
      await saveToNotion({
        context: req.body.context,
        ideas: req.body.ideas,
        selectedAIs,
        results: allResults,
        votes: sortedVotes,
        newIdeas
      });
      
      console.log('✅ Saved to Notion successfully');
    } catch (notionError) {
      console.error('⚠️ Notion save failed:', notionError.message);
      // Non blocca response - i dati sono comunque ritornati
    }

    // SPIEGAZIONE: Ritorna tutto al frontend per display
    res.json({
      success: true,
      raw: allResults,                    // Risposte grezze (per debug)
      votes: sortedVotes,                 // Classifica votazioni
      newIdeas                            // Nuove idee proposte
    });

  } catch (error) {
    console.error('❌ Error in WAW Council:', error.message);
    res.status(500).json({ error: error.message });
  }
});

// ============================================
// AI FUNCTIONS
// ============================================

async function callGemini(prompt) {
  try {
    // Verifica presenza API key (senza esporre caratteri)
    if (!process.env.GOOGLE_AI_API_KEY) {
      throw new Error('GOOGLE_AI_API_KEY not found in environment');
    }
    
    const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });
    const result = await model.generateContent(prompt);
    const response = await result.response;
    return response.text();
  } catch (error) {
    console.error('Gemini error:', error.message);
    throw new Error(`Gemini failed: ${error.message}`);
  }
}

async function callChatGPT(prompt) {
  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    return completion.choices[0].message.content;
  } catch (error) {
    console.error('ChatGPT error:', error.message);
    throw new Error(`ChatGPT failed: ${error.message}`);
  }
}

async function callGrok(prompt) {
  try {
    const completion = await grokClient.chat.completions.create({
      model: 'grok-4',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    return completion.choices[0].message.content;
  } catch (error) {
    console.error('Grok error:', error.message);
    throw new Error(`Grok failed: ${error.message}`);
  }
}

async function callPerplexity(prompt) {
  try {
    const completion = await perplexityClient.chat.completions.create({
      model: 'sonar',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    return completion.choices[0].message.content;
  } catch (error) {
    console.error('Perplexity error:', error.message);
    throw new Error(`Perplexity failed: ${error.message}`);
  }
}

async function callClaude(prompt) {
  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1000,
      messages: [{ role: 'user', content: prompt }]
    });
    return message.content[0].text;
  } catch (error) {
    console.error('Claude error:', error.message);
    throw new Error(`Claude failed: ${error.message}`);
  }
}

// SPIEGAZIONE: Funzione GLM base (era mancante nel file originale!)
async function callGLM(prompt) {
  try {
    const response = await axios.post(GLM_BASE_URL, {
      model: 'glm-4-plus',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    }, {
      headers: {
        'Authorization': `Bearer ${GLM_API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 30000
    });
    
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('GLM error:', error.response?.data || error.message);
    throw new Error(`GLM failed: ${error.response?.data?.error?.message || error.message}`);
  }
}

// SPIEGAZIONE: GLM con Web Search (versione con strumenti)
async function callGLMWithSearch(query) {
  try {
    console.log(`🔍 GLM con Web Search: "${query}"`);
    
    const response = await axios.post(GLM_BASE_URL, {
      model: 'glm-4-plus',
      messages: [
        { 
          role: 'user', 
          content: query 
        }
      ],
      tools: [{
        type: 'web_search',
        web_search: {
          enable: true
        }
      }],
      max_tokens: 2000
    }, {
      headers: {
        'Authorization': `Bearer ${GLM_API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });
    
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('GLM Search error:', error.response?.data || error.message);
    throw new Error(`GLM Search failed: ${error.response?.data?.error?.message || error.message}`);
  }
}

async function callDeepSeek(prompt) {
  try {
    const completion = await deepseekClient.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    return completion.choices[0].message.content;
  } catch (error) {

    console.error('DeepSeek error:', error.message);
    throw new Error(`DeepSeek failed: ${error.message}`);
  }
}

// ============================================
// SAVE WAW RESULTS TO NOTION
// ============================================

async function saveToNotion(data) {
  const { context, results, votes, newIdeas } = data;
  
  // STEP 1: Crea Session
  const session = await notion.pages.create({
    parent: { database_id: config.WAW_SESSIONS_DB_ID },
    properties: {
      'Title': {
        title: [{ text: { content: `AI Council Session #${await getNextSessionNumber()}` }}]
      },
      'Date': {
        date: { start: new Date().toISOString().split('T')[0] }
      },
      'Context': {
        rich_text: [{ text: { content: JSON.stringify(context, null, 2) }}]
      },
      'AI Participants': {
        multi_select: results.map(r => ({ name: r.name }))
      },
      'Session Status': {
        select: { name: 'Ready for CONTENT' }
      },
      'Winner Score': {
        number: votes[0]?.score || 0
      },
      'Winner Idea': {
        rich_text: [{ text: { content: votes[0]?.idea || 'N/A' }}]
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
          'Voters': {
            select: [{ name: aiVote.ai }]
          },
          'Score': {
            number: [3, 2, 1][aiVote.rank - 1] // rank 1=3pt, 2=2pt, 3=1pt
          },
          'Rank': {
            number: aiVote.rank
          },
          'Resoning': {
            rich_text: [{ text: { content: aiVote.reasoning }}]
          },
          'WAW_IDEAS': {
            relation: [{ id: idea.id }]
          },
          'WAW_SESSIONS': {
            relation: [{ id: session.id }]
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
        'Title': {
          title: [{ text: { content: newIdea.title }}]
        },
        'Description': {
          rich_text: [{ text: { content: newIdea.description }}]
        },
        'Proposed By': {
          multi_select: [{ name: newIdea.ai }]
        },
        'Effort': {
          select: { name: newIdea.effort }
        },
        'Impact': {
          select: { name: newIdea.impact }
        },
        'Status': {
          select: { name: 'Proposed' }
        }
      }
    });
  }
  
  return session;
}

// Helper: Find or create idea
async function findOrCreateIdea(ideaTitle) {
  // Query existing ideas
  const existing = await notion.databases.query({
    database_id: config.WAW_IDEAS_DB_ID,
    filter: {
      property: 'Title',
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
      'Title': {
        title: [{ text: { content: ideaTitle }}]
      },
      'Status': {
        select: { name: 'In Progress' }
      }
    }
  });
}

  // Helper: Get next session number
  async function getNextSessionNumber() {
    const sessions = await notion.databases.query({
      database_id: config.WAW_SESSIONS_DB_ID,
      sorts: [{ property: 'ID', direction: 'descending' }],
      page_size: 1
    });
    
    if (sessions.results.length === 0) return 1;
    
    const lastId = sessions.results[0].properties.ID.unique_id.number;
    return lastId + 1;
  }

// ============================================
// START SERVER
// ============================================

app.listen(PORT, () => {
  console.log('\n🚀 PONTE ORCHESTRATOR MULTI-AI v1.1');
  console.log('========================================');
  console.log(`Server running on http://localhost:${PORT}`);
  console.log('\n✅ Ready for CDC chaos!');
  console.log('🎯 WAW Council: ACTIVE');
  console.log('Hayden > NOI > IO > bugghino 🎺\n');
});