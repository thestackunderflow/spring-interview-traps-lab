package lab;

import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

/**
 * The episode's claim as behaviour (PLAN rev 2, #3): with @Component, orderService() calling auditLog() is a plain
 * Java call and builds a second AuditLog the container never sees (trap); with @Configuration the call returns the
 * container's one AuditLog (fix).
 */
class TrapAndFixTest {

    @Nested
    @SpringBootTest(properties = "lab.runner=off")
    @ActiveProfiles("trap")
    class Trap {
        @Autowired AuditLog auditLog;
        @Autowired OrderService orderService;

        @Test
        void orderServiceGotADifferentAuditLog() {
            assertNotSame(auditLog, orderService.auditLog());
        }
    }

    @Nested
    @SpringBootTest(properties = "lab.runner=off")
    @ActiveProfiles("fix")
    class Fix {
        @Autowired AuditLog auditLog;
        @Autowired OrderService orderService;

        @Test
        void orderServiceGotTheContainersAuditLog() {
            assertSame(auditLog, orderService.auditLog());
        }
    }
}
