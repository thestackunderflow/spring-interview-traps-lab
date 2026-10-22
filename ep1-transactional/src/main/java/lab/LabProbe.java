package lab;

import org.springframework.transaction.support.TransactionSynchronizationManager;

/** The lab's own line (never Spring's): is a Spring transaction active on this thread right now? */
public final class LabProbe {

    private LabProbe() {
    }

    public static void transactionActive() {
        boolean active = TransactionSynchronizationManager.isActualTransactionActive();
        System.out.println("LAB: at the insert, transaction active = " + active);
    }
}
