package lab;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.test.context.ActiveProfiles;

/**
 * The episode's claim, as behaviour (PLAN rev 2, #1): with the trap, the order row stays after the exception;
 * with the fix (the same method on its own bean), it is undone. The runner is off here; the tests call the bean.
 */
class TrapAndFixTest {

    static int ordersAfterFailedOrder(Shop shop, JdbcClient db) {
        db.sql("delete from orders").update();
        assertThrows(PaymentDeclinedException.class, () -> shop.placeOrder("book"));
        return db.sql("select count(*) from orders").query(Integer.class).single();
    }

    @Nested
    @SpringBootTest(properties = "lab.runner=off")
    @ActiveProfiles("trap")
    class Trap {
        @Autowired Shop shop;
        @Autowired JdbcClient db;

        @Test
        void theRowStaysBecauseNoTransactionStarted() {
            assertEquals(1, ordersAfterFailedOrder(shop, db));
        }

        @Test
        void theBeanIsProxiedAnywayOnlyTheInnerCallSkipsIt() {
            // acc M2: Spring's stand-in exists in the trap too; the outer call goes through it
            assertTrue(AopUtils.isCglibProxy(shop), shop.getClass().getName());
        }
    }

    @Nested
    @SpringBootTest(properties = "lab.runner=off")
    @ActiveProfiles("fix")
    class Fix {
        @Autowired Shop shop;
        @Autowired JdbcClient db;

        @Test
        void theRowIsUndone() {
            assertEquals(0, ordersAfterFailedOrder(shop, db));
        }
    }
}
