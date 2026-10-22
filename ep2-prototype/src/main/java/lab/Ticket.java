package lab;

import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.beans.factory.config.ConfigurableBeanFactory;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

/** Prototype scope: the container makes a new Ticket every time it is asked for one. */
@Component
@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)
public class Ticket {

    private static final AtomicInteger MADE = new AtomicInteger();

    private final int number = MADE.incrementAndGet();

    public Ticket() {
        System.out.println("LAB: Ticket #" + number + " constructed");
    }

    /** Printed from inside the object, so the number is this object's own (never a proxy's). */
    public String describe(int call) {
        String identity = Integer.toHexString(System.identityHashCode(this));
        return "LAB: call " + call + " served by Ticket #" + number + ", identityHashCode " + identity;
    }
}
