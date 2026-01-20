/**
 * Route: WAW Council
 */

const { callGemini, callClaude, callChatGPT, callGrok, callGLM, callPerplexity, callDeepSeek } = require('../ai/callers');
const { saveToNotion } = require('../helpers/notion');
const { getRecentCompleted } = require('../helpers/completed');

function safeParseAIResponse(text) {
  const jsonMatch = text.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    return { data: null, error: 'No JSON object found in response' };
  }

  try {
    return { data: JSON.parse(jsonMatch[0]), error: null };
  } catch (error) {
    return { data: null, error: `Invalid JSON: ${error.message}` };
  }
}

function registerWAWCouncilRoute(app) {
  app.post('/api/waw-council', async (req, res) => {
    try {
      const { context, ideas, selectedAIs, sessionId, puckVote } = req.body;
      const aiNameMap = {
        claude: 'Claude',
        glm: 'GLM',
        grok: 'Grok',
        gemini: 'Gemini',
        chatgpt: 'ChatGPT',
        perplexity: 'Perplexity',
        deepseek: 'DeepSeek'
      };
      const requestedParticipants = Object.keys(selectedAIs || {})
        .filter((key) => selectedAIs[key])
        .map((key) => aiNameMap[key] || key);

      console.log('\n🎯 WAW COUNCIL REQUEST');
      console.log(`Ideas to vote: ${ideas.length}`);
      console.log(`AIs selected: ${requestedParticipants.join(', ')}`);

      // ✨ AUTO-LOAD COMPLETED WORK FROM DONE-LIST
      const autoCompleted = await getRecentCompleted(10);
      const finalCompleted = context.completed || autoCompleted;

      // SPIEGAZIONE: Questo prompt viene mandato a TUTTE le AI selezionate
      // Chiediamo: 1) vota top 3, 2) proponi idea nuova
      const prompt = `You are participating in LOG_PUCK - a human-AI collaborative blog experiment.

PROJECT CONTEXT:
- Name: ${context.projectName}
- Tech Stack: ${context.techStack}
- Current Focus: ${context.currentFocus}
- Completed: ${finalCompleted}
- Context: ${context.context || ''}

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
              const { data, error } = safeParseAIResponse(text);
              return {
                id: 'claude',
                name: 'Claude',
                data,
                error
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
              const { data, error } = safeParseAIResponse(text);
              return {
                id: 'glm',
                name: 'GLM',
                data,
                error
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
              const { data, error } = safeParseAIResponse(text);
              return {
                id: 'grok',
                name: 'Grok',
                data,
                error
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
              const { data, error } = safeParseAIResponse(text);
              return {
                id: 'gemini',
                name: 'Gemini',
                data,
                error
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
              const { data, error } = safeParseAIResponse(text);
              return {
                id: 'chatgpt',
                name: 'ChatGPT',
                data,
                error
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
              const { data, error } = safeParseAIResponse(text);
              return {
                id: 'perplexity',
                name: 'Perplexity',
                data,
                error
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
              const { data, error } = safeParseAIResponse(text);
              return {
                id: 'deepseek',
                name: 'DeepSeek',
                data,
                error
              };
            })
            .catch(err => ({ 
              id: 'deepseek', 
              name: 'DeepSeek', 
              error: err.message 
            }))
        );
      }

      // SPIEGAZIONE: Aspetta che TUTTE le chiamate finiscano
      const allResults = await Promise.all(apiCalls);
      console.log(`✅ Received ${allResults.length} responses`);
      const failedResults = allResults.filter(r => r.error || !r.data);
      if (failedResults.length) {
        console.warn('⚠️ Some AI responses were invalid:', failedResults.map(r => `${r.name}: ${r.error || 'no data'}`).join(' | '));
      }

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

      if (puckVote) {
        const puckRanks = [puckVote.rank1, puckVote.rank2, puckVote.rank3];
        puckRanks.forEach((idea, index) => {
          const points = [3, 2, 1][index];
          if (idea) {
            voteScores[idea] = (voteScores[idea] || 0) + points;
          }
        });
      }

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
          sessionId,
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
        failed: failedResults,             // Errori parsing/chiamata
        requestedParticipants,             // AI coinvolte (anche se fallite)
        votes: sortedVotes,                 // Classifica votazioni
        newIdeas                            // Nuove idee proposte
      });

    } catch (error) {
      console.error('❌ Error in WAW Council:', error.message);
      res.status(500).json({ error: error.message });
    }
  });
}

module.exports = { registerWAWCouncilRoute };
