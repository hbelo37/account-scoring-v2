const http = require("http");
const axios = require("axios");

const PORT = 3000;

// 👉 CHANGE this to your Render URL if different
const API_BASE = "https://account-scoring-v2.onrender.com";

const server = http.createServer(async (req, res) => {
  if (req.method === "POST" && req.url === "/mcp") {
    let body = "";

    req.on("data", chunk => {
      body += chunk.toString();
    });

    req.on("end", async () => {
      try {
        const mcpRequest = JSON.parse(body);

        // Expecting: { company: "stripe.com" }
        const company = mcpRequest.company;

        if (!company) {
          res.writeHead(400);
          return res.end(JSON.stringify({ error: "company field missing" }));
        }

        // Call your scoring API
        const response = await axios.post(`${API_BASE}/score`, {
          companies: [company]
        });

        const result = response.data.results[0];

        res.writeHead(200, { "Content-Type": "application/json" });
        reend(JSON.stringify({
          score: result.score,
          tier: result.tier,
          enriched: result.enriched
        }));

      } catch (err) {
        res.writeHead(500);
        res.end(JSON.stringify({ error: err.message }));
      }
    });

  } else {
    res.writeHead(404);
    res.end();
  }
});

server.listen(PORT, () => {
  console.log(`MCP server running on http://localhost:${PORT}/mcp`);
});
