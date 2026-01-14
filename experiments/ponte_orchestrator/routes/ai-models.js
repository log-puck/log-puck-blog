/**
 * Route: AI Models
 */

function registerAIModelsRoute(app) {
  app.get('/api/ai-models', async (req, res) => {
    try {
      console.log('🤖 Returning available AI Models...');
      
      // Lista delle AI disponibili basata su quelle implementate nello script
      // Queste corrispondono alle AI che possono essere chiamate tramite API
      const aiModels = [
        { id: 'claude', name: 'Claude', status: 'Active' },
        { id: 'glm', name: 'GLM', status: 'Active' },
        { id: 'grok', name: 'Grok', status: 'Active' },
        { id: 'gemini', name: 'Gemini', status: 'Active' },
        { id: 'chatgpt', name: 'ChatGPT', status: 'Active' },
        { id: 'perplexity', name: 'Perplexity', status: 'Active' },
        { id: 'deepseek', name: 'DeepSeek', status: 'Active' }
      ];

      console.log(`✅ Returning ${aiModels.length} available AI Models`);
      res.json({ 
        success: true, 
        aiModels,
        count: aiModels.length 
      });

    } catch (error) {
      console.error('❌ Error returning AI Models:', error.message);
      res.status(500).json({ 
        success: false, 
        error: error.message 
      });
    }
  });
}

module.exports = { registerAIModelsRoute };
