/**
 * Route: Templates
 */

const { notion } = require('../api/clients');
const { config } = require('../api/clients');

function registerTemplatesRoute(app) {
  app.get('/api/templates', async (req, res) => {
    try {
      console.log('📋 Fetching templates from Notion...');
      
      const DB_TEMPLATES_ID = config.DB_TEMPLATES_ID;
      if (!DB_TEMPLATES_ID) {
        throw new Error('DB_TEMPLATES_ID not configured');
      }
      
      const response = await notion.databases.query({
        database_id: DB_TEMPLATES_ID,
        filter: {
          property: 'Testato',
          checkbox: { equals: true }  // Solo template testati
        },
        sorts: [{ property: 'Nome', direction: 'ascending' }]
      });

      const templates = response.results.map(page => ({
        id: page.id,
        nome: page.properties.Nome?.title?.[0]?.plain_text || 'Senza nome',
        categoria: page.properties.Categoria?.select?.name || '',
        aiConsigliata: page.properties['AI Consigliata']?.select?.name || '',
        template: page.properties.Template?.rich_text?.[0]?.plain_text || '',
        variabili: page.properties.Variabili?.rich_text?.[0]?.plain_text || '',
        risultatoAtteso: page.properties['Risultato Atteso']?.rich_text?.[0]?.plain_text || '',
        temaFiles: page.properties.TEMA?.files || []  // Array di file
      }));

      console.log(`✅ Found ${templates.length} templates`);
      res.json(templates);

    } catch (error) {
      console.error('❌ Error fetching templates:', error.message);
      res.status(500).json({ error: error.message });
    }
  });
}

module.exports = { registerTemplatesRoute };
