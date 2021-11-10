package functions;

import com.mitchellbosecke.pebble.PebbleEngine;
import com.mitchellbosecke.pebble.loader.FileLoader;
import com.mitchellbosecke.pebble.loader.Loader;
import com.mitchellbosecke.pebble.template.PebbleTemplate;

import java.io.IOException;
import java.io.StringWriter;
import java.io.Writer;
import java.nio.file.Path;
import java.util.Map;

public class Template {
    private final Path indexFile;
    private PebbleTemplate template;

    public Template(String indexFile) {
        this.indexFile = Path.of(indexFile);
    }

    public void loadTemplate() {
        Loader<String> loader = new FileLoader();
        loader.setPrefix("./templates");
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
