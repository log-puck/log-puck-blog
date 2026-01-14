/**
 * Route: Ideas
 */

const { notion } = require('../api/clients');
const { config } = require('../api/clients');

function registerIdeasRoute(app) {
  app.get('/api/notion-ideas', async (req, res) => {
    try {
      console.log('💡 Fetching ideas from Notion (Include in Next Vote)...');
      
      const response = await notion.databases.query({
        database_id: config.WAW_IDEAS_DB_ID,
        filter: {
          property: 'Include in Next Vote', // Checkbox field
          checkbox: {
            equals: true
          }
        },
        sorts: [
          {
            property: 'Total Score',
            direction: 'descending'
          }
        ]
      });

      const ideas = response.results.map(page => {
        const titleProp = page.properties.Title || page.properties.Name;
        const titleContent = titleProp?.title || titleProp?.rich_text || [];
        return titleContent[0]?.text?.content || 'Untitled';
      });

      console.log(`✅ Found ${ideas.length} ideas marked for next vote`);
      res.json({ 
        success: true, 
        ideas,
        count: ideas.length 
      });

    } catch (error) {
      console.error('❌ Error fetching ideas from Notion:', error.message);
      res.status(500).json({ 
        success: false, 
        error: error.message 
      });
    }
  });
}

module.exports = { registerIdeasRoute };
