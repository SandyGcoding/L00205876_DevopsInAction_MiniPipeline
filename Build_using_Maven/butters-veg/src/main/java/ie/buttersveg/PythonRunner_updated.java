package ie.buttersveg;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;

/**
 * Butters Veg application entry point.
 *
 * Docker runs this class with no arguments, which starts a minimal HTTP server
 * suitable for an EC2 container deployment. The original Python stock program
 * remains available with --cli (or with the original workbook-path argument).
 * The HTTP page intentionally does NOT claim to provide online ordering.
 */
public final class PythonRunner_updated {

    private static final String PAGE = """
            <!doctype html>
            <html lang="en">
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>Butters Veg</title>
              <style>
                body { font: 1.1rem/1.6 system-ui, sans-serif; background: #f6f5ef;
                       color: #253a2b; margin: 0; }
                main { max-width: 42rem; margin: 4rem auto; padding: 0 1.5rem; }
                h1 { font-size: 2.5rem; line-height: 1.2; }
                .note { padding: 1rem; background: #e3efe1; border-radius: .5rem; }
              </style>
            </head>
            <body>
              <main>
                <h1>Butters Veg</h1>
                <p>Connecting local vegetable growers and buyers.</p>
                <p class="note">The Java application is running on the deployment server.</p>
                <p>This is a CI/CD pipeline demonstration, not an online ordering service.</p>
              </main>
            </body>
            </html>
            """;

    private PythonRunner_updated() {
        // Utility entry-point class.
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        if (args.length == 0) {
            serveHttp(); // The unchanged Docker CMD invokes this mode.
            return;
        }

        if ("--cli".equals(args[0])) {
            runPython(Arrays.copyOfRange(args, 1, args.length));
        } else {
            // Preserve the original one-argument workbook invocation.
            runPython(args);
        }
    }

    private static void serveHttp() throws IOException {
        String configuredPort = System.getenv("PORT");
        int port = (configuredPort == null || configuredPort.isBlank())
                ? 8080 : Integer.parseInt(configuredPort);
        if (port < 1 || port > 65535) {
            throw new IllegalArgumentException("PORT must be between 1 and 65535");
        }

        // Bind to all interfaces so a Docker -p host:container mapping works.
        HttpServer server = HttpServer.create(new InetSocketAddress("0.0.0.0", port), 0);
        server.createContext("/", PythonRunner_updated::respond);
        server.start();
        System.out.println("Butters Veg ready on 0.0.0.0:" + port);
    }

    private static void respond(HttpExchange exchange) throws IOException {
        try (exchange) {
            String method = exchange.getRequestMethod();
            String path = exchange.getRequestURI().getPath();
            int status;
            String body;
            String contentType;

            if (!"GET".equals(method) && !"HEAD".equals(method)) {
                status = 405;
                body = "Method not allowed\n";
                contentType = "text/plain; charset=utf-8";
                exchange.getResponseHeaders().set("Allow", "GET, HEAD");
            } else if ("/".equals(path)) {
                status = 200;
                body = PAGE;
                contentType = "text/html; charset=utf-8";
            } else if ("/health".equals(path)) {
                status = 200;
                body = "OK\n";
                contentType = "text/plain; charset=utf-8";
            } else {
                status = 404;
                body = "Not found\n";
                contentType = "text/plain; charset=utf-8";
            }

            exchange.getResponseHeaders().set("Content-Type", contentType);
            exchange.getResponseHeaders().set("X-Content-Type-Options", "nosniff");
            exchange.getResponseHeaders().set("Cache-Control", "no-store");
            byte[] output = body.getBytes(StandardCharsets.UTF_8);
            if ("HEAD".equals(method)) {
                exchange.sendResponseHeaders(status, -1);
            } else {
                exchange.sendResponseHeaders(status, output.length);
                try (OutputStream stream = exchange.getResponseBody()) {
                    stream.write(output);
                }
            }
            System.out.printf("HTTP %s %s -> %d%n", method, path, status);
        }
    }

    // Original Python launcher preserved for the manually tested stock program.
    private static void runPython(String[] args) throws IOException, InterruptedException {
        if (args.length > 1) {
            System.err.println("Usage: java -cp app.jar ie.buttersveg.PythonRunner_updated --cli [path-to-workbook]");
            System.exit(2);
            return;
        }

        Path workbook = Path.of(args.length == 0 ? "Veg.xlsx" : args[0])
                .toAbsolutePath().normalize();
        if (args.length == 0 && Files.notExists(workbook)) {
            try (InputStream starter = openResource("/Veg.xlsx")) {
                Files.copy(starter, workbook);
            }
        }
        if (!Files.isRegularFile(workbook)) {
            throw new FileNotFoundException("Excel workbook not found: " + workbook);
        }

        String python = System.getenv("VEG_PYTHON");
        if (python == null || python.isBlank()) {
            python = System.getProperty("os.name").startsWith("Windows") ? "py" : "python3";
        }

        Path script = Files.createTempFile("veg-stock-", ".py");
        int exitCode;
        try {
            try (InputStream source = openResource("/Test.py")) {
                Files.copy(source, script, StandardCopyOption.REPLACE_EXISTING);
            }
            Process process = new ProcessBuilder(python, "-u", script.toString(), workbook.toString())
                    .inheritIO()
                    .start();
            try {
                exitCode = process.waitFor();
            } catch (InterruptedException interrupted) {
                process.destroyForcibly();
                throw interrupted;
            }
        } finally {
            Files.deleteIfExists(script);
        }

        if (exitCode != 0) {
            System.exit(exitCode);
        }
    }

    private static InputStream openResource(String name) throws FileNotFoundException {
        InputStream resource = PythonRunner_updated.class.getResourceAsStream(name);
        if (resource == null) {
            throw new FileNotFoundException("Packaged resource not found: " + name);
        }
        return resource;
    }
}
