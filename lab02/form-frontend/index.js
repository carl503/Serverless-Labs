const mysql = require('mysql')

const connection = mysql.createConnection({
    host: process.env.DB_HOST || "localhost:3306",
    user: process.env.DB_USER || "scad",
    password: process.env.DB_PASS || "scad",
    database: process.env.DB_NAME || "scad"
})

/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
exports.entrypoint = (req, res) => {
    if (req.path === "/") {
        if (req.method === "GET") {
            res.sendFile("/form.html")
        }
    }


    if (req.path === "/movies") {
        if (req.method === "GET") {

            connection.connect()

            connection.query('SELECT * from movies', function (error, results, fields) {
                if (error) throw error;
                res.send(results)
            });
               
            connection.end();
        } 
    }
};
