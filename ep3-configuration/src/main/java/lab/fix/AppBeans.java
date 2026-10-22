package lab.fix;

import lab.AuditLog;
import lab.OrderService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;

@Configuration
@Profile("fix")
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
