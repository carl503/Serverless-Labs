import ballerina/http;
import ballerina/os;

int listenPort = check int:fromString(os:getEnv("PORT"));

service / on new http:Listener(listenPort) {
    resource function post generateFizzBuzz(@http:Payload json payload) returns json|error {
        final http:Client cli = check new (os:getEnv("HOST"));
        int val = check payload.amount;
        string[] fizzbuzzes = generateFizzBuzz(val);
        json data = {"fizzbuzz": fizzbuzzes};
        json resp = check cli->post("/countFizzBuzzes", data);

        return resp;
    }
}

function generateFizzBuzz(int amount) returns string[] {
    int i = 0;
    string[] fizzbuzzes = []; 
    while i < amount {

        string line = "";
        if (i % 3 == 0) { line += "Fizz"; }
        if (i % 5 == 0) { line += "Buzz"; }
        if (line == "") { line = i.toString(); }
    
        fizzbuzzes.push(line);
        i += 1;
    }

    return fizzbuzzes;
}