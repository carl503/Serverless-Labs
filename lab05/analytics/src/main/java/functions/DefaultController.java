package functions;

import org.javalite.activejdbc.Base;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.io.IOException;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.OptionalDouble;
import java.util.Set;
import java.util.stream.Collectors;

@Controller
public class DefaultController {
    private static final String RATING = "rating";
    private static final String MOVIE_NAME = "title";

    @RequestMapping("/")
    @ResponseBody
    public String index(@RequestParam(required = false) String password) throws IOException {
        Template template;
        Map<String, Object> context = new HashMap<>();
        if (password != null && password.equals("password")) {
            template = new Template("analytics.html");
            template.loadTemplate();
            queryData(context);
        } else {
            template = new Template("unauthorized.html");
            template.loadTemplate();
        }
        return template.renderTemplate(context);
    }

    private void queryData(Map<String, Object> context) {
        String url = String.format("jdbc:mysql://%s:3306/%s",
                System.getenv("SQL_HOST"), System.getenv("SQL_DB"));

        String userName = System.getenv("SQL_USER");
        String password = System.getenv("SQL_PASS");

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
        Map<String, String> stats = new LinkedHashMap<>();

        double avgRating = 0.0;

        Movie bestRating = movies.get(movies.size() - 1);
        Movie worstRating = movies.get(0);

        String titleRating = "Name: %s: Rating: %.1f";
        String bestRatingString =
                String.format(titleRating, bestRating.get(MOVIE_NAME), bestRating.getDouble(RATING));
        String worstMovieString =
                String.format(titleRating, worstRating.get(MOVIE_NAME), worstRating.getDouble(RATING));

        OptionalDouble opt = movies
                .stream()
                .mapToDouble(value -> value.getDouble(RATING))
                .average();

        if (opt.isPresent()) {
            avgRating = opt.getAsDouble();
        }

        stats.put("Highest rated movie: ", bestRatingString);
        stats.put("Lowest rated movie: ", worstMovieString);
        stats.put("Average movie rating: ", String.format("%.1f", avgRating));
        stats.put("Total movies: ", String.valueOf(movies.size()));

        context.put("stats", stats);
    }

    private void setRatingContext(List<Rating> ratings, Map<String, Object> context) {
        var stats = (LinkedHashMap<String, String>) context.get("stats");

        Set<Integer> movieIds = ratings
                .stream()
                .map(rating -> rating.getInteger("id"))
                .collect(Collectors.toSet());

        HashMap<Integer, Integer> ratingMap = new HashMap<>();
        HashMap<Integer, Integer> sortedRatingMap = new LinkedHashMap<>();

        movieIds.forEach(movieId -> ratingMap.put(movieId, 0));

        ratings
                .stream()
                .map(rating -> rating.getInteger("id"))
                .forEach(rating -> ratingMap.computeIfPresent(rating, (key, value) -> ++value));


        ratingMap.entrySet()
                .stream()
                .sorted(Map.Entry.comparingByValue())
                .forEachOrdered(rating -> sortedRatingMap.put(rating.getKey(), rating.getValue()));

        var it = sortedRatingMap.entrySet().iterator();
        int leastRatedMovieId = it.next().getKey();
        int mostRatedMovieId = 0;
        while (it.hasNext())
            mostRatedMovieId = it.next().getKey();


        String leastRatedMovie = Movie.findFirst("id = ?", leastRatedMovieId).getString(MOVIE_NAME);
        String mostRatedMovie = Movie.findFirst("id = ?", mostRatedMovieId).getString(MOVIE_NAME);

        stats.put("Total ratings: ", String.valueOf(ratings.size()));
        stats.put("Most rated movie: ", mostRatedMovie);
        stats.put("Least rated movie: ", leastRatedMovie);

        context.put("stats", stats);
    }

    private static class MovieComparator implements Comparator<Movie> {
        @Override
        public int compare(Movie o1, Movie o2) {
            return o1.getDouble(RATING).compareTo(o2.getDouble(RATING));
        }
    }
}
