package ie.buttersveg;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Runs the production HTTP response handler inside the same JVM as JaCoCo,
 * so the requests contribute to Java code-coverage measurements.
 *
 * This assumes the production class is named PythonRunner_updated.
 */
class AppTest {
    private static HttpServer server;
    private static URI baseUri;
    private static HttpClient client;

    @BeforeAll
    static void startTestServer() throws Exception {
        Method productionHandler = PythonRunner_updated.class.getDeclaredMethod("respond", HttpExchange.class);
        productionHandler.setAccessible(true);

        // Port zero asks the OS for an unused port; bind only to loopback.
        server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        server.createContext("/", exchange -> {
            try {
                productionHandler.invoke(null, exchange);
            } catch (InvocationTargetException error) {
                Throwable cause = error.getCause();
                if (cause instanceof IOException io) {
                    throw io;
                }
                throw new IOException("Production HTTP handler failed", cause);
            } catch (IllegalAccessException error) {
                throw new IOException("Could not access production HTTP handler", error);
            }
        });
        server.start();

        baseUri = URI.create("http://127.0.0.1:" + server.getAddress().getPort());
        client = HttpClient.newHttpClient();
    }

    @AfterAll
    static void stopTestServer() {
        if (server != null) {
            server.stop(0);
        }
    }

    private static HttpResponse<String> request(String method, String path) throws Exception {
        HttpRequest httpRequest = HttpRequest.newBuilder(baseUri.resolve(path))
                .method(method, HttpRequest.BodyPublishers.noBody())
                .build();
        return client.send(httpRequest, HttpResponse.BodyHandlers.ofString());
    }

    @Test
    void appResourcesAreAvailable() {
        assertNotNull(PythonRunner_updated.class.getResource("/Test.py"));
        assertNotNull(PythonRunner_updated.class.getResource("/Veg.xlsx"));
    }

    @Test
    void homePageReturnsHtml() throws Exception {
        HttpResponse<String> response = request("GET", "/");
        assertEquals(200, response.statusCode());
        assertTrue(response.body().contains("<h1>Butters Veg</h1>"));
        assertTrue(response.headers().firstValue("Content-Type").orElse("").contains("text/html"));
    }

    @Test
    void healthEndpointReturnsOk() throws Exception {
        HttpResponse<String> response = request("GET", "/health");
        assertEquals(200, response.statusCode());
        assertEquals("OK\n", response.body());
    }

    @Test
    void unknownPageReturns404() throws Exception {
        HttpResponse<String> response = request("GET", "/missing");
        assertEquals(404, response.statusCode());
        assertEquals("Not found\n", response.body());
    }

    @Test
    void postRequestReturns405() throws Exception {
        HttpResponse<String> response = request("POST", "/");
        assertEquals(405, response.statusCode());
        assertEquals("GET, HEAD", response.headers().firstValue("Allow").orElse(""));
    }

    @Test
    void headRequestHasNoResponseBody() throws Exception {
        HttpResponse<String> response = request("HEAD", "/");
        assertEquals(200, response.statusCode());
        assertEquals("", response.body());
    }

    @Test
    void responsesIncludeContentTypeProtection() throws Exception {
        HttpResponse<String> response = request("GET", "/");
        assertEquals("nosniff", response.headers().firstValue("X-Content-Type-Options").orElse(""));
    }

    @Test
    void missingWorkbookIsRejectedBeforePythonIsStarted() {
        Path missingWorkbook = Path.of("missing-test-" + System.nanoTime() + ".xlsx");
        assertThrows(FileNotFoundException.class,
                () -> PythonRunner_updated.main(new String[]{missingWorkbook.toString()}));
    }
}
