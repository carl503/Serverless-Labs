package functions;

import com.mitchellbosecke.pebble.PebbleEngine;
import com.mitchellbosecke.pebble.loader.FileLoader;
import com.mitchellbosecke.pebble.loader.Loader;
import com.mitchellbosecke.pebble.template.PebbleTemplate;

import java.io.IOException;
import java.io.InputStream;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

public class Template {
    private final Path indexFile;
    private PebbleTemplate template;

    public Template(String indexFile) {
        this.indexFile = Path.of(indexFile);
    }

    public void loadTemplate() throws IOException {
        if (Files.exists(indexFile)) {
            InputStream is = HelloWorld
                    .class
                    .getClassLoader()
                    .getResourceAsStream(indexFile.getFileName().toString());

            if (is == null)
                throw new IOException("indexFile could not be loaded from resource");
            Files.delete(indexFile);
            Files.copy(is, indexFile);
        }

        Loader<String> loader = new FileLoader();
        loader.setPrefix("./");
        PebbleEngine engine = new PebbleEngine
                .Builder()
                .loader(loader)
                .build();

        this.template = engine.getTemplate(indexFile.toString());
    }

    public String renderTemplate(Map<String, Object> context) throws IOException {
        Writer stringWriter = new StringWriter();
        this.template.evaluate(stringWriter, context);
        return stringWriter.toString();
    }
}
