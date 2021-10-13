package functions;

import com.google.cloud.functions.HttpFunction;
import com.google.cloud.functions.HttpRequest;
import com.google.cloud.functions.HttpResponse;
import org.javalite.activejdbc.Base;

import java.io.BufferedWriter;
import java.io.IOException;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class HelloWorld implements HttpFunction {

    // Simple function to return "Hello World"
    @Override
    public void service(HttpRequest request, HttpResponse response)
            throws IOException {

        Template template;
        Map<String, Object> context = new HashMap<>();
        BufferedWriter writer = response.getWriter();
        var requestParam = request.getFirstQueryParameter("password");
        if (requestParam.isPresent() && requestParam.get().equals("password")) {
            template = new Template("analytics.html");
            template.loadTemplate();
            queryData(context);

        } else {
            template = new Template("unauthorized.html");
            template.loadTemplate();
        }
        writer.write(template.renderTemplate(context));

    }

    private void queryData(Map<String, Object> context) {
        String url = String.format("jdbc:mysql://%s:3306/%s",
                System.getenv("SQL_HOST"), System.getenv("SQL_DB"));

        String userName = System.getenv("SQL_USER");
        String password = System.getenv("SQL_PASSWORD");

        Base.open("com.mysql.cj.jdbc.Driver", url, userName, password);
        if (Base.hasConnection()) {
            List<Movie> movies = Movie.findAll();
            List<Rating> ratings = Rating.findAll();
            setMovieContext(movies, context);
            setRatingContext(ratings, context);
        }
        Base.close();
    }

    private void setMovieContext(List<Movie> movies, Map<String, Object> context) {
        MovieComparator comparator = new MovieComparator();
        movies.sort(comparator);
        Map<String, String> stats = new HashMap<>();

        Movie bestRating = movies.get(movies.size() - 1);
        Movie worstRating = movies.get(0);

        String bestRatingString =
                String.format("%s: %.1f", bestRating.get("title"), bestRating.getDouble("rating"));
        String worstMovieString =
                String.format("%s: %.1f", worstRating.get("title"), worstRating.getDouble("rating"));


        Double avg = movies.stream().mapToDouble(value -> value.getDouble("rating")).average().getAsDouble();

        stats.put("Highest rated movie: ", bestRatingString);
        stats.put("Lowest rated movie: ", worstMovieString);
        stats.put("Average movie rating: ", avg.toString());
        stats.put("Total movies: ", String.valueOf(movies.size()));


        context.put("stats", stats);
    }

    private void setRatingContext(List<Rating> ratings, Map<String, Object> context) {
        var stats = (Map<String, String>) context.get("stats");

        // Todo
        /*
        "Most rated movie(s)"
        "Least rated movie(s)"
        "Most user ratings"
        "Least user ratings"
         */

        stats.put("Total ratings", String.valueOf(ratings.size()));

        context.put("stats", stats);
    }

    private class MovieComparator implements Comparator<Movie> {
        @Override
        public int compare(Movie o1, Movie o2) {
            return o1.getDouble("rating").compareTo(o2.getDouble("rating"));
        }
    }
}