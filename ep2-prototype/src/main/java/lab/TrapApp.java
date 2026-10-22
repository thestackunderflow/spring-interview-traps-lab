package lab;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/** Episode 2: run with --spring.profiles.active=trap or =fix. No web server: three calls, then it exits. */
@SpringBootApplication
public class TrapApp {

    public static void main(String[] args) {
        SpringApplication.run(TrapApp.class, args);
    }
}
