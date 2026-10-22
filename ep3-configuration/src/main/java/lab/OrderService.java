package lab;

/** Needs the audit log; gets it through its constructor. */
public class OrderService {

    private final AuditLog auditLog;

    public OrderService(AuditLog auditLog) {
        this.auditLog = auditLog;
    }

    public AuditLog auditLog() {
        return auditLog;
    }
}
