package lab;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/** Episode 1: run with --spring.profiles.active=trap or =fix. No web server: it places one order and exits. */
@SpringBootApplication
public class TrapApp {

    public static void main(String[] args) {
        SpringApplication.run(TrapApp.class, args);
    }
}
