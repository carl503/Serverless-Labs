const yaml = require('js-yaml');
const fs   = require('fs');
const axios = require('axios');

// Init graph
function main() {
  try {
    const doc = yaml.load(fs.readFileSync('orchestrator.yml', 'utf8'));
    const orchestrator = doc.orchestrator;
    const functions = orchestrator.functions;
    const start =  Object.keys(functions)[0];
    console.log(functions);
    initGraph(orchestrator, start);
    // Ping to prewarm if configured in orchestrator.yml
    if (doc.prewarm)
      prewarm(functions);
      // Run the functions
    
    console.log(functions);
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