require("dotenv").config();

const { GoogleGenAI } = require("@google/genai");

const ai = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY,
});

let user_query = "what's the weather of Gurugram?"

let tools = {
    getNews,
    getWeather
}

async function main() {
    // const conversations = []
    

    const weatherFunctionDeclaration = {
        type: 'function',
        name: 'getWeather',
        description: 'Gets the current temperature for a given location.',
        parameters: {
            type: 'object',
            properties: {
                location: {
                    type: 'string',
                    description: 'The city name, e.g. Delhi',
                },
            },
            required: ['location'],
        },
    };

    // conversations.push({
    //     role: 'user',
    //     content: user_query
    // })

    const interaction = await ai.interactions.create({
        model: "gemini-3.6-flash",
        input: `${user_query}`,
//         system_instruction: `
// You have access to this tool:

// getWeather(city)
// getNews()

// If you need the tool, respond ONLY in this format:

// TOOL: getWeather
// ARGS: {"city":"Delhi"}

// If you don't need a tool, answer the user normally.
//             `,
        tools: [weatherFunctionDeclaration]
    });


    const fcStep = interaction.steps.find(s => s.type === 'function_call');
    console.log(fcStep);

    let result;
    if (fcStep.name === 'getWeather') {
        result = getWeather(fcStep.arguments);
        console.log(`Function execution result: ${JSON.stringify(result)}`);
    }

    const finalInteraction = await ai.interactions.create({
        model: 'gemini-3.6-flash',
        input: [{
            type: 'function_result',
            name: fcStep.name,
            call_id: fcStep.id,
            result: [{ type: 'text', text: JSON.stringify(result) }]
        }],
        tools: [weatherFunctionDeclaration],
        previous_interaction_id: interaction.id,
    });

    console.log(finalInteraction.output_text);


    // conversations.push({
    //     role: 'assistant',
    //     content: output
    // })

    // conversations.push({
    //     role: 'tool',
    //     name: toolName,
    //     content: result
    // })

    // console.log("conversations",conversations)
}


function getWeather(args) {
    const city = args.location;

    if (city === 'Gurugram') {
        return '28 degree with some winds';
    }

    return `The weather of ${city} is 34 degree with high humidity`;
}

function getNews() {
    return `
    🇮🇳 BRICS Summit: PM Modi calls for greater global cooperation to tackle geopolitical tensions and supply-chain disruptions.
🤖 AI Safety Debate: Sam Altman, Elon Musk and Anthropic CEO Dario Amodei back calls for stronger safeguards around advanced AI development.
🇺🇸 Trump on AI: Donald Trump says concerns about AI risks are exaggerated and stresses the importance of U.S. leadership in AI.
🏏 India vs Afghanistan: India is playing Afghanistan in the first T20I in New Delhi on September 13.
🏆 Women's Asia Cup: India Women face Sri Lanka Women in the 2026 Asia Cup final in Dubai.
🎾 US Open: Kazakhstan's Elena Rybakina wins her first US Open women's singles title and reaches world No. 1.
💻 PwC India: PwC plans a major restructuring combining parts of its Indian and U.S. operations, creating a roughly 40,000-employee unit.
🌊 Bihar Floods: More than 48 lakh people are reportedly affected by severe flooding across Bihar.
🦭 Australia: Australia's first confirmed case of bird flu in an endangered Australian sea lion has raised conservation concerns.
🌍 BRICS: China and India signal willingness to contribute to peace efforts regarding the Ukraine conflict during the BRICS summit.
    `
}

main();