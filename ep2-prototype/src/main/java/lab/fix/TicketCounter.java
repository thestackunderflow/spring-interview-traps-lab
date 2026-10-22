package lab.fix;

import lab.Counter;
import lab.Ticket;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Service;

@Service
@Profile("fix")
public class TicketCounter implements Counter {

    private final ObjectProvider<Ticket> tickets;

    public TicketCounter(ObjectProvider<Ticket> tickets) {
        this.tickets = tickets;
    }

    public String serve(int call) {
        return tickets.getObject().describe(call);
    }
}
