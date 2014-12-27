package id.web.wirama.fpsensor;

import android.app.Activity;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.StrictMode;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import android.os.Handler;


public class MainActivity extends ActionBarActivity {

    private DatagramSocket sock;

    Double lightIntensity = -100.0;
    Double temperature = -100.0;
    Double humidity = -100.0;
    String broadcastAddress = "192.168.43.255";
    int broadcastPort = 5000;

    TextView tvLightIntensity, tvTemperature, tvHumidity;
    EditText etBroadcastAddress;

    DatagramSocket s = null;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        super.onCreate(savedInstanceState);
        final Handler handler = new Handler();
        setContentView(R.layout.activity_main);


        try {
            s = new DatagramSocket(broadcastPort);
            s.setBroadcast(true);

            // Thread
            final Runnable threadSender = new Runnable() {

                @Override
                public void run() {
                    Log.d("threadSender", "threadSender Starting...");
                    //while(true) {
                        Log.d("threadSender", "Do sending data...");
                        try {
                            InetAddress bcast = InetAddress.getByName(broadcastAddress);

                            // Create message

                            JSONObject json = new JSONObject();
                            json.put("lightIntensity", lightIntensity);
                            json.put("source", "android");
                            json.put("temperature", temperature);
                            json.put("humidity", humidity);

                            String data = json.toString();

                            byte[] message = data.getBytes();
                            DatagramPacket p = new DatagramPacket(message, data.length(), bcast, broadcastPort);
                            Log.d("threadSender", "Data sent " + data);
                            s.send(p);
                            handler.postDelayed(this, 5000);

                        } catch (SocketException e) {
                            e.printStackTrace();
                        } catch (UnknownHostException e) {
                            e.printStackTrace();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }



                //}
            };

            final Runnable threadReceiver = new Runnable() {

                @Override
                public void run() {
                    Log.d("threadReceiver", "threadReceiver Starting...");
                    //while(true) {
                        Log.d("threadReceiver", "Do receiving data...");
                        try {
                            byte[] buf = new byte[1024];
                            DatagramPacket p = new DatagramPacket(buf, buf.length);
                            s.receive(p);

                            String data = new String(p.getData(), 0, p.getLength());

                            Log.d("threadReceiver", "Data received: " + data);


                            JSONObject json = new JSONObject(data);

                            // Set temperature and humidity
                            temperature = Double.parseDouble(json.getString("temperature"));
                            humidity = Double.parseDouble(json.getString("humidity"));


                            tvTemperature.setText(temperature.toString());
                            tvHumidity.setText(humidity.toString());

                            handler.postDelayed(this, 5000);




                        } catch (SocketException e) {
                            e.printStackTrace();
                        } catch (IOException e) {
                            e.printStackTrace();
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }



                //}
            };




            // Activity's element
            tvLightIntensity = (TextView) findViewById(R.id.lightIntensity);
            tvTemperature = (TextView) findViewById(R.id.temperature);
            tvHumidity = (TextView) findViewById(R.id.humidity);
            etBroadcastAddress = (EditText) findViewById(R.id.alamatBroadcast);

            final Button changeBcast = (Button) findViewById(R.id.ubahBcast);
            changeBcast.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    broadcastAddress = etBroadcastAddress.getText().toString();
                    etBroadcastAddress.setFocusable(false);
                    changeBcast.setClickable(false);


                    // Also run the thread

                    handler.postDelayed(threadReceiver, 5000);
                    handler.postDelayed(threadSender, 5000);
                }
            });

            SensorManager sensorManager = (SensorManager) this.getSystemService(SENSOR_SERVICE);
            Sensor lightSensor = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);

            // Sensor reader
            if(lightSensor == null) {
                Toast.makeText(MainActivity.this, "Tidak ada sensor cahaya", Toast.LENGTH_LONG).show();

            } else {
                sensorManager.registerListener(new SensorEventListener() {

                    @Override
                    public void onSensorChanged(SensorEvent event) {
                        if(event.sensor.getType() == Sensor.TYPE_LIGHT) {
                            lightIntensity = (double) event.values[0];
                            tvLightIntensity.setText(lightIntensity.toString());
                        }
                    }

                    @Override
                    public void onAccuracyChanged(Sensor sensor, int accuracy) {

                    }

                }, lightSensor, SensorManager.SENSOR_DELAY_NORMAL);
            }

            // Data sender


        } catch (SocketException e) {
            e.printStackTrace();
        }





    }



}
