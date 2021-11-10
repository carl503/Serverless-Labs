const mysql = require('mysql')
const express = require('express')
const app = express()
const port = process.env.PORT || 8080

const connection = mysql.createConnection({
    host: process.env.DB_HOST || "localhost",
    port: process.env.DB_PORT || "3306",
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
app.get("/", (_req, res) => {
    res.sendFile("/app/form.html")
});

app.get("/movies", (_req, res) => {
    connection.connect()

    connection.query('SELECT * from movies', function (error, results, _fields) {
        if (error) throw error;
        res.send(results)
    });
       
    connection.end();
})

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`)
})