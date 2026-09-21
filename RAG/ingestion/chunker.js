
function chunkText(text, chunksize=3000, overlap=300) {
    let chunks = []
    let start = 0
    // let result = {
    //     text: '',
    //     metadata: {
    //         source: 'sampleforRAG.pdf',
    //         page: 1,
    //         section: null
    //     }
    // }
    while (start < text.length){
        let end = (start + chunksize)
        let result = text.slice(start, end)

        chunks.push(result)

        start += chunksize - overlap

    }
    return chunks
}

module.exports = chunkText