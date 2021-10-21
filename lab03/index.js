const yaml = require('js-yaml');
const fs   = require('fs');
const axios = require('axios');

let prewarmActive;
// Init graph
async function main(testMode) {
  try {
    const doc = yaml.load(fs.readFileSync('orchestrator.yml', 'utf8'));
    const orchestrator = doc.orchestrator;
    const functions = orchestrator.functions;
    const start = Object.keys(functions)[0];
    initGraph(orchestrator, start);
    // Ping to prewarm if configured in orchestrator.yml
    
    if (orchestrator.prewarm) await prewarm(functions);

    prewarmActive = orchestrator.prewarm;
    console.log(`Prewarm: ${prewarmActive ? "Active": "Inactive"}`);
    // Run the functions
    // function(s);time;
    if (testMode) {
      let startTime = Date.now();
      for (let i = 0; i < 300; i++) {
        await exec(orchestrator, start, fetchAndRelayData, null);
        console.log("-".repeat(80));
      }
      let endTime = Date.now();
      logLineToFile(`All;${(endTime - startTime) / 300}`, `log-all-pre-${prewarmActive ? "Active":"Inactive"}.csv`)
    } else {
      await exec(orchestrator, start, fetchAndRelayData, null)
    }

  } catch (e) {
    console.log("Error in main");
    console.error(e);
  }
}

function fetchAndRelayData(func, payload) {
  if (payload) {
    return axios.post(func.url, payload);
  } else {
    return axios.get(func.url);
  }
}

async function exec(orchestrator, func, callback, payload) {
  const f = orchestrator.functions[func] || func;
  const output = f.output;
  const length = output?.length;

  let random = 0;

  if(length > 1) {
    random = Math.floor(Math.random() * length);
  }
  try {
    // start
    const startTime = Date.now();
    payload = (await callback(f, payload)).data;
    const endTime = Date.now();
    logLineToFile(`${f.name};${endTime - startTime}`, `log-${prewarmActive ? "prewarm":"noPrewarm"}.csv`)

    console.log(`Function: ${f.name}, Execution time: ${endTime - startTime}ms`)
    // end

    if(output) {
      exec(orchestrator, output[random], callback, payload);
    } else {
      // last output
      console.log(`Last function returnd (first entry): \n[${JSON.stringify(payload[0])},...]`);
    }
  } catch (e) {
    console.error(`${f.name} failed due to error: ${e}`);
  }
}

function initGraph(orchestrator, func) {
  const f = orchestrator.functions[func];
  const output = f.output;
  const length = output?.length;
  
  let tmpList = [];
  
  for (let i = 0; i < length; i++) {
    tmpList.push(initGraph(orchestrator, output?.pop()));
  }

  output?.push(...tmpList);

  return f;
}


function prewarm(functions) {
  const reqPromises = [];
  try {
    for (const key in functions) {
      const func = functions[key];
      reqPromises.push(axios.get(func.url + "/ping"));
    } 
  } catch (e) {
    console.log("literally unreachable");
    console.error(`Failed prewarm due to: ${e}`);
  }

  return Promise.all(reqPromises);
}

function logLineToFile(line, filename) {
  if (!fs.existsSync(filename)) {
    fs.writeFileSync(filename, "");
  }
  fs.appendFile(filename, line + "\n", console.error);
}

main(true);
