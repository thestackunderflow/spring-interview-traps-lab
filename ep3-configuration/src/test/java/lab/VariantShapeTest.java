package lab;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

/** The A/B card shows real files: the two AppBeans variants differ in exactly one row of the class, the annotation. */
class VariantShapeTest {

    static final Path JAVA = Path.of("src/main/java/lab");

    @Test
    void theOnlyChangeIsComponentToConfiguration() throws IOException {
        List<String> a = Files.readAllLines(JAVA.resolve("trap/AppBeans.java"));
        List<String> b = Files.readAllLines(JAVA.resolve("fix/AppBeans.java"));
        assertEquals(a.size(), b.size(), "same row count");
        int from = a.indexOf("@Component");
        assertTrue(from > 0);
        assertEquals("@Configuration", b.get(from), "same line number");
        List<String> differing = new ArrayList<>();
        for (int i = from; i < a.size(); i++) if (!a.get(i).equals(b.get(i))) differing.add(a.get(i) + " -> " + b.get(i));
        assertEquals(List.of("@Component -> @Configuration", "@Profile(\"trap\") -> @Profile(\"fix\")"), differing);
    }

    @Test
    void orderServiceCallsTheOtherBeanMethodDirectly() throws IOException {
        for (String v : List.of("trap", "fix")) {
            assertTrue(Files.readAllLines(JAVA.resolve(v + "/AppBeans.java")).contains("        return new OrderService(auditLog());"), v);
        }
    }
}
