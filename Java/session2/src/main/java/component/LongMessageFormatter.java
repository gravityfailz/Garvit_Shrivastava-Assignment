package session2.src.main.java.component;

import org.springframework.stereotype.Component;

@Component("longFormatter")
public class LongMessageFormatter implements MessageFormatter {

    public String format() {
        return "This is a long detailed message";
    }
}