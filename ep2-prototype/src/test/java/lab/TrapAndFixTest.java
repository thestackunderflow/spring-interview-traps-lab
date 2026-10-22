package lab;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

/**
 * The episode's claim as behaviour (PLAN rev 2, #2): the singleton keeps the one prototype it got when it was built
 * (trap); asking the container through an ObjectProvider each time gives a new one per call (fix).
 */
class TrapAndFixTest {

    static String ticketOf(String served) {   // "LAB: call 1 served by Ticket #3, identityHashCode ..." -> "#3"
        return served.replaceAll(".* served by Ticket (#\\d+),.*", "$1");
    }

    @Nested
    @SpringBootTest(properties = "lab.runner=off")
    @ActiveProfiles("trap")
    class Trap {
        @Autowired Counter counter;

        @Test
        void everyCallGetsTheSameTicket() {
            String a = ticketOf(counter.serve(1));
            assertEquals(a, ticketOf(counter.serve(2)));
            assertEquals(a, ticketOf(counter.serve(3)));
        }
    }

    @Nested
    @SpringBootTest(properties = "lab.runner=off")
    @ActiveProfiles("fix")
    class Fix {
        @Autowired Counter counter;

        @Test
        void everyCallGetsANewTicket() {
            String a = ticketOf(counter.serve(1));
            String b = ticketOf(counter.serve(2));
            assertNotEquals(a, b);
            assertNotEquals(b, ticketOf(counter.serve(3)));
        }
    }
}
