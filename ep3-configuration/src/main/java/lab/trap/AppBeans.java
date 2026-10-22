package lab.trap;

import lab.AuditLog;
import lab.OrderService;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Component;
import org.springframework.context.annotation.Profile;

@Component
@Profile("trap")
public class AppBeans {

    @Bean
    public AuditLog auditLog() {
        return new AuditLog();
    }

    @Bean
    public OrderService orderService() {
        return new OrderService(auditLog());
    }
}
