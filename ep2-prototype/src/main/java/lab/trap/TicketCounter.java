package lab.trap;

import lab.Counter;
import lab.Ticket;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;

/** A singleton: built once, so its constructor runs once. */
@Service
@Profile("trap")
public class TicketCounter implements Counter {

    private final Ticket ticket;

    public TicketCounter(Ticket ticket) {
        this.ticket = ticket;
    }

    public String serve(int call) {
        return ticket.describe(call);
    }
}
