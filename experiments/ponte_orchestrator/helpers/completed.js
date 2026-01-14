/**
 * Completed Helper: Auto-load recent completed work from Notion
 */

const { notion } = require('../api/clients');
const { config } = require('../api/clients');

/**
 * Carica gli ultimi task completati da Done-List
 * @param {number} limit - Numero di task da caricare (default: 10)
 * @returns {Promise<string>} Stringa formattata con i task completati
 */
async function getRecentCompleted(limit = 10) {
  try {
    const DONE_LIST_DB_ID = config.DONE_LIST_ID || '2df6f0146d11805aab91c54ff167028d';
    
    console.log(`📋 Loading last ${limit} completed tasks from Done-List...`);
    
    const response = await notion.databases.query({
      database_id: DONE_LIST_DB_ID,
      sorts: [{ property: 'Created time', direction: 'descending' }],
      page_size: limit
    });
    
    const completed = response.results.map(page => {
      const name = page.properties.Name?.title?.[0]?.text?.content || 'Untitled';
      const desc = page.properties.Descrizione?.rich_text?.[0]?.text?.content || '';
      const date = page.properties['Created time']?.created_time || '';
      const dateStr = date ? new Date(date).toLocaleDateString('it-IT') : '';
      
      return desc ? `- ${name} (${dateStr}): ${desc}` : `- ${name} (${dateStr})`;
    });
    
    console.log(`✅ Loaded ${completed.length} completed tasks`);
    return completed.join('\n');
    
  } catch (error) {
    console.error('⚠️ Could not auto-load Done-List:', error.message);
    return '[Unable to load recent work - using manual context]';
  }
}

module.exports = {
  getRecentCompleted
};
