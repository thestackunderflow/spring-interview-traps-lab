package lab;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Component;

/** Calls placeOrder once from outside the bean, then counts the order rows. Lines it prints start with LAB:. */
@Component
@ConditionalOnProperty(name = "lab.runner", havingValue = "on", matchIfMissing = true)
class LabRunner implements CommandLineRunner {

    private final Shop shop;
    private final JdbcClient db;

    LabRunner(Shop shop, JdbcClient db) {
        this.shop = shop;
        this.db = db;
    }

    @Override
    public void run(String... args) {
        System.out.println("LAB: calling placeOrder(\"book\") from outside the bean");
        try {
            shop.placeOrder("book");
        } catch (PaymentDeclinedException e) {
            System.out.println("LAB: placeOrder threw PaymentDeclinedException: " + e.getMessage());
        }
        int orders = db.sql("select count(*) from orders").query(Integer.class).single();
        System.out.println("LAB: orders after failure = " + orders);
    }
}
