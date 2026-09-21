const pool = require("../db/db");
const createEmbedding = require("../ingestion/localEmbeddings");




async function searchChunks(query, top_k, threshold = 0.6) {
    const queryEmbedding = await createEmbedding([query]);

    const result = await pool.query(
        `
        SELECT
            id,
            text,
            source,
            page,
            section,
            1 - (embedding <=> $1::vector) AS score 
        FROM documents_local
        WHERE 1 - (embedding <=> $1::vector) >= $2
        ORDER BY embedding <=> $1::vector
        LIMIT $3
        `,
        [
            `[${queryEmbedding.join(",")}]`,
            threshold,
            top_k
        ]
        // $1::vector means that treat $1 as a vector
    );

    return result.rows;
}


module.exports = searchChunks