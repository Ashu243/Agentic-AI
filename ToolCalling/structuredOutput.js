require("dotenv").config();

const { GoogleGenAI } = require("@google/genai");

const ai = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY,
});

let user_query = "What happened to my payment for the order? i haven't received the confirmation email yet?"

const responseSchema = {
    type: "object",
    properties: {
        category: {
            type: "string",
            enum: ["order_issue", "payment_issue", "general"]
        },
        urgency: {
            type: "string",
            enum: ["low", "medium", "high"]
        },
        confidence: {
            type: "number"
        }
    },
    required: ["category", "urgency", "confidence"]
};

const client = new GoogleGenAI({});

async function main() {

    const interaction = await client.interactions.create({
        model: "gemini-3.6-flash",
        input: user_query,
        response_format: {
            type: 'text',
            mime_type: 'application/json',
            schema: responseSchema
        },
    });

    const result = JSON.parse(interaction.output_text)
    console.log(result);
}


main()