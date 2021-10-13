package functions;

import com.google.cloud.functions.HttpFunction;
import com.google.cloud.functions.HttpRequest;
import com.google.cloud.functions.HttpResponse;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class HelloWorld implements HttpFunction {
    // Simple function to return "Hello World"
    @Override
    public void service(HttpRequest request, HttpResponse response)
            throws IOException {
        BufferedWriter writer = response.getWriter();
        Template template = new Template("index.html");
        template.loadTemplate();
        Map<String, Object> context = new HashMap<>();
        context.put("test", "waddup");

        writer.write(template.renderTemplate(context));
    }
}