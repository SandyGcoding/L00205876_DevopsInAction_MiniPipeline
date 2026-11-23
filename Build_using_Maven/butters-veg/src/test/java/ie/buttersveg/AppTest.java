package ie.buttersveg;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class AppTest {
    @Test
    void appResourcesAreAvailable() {
        assertNotNull(PythonRunner_updated.class.getResource("/Test.py"));
        assertNotNull(PythonRunner_updated.class.getResource("/Veg.xlsx"));
    }
}