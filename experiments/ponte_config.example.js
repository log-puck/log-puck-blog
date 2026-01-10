/**
 * PONTE ORCHESTRATOR - Configurazione ESEMPIO
 * 
 * 📋 ISTRUZIONI:
 * 1. Copia questo file come ponte_config.js
 * 2. Sostituisci i valori placeholder con i tuoi Database IDs reali
 * 3. Il file ponte_config.js è già in .gitignore e NON verrà committato
 * 
 * ⚠️ NON COMMITTARE ponte_config.js (contiene dati sensibili)
 */

module.exports = {
  // Notion Database IDs
  // Sostituisci con i tuoi Database IDs reali
  DB_TEMPLATES_ID: process.env.NOTION_DB_TEMPLATES_ID || 'YOUR_DB_TEMPLATES_ID_HERE',
  DB_TASKS_ID: process.env.NOTION_DB_TASKS_ID || 'YOUR_DB_TASKS_ID_HERE',
  
  // GLM API Configuration
  GLM_BASE_URL: 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
};

