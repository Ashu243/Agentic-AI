const { PDFParse } = require('pdf-parse');
const chunkText = require("./chunker");


async function textExtractor(pdfBuffer) {


    const parser = new PDFParse({
        data: pdfBuffer
    });

    const info = await parser.getInfo();

    console.log(`Total pages: ${info.total}`);

    const pageChunks = [];

    for (let page = 1; page <= info.total; page++) {
        const result = await parser.getText({
            partial: [page]
        });

        const chunks = chunkText(result.text);

        chunks.forEach(chunk => {
            pageChunks.push({
                text: chunk,
                metadata: {
                    source: "sampleforRAG.pdf",
                    page: page,
                    section: null
                }
            });
        });
    }
    console.log(`Total chunks: ${pageChunks.length}`);

    return pageChunks
}

module.exports = textExtractor