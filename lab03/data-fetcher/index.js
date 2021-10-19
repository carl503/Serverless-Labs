const fetch = require("node-fetch")

const mockarooAPI = `https://my.api.mockaroo.com/users.json?key=${process.env.MOCKAROO_KEY}`

let cachedData = null

/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
exports.entrypoint = async (req, res) => {
    if (req.path === "/") {
        if (req.method === "GET") {

            if (!cachedData) {
                let resp = await fetch(mockarooAPI)
                cachedData = await resp.json()
            }
            
            res.send(cachedData)
        }
    }
};
