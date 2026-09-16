require("dotenv").config();

const { GoogleGenAI } = require("@google/genai");

const ai = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY
});

const chunks = [
    {
        id: 1,
        text: "Refunds are processed within 5 business days after approval."
    },
    {
        id: 2,
        text: "Orders are normally shipped within 2 business days."
    },
    {
        id: 3,
        text: "Users can reset their password from the account settings page."
    },
    {
        id: 4,
        text: "Customers can request a refund within 7 days of receiving their order."
    }
];

const user_query = '"When will I get my refund?"'

// Create Embeddings
async function createEmbedding(text) {
    const response = await ai.models.embedContent({
        model: "gemini-embedding-001",
        contents: text
    });

    return response.embeddings[0].values;
}

function cosineSimilarity(a, b) {
    let dotProduct = 0;
    let magnitudeA = 0;
    let magnitudeB = 0;

    for (let i = 0; i < a.length; i++) {
        dotProduct += a[i] * b[i];
        magnitudeA += a[i] * a[i];
        magnitudeB += b[i] * b[i];
    }

    return (
        dotProduct /
        (Math.sqrt(magnitudeA) * Math.sqrt(magnitudeB))
    );
}

async function search(query, top_k) {
    const user_embedding = await createEmbedding(query)
    const results = chunks.map((chunk) => {
        const score = cosineSimilarity(chunk.embeddings, user_embedding)

        return {
            ...chunk, score
        }
    })

    results.sort((a, b) => b.score - a.score)

    return results.slice(0, top_k)
}

async function main() {
    let top_k = 2
    for (const chunk of chunks) {
        chunk.embeddings = await createEmbedding(chunk.text)
        console.log(
            `Chunk ${chunk.id}:`,
            chunk.embeddings.length,
            "dimensions"
        );
    }

    const results = await search(user_query, top_k)

    console.log(`Top ${top_k} results`)

    const interaction = await ai.interactions.create({
        model: "gemini-3.6-flash",

        input: `
User Query:
${user_query}

Retrieved Context:
${JSON.stringify(results, null, 2)}
`,

        system_instruction: `
You are a helpful assistant.

Answer the user's question using the retrieved context.

Rules:
- Use the retrieved context as your source of truth.
- Do not invent information that is not present in the context.
- If the context does not contain enough information to answer the question, say that you don't have enough information.
- Give a concise and direct answer.
`
    });
    console.log(interaction.output_text);



}

main()