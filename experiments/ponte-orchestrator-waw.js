/**
 * PONTE ORCHESTRATOR MULTI-AI v1.1
 * Log_Puck Project - Anker2 + WAW Council
 * CDC: Struttura emerge quando serve
 * 
 * Entry point minimale - Usa architettura modulare
 */

require('dotenv').config({ path: '../.env' });
const { start } = require('./ponte_orchestrator/orchestrator');

if (require.main === module) {
  start();
}

module.exports = { start };
