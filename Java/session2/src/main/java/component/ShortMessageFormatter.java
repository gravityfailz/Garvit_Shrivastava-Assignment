package session2.src.main.java.component;

import org.springframework.stereotype.Component;

@Component("shortFormatter")
public class ShortMessageFormatter implements MessageFormatter {

    public String format() {
        return "Short Message";
    }
}
