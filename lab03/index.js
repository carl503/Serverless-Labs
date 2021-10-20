const yaml = require('js-yaml');
const fs   = require('fs');
const axios = require('axios');

// Init graph
async function main() {
  try {
    const doc = yaml.load(fs.readFileSync('orchestrator.yml', 'utf8'));
    const orchestrator = doc.orchestrator;
    const functions = orchestrator.functions;
    const start = Object.keys(functions)[0];
    initGraph(orchestrator, start);
    // Ping to prewarm if configured in orchestrator.yml
    if (doc.prewarm) prewarm(functions);
    // Run the functions
    await exec(orchestrator, start, fetchAndRelayData, null)
  } catch (e) {
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
    payload = (await callback(f, payload)).data;
    console.log("-----------------------------");
    console.log(payload[0]);
    console.log(payload[5]);
    console.log("-----------------------------");
    if(output) {
      exec(orchestrator, output[random], callback, payload);
    }
  } catch (e) {
    console.error(e);
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
      reqPromises.push(axios.get(`${func.url}/ping`));
    } 
  } catch (e) {
    console.error(e);
  }

  return Promise.all(reqPromises);
}

main();