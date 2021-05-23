package com.example.raco;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class Comm extends AppCompatActivity {
    public String message;
    public String m1;
    public String m2;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_comm);
        final EditText inputtext1 = (EditText) findViewById(R.id.editText);
        final EditText inputtext2 = (EditText) findViewById(R.id.editText2);
        final Button clickable = (Button) findViewById(R.id.button2);
        clickable.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                send sendcode = new send();
                m1 = inputtext1.getText().toString();
                m2 = inputtext2.getText().toString();
                message = m1+':'+m2;
                sendcode.execute();
            }
        });
    }

    class send extends AsyncTask<Void,Void,Void> {
        Socket s;
        PrintWriter pw;
        @Override
        protected Void doInBackground(Void...params){
            try {
                s = new Socket("10.0.2.2",808);
                pw = new PrintWriter(s.getOutputStream());
                pw.write(message);
                pw.flush();
                pw.close();
                s.close();
            } catch (UnknownHostException e) {
                System.out.println("Fail");
                e.printStackTrace();
            } catch (IOException e) {
                System.out.println("Fail");
                e.printStackTrace();
            }
            return null;
        }
    }
}