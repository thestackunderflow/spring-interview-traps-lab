package lab;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.config.ConfigurableBeanFactory;
import org.springframework.context.annotation.Scope;

/** The A/B card shows real files: the two TicketCounter variants line up row for row and differ only where the fix is. */
class VariantShapeTest {

    static final Path JAVA = Path.of("src/main/java/lab");

    @Test
    void ticketIsReallyPrototype() {
        assertEquals(ConfigurableBeanFactory.SCOPE_PROTOTYPE, Ticket.class.getAnnotation(Scope.class).value());
    }

    @Test
    void theClassBodiesDifferOnlyInTheInjectedFieldTheConstructorAndTheCall() throws IOException {
        List<String> a = Files.readAllLines(JAVA.resolve("trap/TicketCounter.java"));
        List<String> b = Files.readAllLines(JAVA.resolve("fix/TicketCounter.java"));
        assertEquals(a.size(), b.size(), "same row count");
        int from = a.indexOf("public class TicketCounter implements Counter {");
        assertTrue(from > 0);
        assertEquals(from, b.indexOf("public class TicketCounter implements Counter {"), "same line numbers");
        List<String> differing = new ArrayList<>();
        for (int i = from; i < a.size(); i++) if (!a.get(i).equals(b.get(i))) differing.add(b.get(i).strip());
        assertEquals(List.of(
                "private final ObjectProvider<Ticket> tickets;",
                "public TicketCounter(ObjectProvider<Ticket> tickets) {",
                "this.tickets = tickets;",
                "return tickets.getObject().describe(call);"), differing);
    }
}
