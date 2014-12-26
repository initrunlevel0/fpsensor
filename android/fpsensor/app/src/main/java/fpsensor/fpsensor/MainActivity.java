package fpsensor.fpsensor;

import android.net.DhcpInfo;
import android.net.wifi.WifiManager;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.os.AsyncTask;
import android.view.Menu;
import android.view.MenuItem;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.widget.TextView;
import android.os.Handler;

import java.io.IOException;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;


public class MainActivity extends ActionBarActivity {

    TextView intensity;

    private Handler handler = new Handler();
    private Thread thread;

    private DatagramSocket s;

    private double temperature = -100;
    private double currentReading = -100;
    private double humidity = -100;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        intensity = (TextView)findViewById(R.id.intensity);
        SensorManager sensorManager = (SensorManager)getSystemService(Context.SENSOR_SERVICE);
        Sensor lightSensor = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
        sensorManager.registerListener(lightSensorEventListener,
                lightSensor,
                SensorManager.SENSOR_DELAY_NORMAL);

        intensity.setText(String.valueOf(currentReading));

        // Socket
        try {
            s = new DatagramSocket(5000);
        } catch (SocketException e) {
            e.printStackTrace();
        }

        thread = new Thread() {
            public void run() {

                try {
                    s.setBroadcast(true);
                    while(true) {
                        // Packet sender

                    }

                } catch (SocketException e) {
                    e.printStackTrace();
                }


            }
        };

    }





    SensorEventListener lightSensorEventListener
            = new SensorEventListener(){

        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
            // TODO Auto-generated method stub

        }

        @Override
        public void onSensorChanged(SensorEvent event) {
            // TODO Auto-generated method stub
            if(event.sensor.getType()==Sensor.TYPE_LIGHT){
                currentReading = event.values[0];
                intensity.setText(String.valueOf(currentReading));
            }
        }

    };


}
