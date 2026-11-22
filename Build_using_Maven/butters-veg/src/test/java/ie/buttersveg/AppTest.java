package ie.buttersveg;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class AppTest {
    @Test
    void appResourcesAreAvailable() {
        assertNotNull(PythonRunner.class.getResource("/Test.py"));
        assertNotNull(PythonRunner.class.getResource("/Veg.xlsx"));
    }
}