/**
 * Route: Write to Notion
 */

const { notion } = require('../api/clients');
const { config } = require('../api/clients');

function registerWriteToNotionRoute(app) {
  app.post('/api/write-to-notion', async (req, res) => {
    try {
      const { taskId, aiName, content } = req.body;

      console.log('\n✍️ WRITING TO NOTION (APPROVED)');
      console.log(`Task: ${taskId}`);
      console.log(`AI Column: ${aiName}`);

      const DB_TASKS_ID = config.DB_TASKS_ID;
      if (!DB_TASKS_ID) {
        throw new Error('DB_TASKS_ID not configured');
      }

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
}

module.exports = { registerWriteToNotionRoute };
