const { pipeline } = require("@huggingface/transformers");

let extractor;

async function loadModel() {
    if (!extractor) {
        console.log("Loading BGE embedding model...");

        extractor = await pipeline(
            "feature-extraction",
            "Xenova/bge-small-en-v1.5"
        );

        console.log("Model loaded");
    }

    return extractor;
}

async function createEmbedding(texts) {
    const model = await loadModel();

    const output = await model(texts, {
        pooling: "mean",
        normalize: true
    });

    
    return Array.from(output.tolist());
}


async function main() {
    // const result = await createEmbedding('python list are mutable')
    
}

main()

module.exports = createEmbedding;