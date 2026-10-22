package lab;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;

/**
 * The A/B code card shows real files, so the variants may differ only where the lesson says (DECISIONS §2):
 * the transactional method is byte-identical in both places, and placeOrder differs in exactly one row, the call.
 */
class VariantShapeTest {

    static final Path JAVA = Path.of("src/main/java/lab");

    static List<String> read(String rel) throws IOException {
        return Files.readAllLines(JAVA.resolve(rel));
    }

    /** The lines from the method's signature to its closing brace (4-space indented members). */
    static List<String> method(List<String> file, String signature) {
        int from = -1;
        for (int i = 0; i < file.size(); i++) {
            if (file.get(i).contains(signature)) { from = i; break; }
        }
        assertTrue(from >= 0, "not found: " + signature);
        if (file.get(from - 1).strip().startsWith("@")) from--;   // keep the annotation row
        int to = from;
        while (!file.get(to).equals("    }")) to++;
        return file.subList(from, to + 1);
    }

    @Test
    void theTransactionalMethodIsByteIdenticalInBothVariants() throws IOException {
        List<String> trap = method(read("trap/Checkout.java"), "public void saveAndCharge(");
        List<String> fix = method(read("fix/OrderWriter.java"), "public void saveAndCharge(");
        assertEquals(trap, fix);
        assertEquals("    @Transactional", trap.get(0));
    }

    @Test
    void placeOrderDiffersOnlyInTheCallTarget() throws IOException {
        List<String> trapFile = read("trap/Checkout.java");
        List<String> fixFile = read("fix/Checkout.java");
        List<String> trap = method(trapFile, "public void placeOrder(");
        List<String> fix = method(fixFile, "public void placeOrder(");
        assertEquals(trap.size(), fix.size());
        int differing = 0;
        for (int i = 0; i < trap.size(); i++) if (!trap.get(i).equals(fix.get(i))) differing++;
        assertEquals(1, differing);
        assertTrue(trap.contains("        this.saveAndCharge(item);"));
        assertTrue(fix.contains("        writer.saveAndCharge(item);"));
        // same line numbers in both files, so the A/B card's rows line up
        assertEquals(trapFile.indexOf(trap.get(0)), fixFile.indexOf(fix.get(0)));
    }

    @Test
    void theTrapMethodIsPublicSoThePrivateRuleIsNotTheAnswer() throws Exception {
        var m = lab.trap.Checkout.class.getMethod("saveAndCharge", String.class);
        assertTrue(java.lang.reflect.Modifier.isPublic(m.getModifiers()));
    }
}
