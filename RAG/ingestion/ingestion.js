
const fs = require("fs");

const { PDFParse } = require('pdf-parse');
const chunkText = require("./chunker");

const pool = require("../db/db");
const createEmbedding = require("./localEmbeddings");


async function insertChunk(chunk) {
    await pool.query(
        `
        INSERT INTO documents_local
            (text, source, page, section, embedding)
        VALUES
            ($1, $2, $3, $4, $5)
        `,
        [
            chunk.text,
            chunk.metadata.source,
            chunk.metadata.page,
            chunk.metadata.section,
            `[${chunk.embeddings.join(",")}]`
        ]
    );
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
    try {
        const pdfBuffer = fs.readFileSync("./documents/sampleforRAG.pdf");

        const parser = new PDFParse({
            data: pdfBuffer
        });

        const result = await parser.getText();

        const chunks = chunkText(result.text)
        const uniqueChunks = new Set(chunks)

        console.log(`total lenght: ${chunks.length}`)
        console.log(`unique chunks: ${uniqueChunks.size}`)

        let start = 0;
        const size = 50;

        while (start < chunks.length) {
            const end = start + size;

            const batchChunks = chunks.slice(start, end);

            console.log(
                `Processing chunks ${start} → ${Math.min(end, chunks.length) - 1}`
            );

            const results = await createEmbedding(batchChunks);

            console.log(`Received ${results.length} embeddings`);

            for (let i = 0; i < results.length; i++) {
                const ans = {
                    text: batchChunks[i],
                    metadata: {
                        source: 'sampleforRAG.pdf',
                        page: 1,
                        section: null
                    },
                    embeddings: results[i]
                };

                await insertChunk(ans);
            }

            start += size;
            console.log('inserted chunks in pg: ', batchChunks.length)
        }

    } catch (error) {
        console.log(error)
    }
}

main()