package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.app.Activity;
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

        ipAddress = "192.168.43.18";
        port = 10000;

        getDataBtn = (Button) findViewById(R.id.getData);
        resultPanel = (ConstraintLayout) findViewById(R.id.resultPanel);
        tempValue = (TextView) findViewById(R.id.tempValue);
        lumValue = (TextView) findViewById(R.id.lumValue);

        resultPanel.setVisibility(View.INVISIBLE);
        (new ReceiverTask()).execute();

        getDataBtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                (new Thread() {
                    public void run() {
                        try {
                            String test = "LT";
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
            }
        });
    }

    class ReceiverTask extends AsyncTask<String, Void, Void>{
        @Override
        protected Void doInBackground(String... arg0) {
            try {
                DatagramSocket UDPSocket = new DatagramSocket(port);
                while(true){
                    byte[] data = new byte [1024]; // Espace de réception des données.
                    DatagramPacket packet = new DatagramPacket(data, data.length);
                    UDPSocket.receive(packet);
                    String str = new String(packet.getData());
                    System.out.println("str : " + str);
                    resultPanel.setVisibility(View.VISIBLE);
                }
            } catch (SocketException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }
        @Override
        protected void onPostExecute(Void result) {
            super.onPostExecute(result);
        }
    }
}
