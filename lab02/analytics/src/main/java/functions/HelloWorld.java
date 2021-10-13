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
        Template template = new Template("analytics.html");
        template.loadTemplate();
        Map<String, Object> context = new HashMap<>();
        Map<String, String> analytics = Map.of(
                "Average movie rating", "",
                "Highest rated movie(s)", "",
                "Lowest rated movie(s)", "",
                "Most rated movie(s)", "",
                "Least rated movie(s)", "",
                "Most user ratings", "",
                "Least user ratings", "",
                "Total ratings", "",
                "Total movies", ""
        );
        context.put("stats", analytics);
        writer.write(template.renderTemplate(context));
    }
}