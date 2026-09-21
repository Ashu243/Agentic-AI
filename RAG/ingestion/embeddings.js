require("dotenv").config();
const { GoogleGenAI } = require("@google/genai");

const ai = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY
});


// Create Embeddings
async function createEmbedding(texts) {
    const response = await ai.models.embedContent({
        model: "gemini-embedding-001",
        contents: texts,
        config: {
            outputDimensionality: 1536
        }
    });
    return response.embeddings.map(embedding => embedding.values);
}

module.exports = createEmbedding