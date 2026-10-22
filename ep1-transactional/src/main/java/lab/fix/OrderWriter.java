package lab.fix;

import lab.LabProbe;
import lab.PaymentDeclinedException;
import org.springframework.context.annotation.Profile;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Profile("fix")
public class OrderWriter {

    private final JdbcClient db;

    public OrderWriter(JdbcClient db) {
        this.db = db;
    }

    @Transactional
    public void saveAndCharge(String item) {
        db.sql("insert into orders(item) values (?)")
                .param(item).update();
        LabProbe.transactionActive();
        throw new PaymentDeclinedException(item);
    }
}
