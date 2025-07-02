// routes/chatBot.js

const express = require('express');
const axios = require('axios');
const router = express.Router();

// ✅ Load environment variables here too (important if this file runs before server.js loads dotenv)
require('dotenv').config();

const RAG_URL = process.env.RAG_SERVER_URL;

router.post('/', async (req, res) => {
  const { query } = req.body;

  console.log("🟡 Received query:", query);
  console.log("🟢 Forwarding to RAG server:", RAG_URL);

  try {
    const response = await axios.post(RAG_URL, { query }, { timeout: 10000 });

    console.log("✅ RAG response:", response.data);
    res.json({ answer: response.data.answer }); // or just: res.json(response.data);
  } catch (error) {
    console.error("❌ Error forwarding to RAG:", error.message);
    if (error.response) {
      console.error("❌ RAG response error data:", error.response.data);
    }
    res.status(500).json({
      error: "Internal server error",
      details: error.message,
      ragError: error.response?.data || null
    });
  }
});

module.exports = router;
