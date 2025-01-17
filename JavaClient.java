import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

public class JavaClient {
    public static void main(String[] args) {
        // Create a new instance of JFrame and Button
        JFrame frame = new JFrame("Python Script Runner");
        JButton button = new JButton("Run app.py");

        // Add the button to the JFrame
        frame.add(button);

        // Make the JFrame visible
        frame.setSize(200, 100);
        frame.setVisible(true);   
    }
}

// Reference - https://docs.oracle.com/javase/tutorial/uiswing/start/compile.html
