const express = require("express");
const axios = require("axios");

const app = express();
app.use(express.json());

const API = "https://account-scoring-v2.onrender.com/score";

app.post("/mcp", async (req, res) => {
  try {
    const { companies, customers } = req.body;

    if (!customers || customers.length === 0) {
      return res.status(400).json({
        error: "Provide customer examples to define ICP."
      });
    }

    const response = await axios.post(API, {
      companies,
      customers
    });

    res.status(200).json(response.data);

  } catch (e) {
    res.status(500).json({
      error: e.message,
      details: e.response?.data
    });
  }
});

app.listen(3000, () => {
  console.log("MCP running on http://localhost:3000/mcp");
});