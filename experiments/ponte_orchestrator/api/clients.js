/**
 * API Clients: Setup per tutti i client API esterni
 */

const { Client } = require('@notionhq/client');
const { GoogleGenerativeAI } = require('@google/generative-ai');
const Anthropic = require('@anthropic-ai/sdk');
const OpenAI = require('openai');
const axios = require('axios');
const config = require('../../ponte_config');

// Notion Client
const notion = new Client({ auth: process.env.NOTION_API_KEY });

// Google Gemini
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_AI_API_KEY);

// OpenAI (ChatGPT)
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// xAI (Grok) - usa stesso SDK OpenAI con base URL diverso
const grokClient = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1'
});

// Perplexity - usa formato OpenAI-compatible
const perplexityClient = new OpenAI({
  apiKey: process.env.PERPLEXITY_API_KEY,
  baseURL: 'https://api.perplexity.ai'
});

// DeepSeek - usa formato OpenAI-compatible
const deepseekClient = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: 'https://api.deepseek.com'
});

// Anthropic Claude
const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

// GLM client (custom con axios)
const GLM_API_KEY = process.env.GLM_API_KEY;
const GLM_BASE_URL = config.GLM_BASE_URL;

module.exports = {
  notion,
  genAI,
  openai,
  grokClient,
  perplexityClient,
  deepseekClient,
  anthropic,
  GLM_API_KEY,
  GLM_BASE_URL,
  config
};
