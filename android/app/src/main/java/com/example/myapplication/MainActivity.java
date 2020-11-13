package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;

public class MainActivity extends AppCompatActivity {

    private Button getDataBtn;
    private ConstraintLayout resultPanel;
    private TextView tempValue;
    private TextView lumValue;

    private String ipAddress;
    private int port;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ipAddress = "82.67.78.62";
        port = 4444;

        getDataBtn = (Button) findViewById(R.id.getData);
        resultPanel = (ConstraintLayout) findViewById(R.id.resultPanel);
        tempValue = (TextView) findViewById(R.id.tempValue);
        lumValue = (TextView) findViewById(R.id.lumValue);

        resultPanel.setVisibility(View.INVISIBLE);

        getDataBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                getData();
            }
        });
    }

    public void getData() {
        (new Thread() {
            public void run() {
                try {
                    String test = "hello";
                    byte[] data = test.getBytes();
                    DatagramSocket UDPSocket = new DatagramSocket();
                    InetAddress address = InetAddress.getByName(ipAddress);
                    DatagramPacket packet = new DatagramPacket(data, data.length, address, port);
                    UDPSocket.send(packet);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();

        (new Thread() {
            public void run() {
                try {
                    DatagramSocket server = new DatagramSocket(port);

                    while(true) {
                        byte[] buffer = new byte[8192];
                        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);

                        server.receive(packet);

                        String str = new String(packet.getData());
                        packet.setLength(buffer.length);
                        System.out.println(str);
                        resultPanel.setVisibility(View.VISIBLE);
                    }
                } catch (SocketException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }
}