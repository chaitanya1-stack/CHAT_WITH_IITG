const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const path = require('path');


dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());


const chatbotRoute = require('./routes/chatBot');
app.use('/api/chatbotexpress', chatbotRoute);


const PORT = process.env.PORT2 || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Express server running on port ${PORT}`);
});
