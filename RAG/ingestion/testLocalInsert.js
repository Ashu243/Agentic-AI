const pool = require("../db/db");
const createEmbedding = require("./localEmbeddings");




async function main() {
    try {
        const chunks = [
            "Python lists are ordered and mutable collections.",
            "A list can contain multiple values of different data types.",
            "You can add elements to a Python list using the append method."
        ];

        for (const text of chunks) {
            const embedding = await createEmbedding(text);

            await pool.query(
                `
                INSERT INTO documents_local
                    (text, source, page, section, embedding)
                VALUES
                    ($1, $2, $3, $4, $5)
                `,
                [
                    text,
                    "test",
                    1,
                    null,
                    `[${embedding.join(",")}]`
                ]
            );

            console.log("Inserted:", text);
        }

        console.log("Done");
    } catch (error) {
        console.log(error);
    } finally {
        await pool.end();
    }
}

main();