package lab;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.logging.LogLevel;
import org.springframework.boot.logging.LoggingSystem;
import org.springframework.stereotype.Component;

/**
 * After startup, turns on Spring's own TRACE logging for the bean factory (so the log shows each bean the container
 * creates from here on, without the startup flood), then serves three calls. Lines it prints start with LAB:.
 */
@Component
@ConditionalOnProperty(name = "lab.runner", havingValue = "on", matchIfMissing = true)
class LabRunner implements CommandLineRunner {

    static final String FACTORY = "org.springframework.beans.factory.support.DefaultListableBeanFactory";

    private final Counter counter;

    LabRunner(Counter counter) {
        this.counter = counter;
    }

    @Override
    public void run(String... args) {
        LoggingSystem.get(getClass().getClassLoader()).setLogLevel(FACTORY, LogLevel.TRACE);
        System.out.println("LAB: bean-factory TRACE logging on from here");
        for (int call = 1; call <= 3; call++) {
            System.out.println(counter.serve(call));
        }
    }
}
