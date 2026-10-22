package lab;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

/** Compares the container's auditLog bean with the one OrderService holds. Lines it prints start with LAB:. */
@Component
@ConditionalOnProperty(name = "lab.runner", havingValue = "on", matchIfMissing = true)
class LabRunner implements CommandLineRunner {

    private final AuditLog auditLog;
    private final OrderService orderService;

    LabRunner(AuditLog auditLog, OrderService orderService) {
        this.auditLog = auditLog;
        this.orderService = orderService;
    }

    @Override
    public void run(String... args) {
        System.out.println("LAB: container's auditLog bean, identityHashCode " + id(auditLog));
        System.out.println("LAB: orderService's auditLog,   identityHashCode " + id(orderService.auditLog()));
        System.out.println("LAB: same object? " + (auditLog == orderService.auditLog()));
    }

    private static String id(Object o) {
        return Integer.toHexString(System.identityHashCode(o));
    }
}
