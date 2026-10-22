package lab.trap;

import lab.LabProbe;
import lab.PaymentDeclinedException;
import lab.Shop;
import org.springframework.context.annotation.Profile;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Profile("trap")
public class Checkout implements Shop {

    private final JdbcClient db;

    public Checkout(JdbcClient db) {
        this.db = db;
    }

    public void placeOrder(String item) {
        this.saveAndCharge(item);
    }

    @Transactional
    public void saveAndCharge(String item) {
        db.sql("insert into orders(item) values (?)")
                .param(item).update();
        LabProbe.transactionActive();
        throw new PaymentDeclinedException(item);
    }
}
