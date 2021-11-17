import ballerina/http;
import ballerina/os;

int listenPort = check int:fromString(os:getEnv("PORT"));

service / on new http:Listener(listenPort) {
    resource function get fizzbuzz(int amount) returns json|error {
        final http:Client cli = check new (os:getEnv("HOST"));
        json data = {"amount": amount};
        json resp = check cli->post("/generateFizzBuzz", data);

        return resp;
    }
}
