import ballerina/http;
import ballerina/os;
 

int listenPort = check int:fromString(os:getEnv("PORT"));

service / on new http:Listener(listenPort) {
    resource function post countFizzBuzzes(@http:Payload json payload) returns json|error {
        int fizzes = 0;
        int buzzes = 0;
        int fizzBuzzes = 0;
        json[] fizzbuzzes = <json[]>(check payload.fizzbuzz);
        int i = 0;
        
        while i < fizzbuzzes.length() {
            string val = fizzbuzzes[i].toString();
            match val {
                "Fizz" => {fizzes += 1;}
                "Buzz" => {buzzes += 1;}
                "FizzBuzz" => {fizzBuzzes += 1;}
                _ => {}
            }
            i += 1;
        }

        return {
            "fizzes": fizzes,
            "buzzes": buzzes,
            "fizzBuzzes": fizzBuzzes,
            "fizzbuzz": fizzbuzzes
        };
    }
}