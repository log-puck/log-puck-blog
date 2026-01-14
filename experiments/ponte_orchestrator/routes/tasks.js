/**
 * Route: Tasks
 */

const { notion } = require('../api/clients');
const { config } = require('../api/clients');

function registerTasksRoute(app) {
  app.get('/api/tasks', async (req, res) => {
    try {
      console.log('📖 Fetching tasks from Notion...');
      
      const DB_TASKS_ID = config.DB_TASKS_ID;
      if (!DB_TASKS_ID) {
        throw new Error('DB_TASKS_ID not configured');
      }
      
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
}

module.exports = { registerTasksRoute };
