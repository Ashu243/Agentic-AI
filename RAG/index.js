require("dotenv").config();

const { GoogleGenAI } = require("@google/genai");
const pool = require("./db/db");
const searchChunks = require("./retrieval/search");

const ai = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY
});




// function cosineSimilarity(a, b) {
//     let dotProduct = 0;
//     let magnitudeA = 0;
//     let magnitudeB = 0;

//     for (let i = 0; i < a.length; i++) {
//         dotProduct += a[i] * b[i];
//         magnitudeA += a[i] * a[i];
//         magnitudeB += b[i] * b[i];
//     }

//     return (
//         dotProduct /
//         (Math.sqrt(magnitudeA) * Math.sqrt(magnitudeB))
//     );
// }





const user_query = `what are the methods that are in python lists?`



async function main() {
    let top_k = 5

    const results = await searchChunks(user_query, top_k, 0.6)
    console.log(results)

    console.log(`Retrieved ${results.length} relevant chunks`);

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
- At the end of your answer, mention the source and page number used.
- Keep the answer concise.
`
    });
    console.log(interaction.output_text);



}

main()