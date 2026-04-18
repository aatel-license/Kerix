const express = require("express");
const axios = require("axios");
const { JSDOM } = require("jsdom");
const { Readability } = require("@mozilla/readability");

const app = express();
app.use(express.json());

app.post("/extract", async (req, res) => {
  try {
    const { url } = req.body;

    const response = await axios.get(url, { timeout: 10000 });
    const dom = new JSDOM(response.data, { url });

    const reader = new Readability(dom.window.document);
    const article = reader.parse();

    if (!article || !article.textContent) {
      return res.status(400).json({ error: "No content extracted" });
    }

    res.json({
      title: article.title,
      text: article.textContent
    });

  } catch (err) {
    res.status(500).json({ error: err.toString() });
  }
});

app.listen(3001, () => console.log("Readability service on http://localhost:3001/extract"));