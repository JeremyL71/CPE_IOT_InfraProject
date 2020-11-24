package com.example.myapplication;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import com.example.myapplication.model.AppData;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Arrays;

public class MainActivity extends AppCompatActivity {

    private Button toggleFormatbtn;
    private Button askValuesBtn;
    private ConstraintLayout resultPanel;
    private TextView temperatureValue;
    private TextView luminositeValue;

    private String ipAddress;
    private int portServer;

    private String[] formatValues;
    private int currentValue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ipAddress = "172.20.10.2";
        portServer = 56000;

        formatValues = new String[]{"LT", "TL"};
        currentValue = 0;

        toggleFormatbtn = (Button) findViewById(R.id.toggle_format);
        askValuesBtn = (Button) findViewById(R.id.ask_values);
        resultPanel = (ConstraintLayout) findViewById(R.id.resultPanel);
        temperatureValue = (TextView) findViewById(R.id.temperature_value);
        luminositeValue = (TextView) findViewById(R.id.luminosite_value);

        resultPanel.setVisibility(View.INVISIBLE);

        askValuesBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                (new GetDataTask()).execute();
            }
        });

        toggleFormatbtn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                currentValue = (currentValue + 1) % formatValues.length;
                sendFormatValue();
            }
        });

        sendFormatValue();
        (new GetDataTask()).execute();
    }

    public void sendFormatValue() {
        (new Thread() {
            public void run() {
                try {
                    String content = formatValues[currentValue];
                    byte[] data = content.getBytes();
                    DatagramSocket UDPSocket = new DatagramSocket();
                    InetAddress address = InetAddress.getByName(ipAddress);
                    DatagramPacket packet = new DatagramPacket(data, data.length, address, portServer);
                    UDPSocket.send(packet);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    class GetDataTask extends AsyncTask<Void, AppData, Void>{

        @Override
        protected Void doInBackground(Void... voids) {
            try {
                // Envoie de la demande de valeurs
                String content = "getValues()";
                byte[] dataSend = content.getBytes();
                DatagramSocket UDPSocket = new DatagramSocket();
                InetAddress address = InetAddress.getByName(ipAddress);
                DatagramPacket packetSend = new DatagramPacket(dataSend, dataSend.length, address, portServer);
                UDPSocket.send(packetSend);

                // Récupération des dernières valeurs
                byte[] dataReceive = new byte[1024];
                DatagramPacket packetReceive = new DatagramPacket(dataReceive, dataReceive.length, address, portServer);
                UDPSocket.receive(packetReceive);
                String contentReceive = new String(Arrays.copyOfRange(packetReceive.getData(), 0, packetReceive.getLength()));
                System.out.println("[+] " + contentReceive);
                int temperature = Integer.parseInt(contentReceive.split(" ")[0]);
                int luminosite = Integer.parseInt(contentReceive.split(" ")[1]);
                publishProgress(new AppData(temperature, luminosite));
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }

        protected void onProgressUpdate(AppData... appDatas) {
            updatedatas(appDatas[0]);
        }

    }

    public void updatedatas(AppData appData) {
        resultPanel.setVisibility(View.VISIBLE);
        temperatureValue.setText(String.valueOf(appData.getTemperature()));
        luminositeValue.setText(String.valueOf(appData.getLuminosite()));
    }
}
