package lab;

/** A RuntimeException, so Spring's default rule would roll back (checked exceptions do not: another episode). */
public class PaymentDeclinedException extends RuntimeException {

    public PaymentDeclinedException(String item) {
        super("card declined for " + item);
    }
}
