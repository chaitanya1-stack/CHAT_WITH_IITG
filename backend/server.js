
// server.js
const path = require('path');
const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

// Import routes
const chatbotRoute = require('./routes/chatBot');
app.use('/api/chatbotexpress', chatbotRoute);

// Start server
const PORT = process.env.PORT2 || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Express server running on port ${PORT}`);
});
