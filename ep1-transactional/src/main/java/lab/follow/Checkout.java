package lab.follow;

import lab.LabProbe;
import lab.PaymentDeclinedException;
import lab.Shop;
import org.springframework.context.annotation.Profile;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

/** The interview follow-up: both methods annotated, the inner one REQUIRES_NEW, called with this. */
@Service
@Profile("follow")
public class Checkout implements Shop {

    private final JdbcClient db;

    public Checkout(JdbcClient db) {
        this.db = db;
    }

    @Transactional
    public void placeOrder(String item) {
        this.saveAndCharge(item);
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void saveAndCharge(String item) {
        db.sql("insert into orders(item) values (?)")
                .param(item).update();
        LabProbe.transactionActive();
        throw new PaymentDeclinedException(item);
    }
}
