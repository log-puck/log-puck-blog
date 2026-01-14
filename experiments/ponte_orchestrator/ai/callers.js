/**
 * AI Callers: Funzioni per chiamare le diverse AI
 */

const { genAI, openai, grokClient, perplexityClient, deepseekClient, anthropic, GLM_API_KEY, GLM_BASE_URL } = require('../api/clients');
const axios = require('axios');

/**
 * Chiama Google Gemini
 * @param {string} prompt - Prompt da inviare
 * @returns {Promise<string>} Risposta dell'AI
 */
async function callGemini(prompt) {
  try {
    if (!process.env.GOOGLE_AI_API_KEY) {
      throw new Error('GOOGLE_AI_API_KEY not found in environment');
    }
    
    const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });
    const result = await model.generateContent(prompt);
    const response = await result.response;
    return response.text();
  } catch (error) {
    console.error('Gemini error:', error.message);
    throw new Error(`Gemini failed: ${error.message}`);
  }
}

/**
 * Chiama OpenAI ChatGPT
 * @param {string} prompt - Prompt da inviare
 * @returns {Promise<string>} Risposta dell'AI
 */
async function callChatGPT(prompt) {
  try {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    return completion.choices[0].message.content;
  } catch (error) {
    console.error('ChatGPT error:', error.message);
    throw new Error(`ChatGPT failed: ${error.message}`);
  }
}

/**
 * Chiama xAI Grok
 * @param {string} prompt - Prompt da inviare
 * @returns {Promise<string>} Risposta dell'AI
 */
async function callGrok(prompt) {
  try {
    const completion = await grokClient.chat.completions.create({
      model: 'grok-4',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    return completion.choices[0].message.content;
  } catch (error) {
    console.error('Grok error:', error.message);
    throw new Error(`Grok failed: ${error.message}`);
  }
}

/**
 * Chiama Perplexity
 * @param {string} prompt - Prompt da inviare
 * @returns {Promise<string>} Risposta dell'AI
 */
async function callPerplexity(prompt) {
  try {
    const completion = await perplexityClient.chat.completions.create({
      model: 'sonar',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    return completion.choices[0].message.content;
  } catch (error) {
    console.error('Perplexity error:', error.message);
    throw new Error(`Perplexity failed: ${error.message}`);
  }
}

/**
 * Chiama Anthropic Claude
 * @param {string} prompt - Prompt da inviare
 * @returns {Promise<string>} Risposta dell'AI
 */
async function callClaude(prompt) {
  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1000,
      messages: [{ role: 'user', content: prompt }]
    });
    return message.content[0].text;
  } catch (error) {
    console.error('Claude error:', error.message);
    throw new Error(`Claude failed: ${error.message}`);
  }
}

/**
 * Chiama GLM (base)
 * @param {string} prompt - Prompt da inviare
 * @returns {Promise<string>} Risposta dell'AI
 */
async function callGLM(prompt) {
  try {
    const response = await axios.post(GLM_BASE_URL, {
      model: 'glm-4-plus',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    }, {
      headers: {
        'Authorization': `Bearer ${GLM_API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 30000
    });
    
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('GLM error:', error.response?.data || error.message);
    throw new Error(`GLM failed: ${error.response?.data?.error?.message || error.message}`);
  }
}

/**
 * Chiama GLM con Web Search
 * @param {string} query - Query da cercare
 * @returns {Promise<string>} Risposta dell'AI
 */
async function callGLMWithSearch(query) {
  try {
    console.log(`🔍 GLM con Web Search: "${query}"`);
    
    const response = await axios.post(GLM_BASE_URL, {
      model: 'glm-4-plus',
      messages: [
        { 
          role: 'user', 
          content: query 
        }
      ],
      tools: [{
        type: 'web_search',
        web_search: {
          enable: true
        }
      }],
      max_tokens: 2000
    }, {
      headers: {
        'Authorization': `Bearer ${GLM_API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });
    
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('GLM Search error:', error.response?.data || error.message);
    throw new Error(`GLM Search failed: ${error.response?.data?.error?.message || error.message}`);
  }
}

/**
 * Chiama DeepSeek
 * @param {string} prompt - Prompt da inviare
 * @returns {Promise<string>} Risposta dell'AI
 */
async function callDeepSeek(prompt) {
  try {
    const completion = await deepseekClient.chat.completions.create({
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 1000
    });
    const response = completion.choices[0].message.content;
    console.log('🔍 DeepSeek RAW response:', response);
    return response;
  } catch (error) {
    console.error('DeepSeek error:', error.message);
    throw new Error(`DeepSeek failed: ${error.message}`);
  }
}

module.exports = {
  callGemini,
  callChatGPT,
  callGrok,
  callPerplexity,
  callClaude,
  callGLM,
  callGLMWithSearch,
  callDeepSeek
};
