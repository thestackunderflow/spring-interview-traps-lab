package lab;

import java.util.concurrent.atomic.AtomicInteger;

/** Meant to be a singleton: one audit log for the whole app. The constructor says each time it runs. */
public class AuditLog {

    private static final AtomicInteger BUILT = new AtomicInteger();

    public AuditLog() {
        System.out.println("LAB: AuditLog constructor ran, #" + BUILT.incrementAndGet());
    }
}
