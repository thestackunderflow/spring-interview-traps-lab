package lab;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/** Episode 3: run with --spring.profiles.active=trap or =fix. No web server: it compares two references and exits. */
@SpringBootApplication
public class TrapApp {

    public static void main(String[] args) {
        SpringApplication.run(TrapApp.class, args);
    }
}
