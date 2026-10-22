package lab.fix;

import lab.Shop;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;

/**
 * The fix: the same @Transactional method now lives on its own bean, OrderWriter,
 * so the call from placeOrder goes through Spring and a transaction starts.
 */
@Service
@Profile("fix")
public class Checkout implements Shop {

    private final OrderWriter writer;

    public Checkout(OrderWriter writer) {
        this.writer = writer;
    }

    public void placeOrder(String item) {
        writer.saveAndCharge(item);
    }
}
