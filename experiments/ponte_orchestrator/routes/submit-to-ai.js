/**
 * Route: Submit to AI
 */

const { callGemini, callClaude, callChatGPT, callGrok, callGLM, callGLMWithSearch, callPerplexity } = require('../ai/callers');

function registerSubmitToAIRoute(app) {
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
}

module.exports = { registerSubmitToAIRoute };
