import express from "express"
import cors from "cors"
import { MongoClient } from "mongodb"

const app = express()
const url = process.env.MONGO_URL
const client = new MongoClient(url)
const database = client.db("scad-movy")
const COLLECTION = "data"
const coll = database.collection(COLLECTION)
const movementPercentage = process.env.MOVEMENT_PERCENTAGE || 1 - 0.15

async function setup() {
  await client.connect()

  if (!await database.listCollections({name: COLLECTION}).hasNext()) {
    await database.createCollection(COLLECTION)
  }
}

setup()

app.use(express.json())
app.use(cors())

const port = process.env.PORT || 8080

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.post("/data", async (req, res) => {
  const data = req.body
  await client.connect()

  if (data?.mac && data?.rssi && data?.timestamp) {
    await coll.insertOne(data)
    res.sendStatus(204).end()
    await client.close()
  } else {
    res.sendStatus(400).end()
  }  
})

app.get("/data", async (_req, res) => {
  await client.connect()

  res.json(await coll.find().toArray())

  await client.close()
})

app.delete("/data", async (_req, res) => {
  await client.connect()
  await coll.deleteMany()
  await client.close()
  res.send()
})

app.post("/move", async (req, res) => {
  await client.connect()
  const data = req.body
  let hasMoved = false

  if (data?.interval >= 0 && data?.duration >= 0 && data?.timestamp > 0) {
    const beforeDurationAvg = {}
    const afterDurationAvg = {}
    const dataBeforeDuration = data.timestamp + data.interval - data.duration
    const dataAfterDuration = data.timestamp + data.interval + data.duration
    const movementActivityBeforeDuration = await coll.find({"timestamp": { "$gt": dataBeforeDuration, "$lte": dataBeforeDuration + data.duration}}).toArray()
    const movementActivityAfterDuration = await coll.find({"timestamp": { "$gt": dataAfterDuration }}).toArray()
    

    const calcAverageForArr = (movementActivityArr, avgObj) => {
      const macs = new Set(movementActivityArr.map((activity) => activity.mac))
      macs.forEach((mac) => {
        const data = movementActivityArr.filter((activity) => activity.mac === mac)
        avgObj[mac] = movementActivityArr.map((activity) => activity.rssi).reduce((partial_sum, val) => partial_sum + val, 0) / data.length
      })
    }
    
    calcAverageForArr(movementActivityBeforeDuration, beforeDurationAvg)
    calcAverageForArr(movementActivityAfterDuration, afterDurationAvg)

    for (const [mac, avg] of Object.entries(beforeDurationAvg)) {
      const avgNew = afterDurationAvg[mac]
      if (Math.abs(avg) / Math.abs(avgNew) > movementPercentage) {
        hasMoved = true
      }
    }
  }

  await client.close()
  res.json(hasMoved)
})

app.listen(port, () => {
  console.log(`Movy api listening at http://localhost:${port}`)
})

