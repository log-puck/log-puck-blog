/**
 * Orchestrator: Setup Express e registrazione routes
 */

const express = require('express');
const path = require('path');

// Import routes
const { registerTemplatesRoute } = require('./routes/templates');
const { registerTasksRoute } = require('./routes/tasks');
const { registerIdeasRoute } = require('./routes/ideas');
const { registerAIModelsRoute } = require('./routes/ai-models');
const { registerSubmitToAIRoute } = require('./routes/submit-to-ai');
const { registerPuckVoteRoute } = require('./routes/puck-vote');
const { registerWriteToNotionRoute } = require('./routes/write-to-notion');
const { registerWAWCouncilRoute } = require('./routes/waw-council');

const PORT = 3000;

/**
 * Crea e configura l'app Express
 * @returns {express.Application} App Express configurata
 */
function createApp() {
  const app = express();

  // Middleware
  app.use(express.json());
  app.use(express.static(path.join(__dirname, '../public'))); // Serve index.html da cartella public

  // Registra routes
  registerPuckVoteRoute(app);
  registerTemplatesRoute(app);
  registerTasksRoute(app);
  registerIdeasRoute(app);
  registerAIModelsRoute(app);
  registerSubmitToAIRoute(app);
  registerWriteToNotionRoute(app);
  registerWAWCouncilRoute(app);

  return app;
}

/**
 * Avvia il server
 */
function start() {
  const app = createApp();

  app.listen(PORT, () => {
    console.log('\n🚀 PONTE ORCHESTRATOR MULTI-AI v1.1');
    console.log('========================================');
    console.log(`Server running on http://localhost:${PORT}`);
    console.log('\n✅ Ready for CDC chaos!');
    console.log('🎯 WAW Council: ACTIVE');
    console.log('Hayden > NOI > IO > bugghino 🎺\n');
  });
}

module.exports = {
  createApp,
  start
};
