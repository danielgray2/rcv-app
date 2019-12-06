package com.example.bluetoothcontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    /* Daniel Gray 12/5/19
    * This activity defines and handles all of the inputs
    * into the main portion of the application
    * */

    private static final String UPDATE_SPEED = "s";
    private static final String UPDATE_DIRECTION = "d";
    private static final String READY_FOR_UPDATE = "rfu";
    private BluetoothController btController;

    private SeekBar speedController;
    private SeekBar turnController;
    private Button stopButton;
    private Button trimButton;
    private Button connectButton;
    private BluetoothService btService;
    private Boolean serviceBound = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        /*
        * This method is called when the application is created.
         */
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        turnController = (SeekBar) findViewById(R.id.turnController);
        speedController = (SeekBar) findViewById(R.id.speedController);
        stopButton = (Button) findViewById(R.id.stop_button);
        trimButton = (Button) findViewById(R.id.trimButton);
        connectButton = (Button) findViewById(R.id.connectButton);

        // This controls the turning and sends that information to the BluetoothService
        turnController.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                JSONObject messageObject = new JSONObject();
                Integer trim = 0;
                try {
                    if(btService.getReceivedMessage().equals(READY_FOR_UPDATE)) {
                        int valueToSend = progress + trim;
                        System.out.println("Sending dude: " + valueToSend);
                        messageObject.put("e", UPDATE_DIRECTION);
                        messageObject.put("v", progress);
                        btController.write(messageObject.toString().getBytes());
                    }
                } catch (JSONException e){
                    System.out.println("There was an issue creating the JSON message object");
                }
                try{
                    Thread.sleep(0);
                }
                catch (InterruptedException e){
                    System.out.println("There was an interrupted exception");
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });

        // This controls the speed and sends that information to the BluetoothService
        speedController.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                System.out.println("Here is the boolean: " + serviceBound);
                JSONObject messageObject = new JSONObject();
                try {
                    if(btService.getReceivedMessage().equals(READY_FOR_UPDATE)) {
                        messageObject.put("e", UPDATE_SPEED);
                        messageObject.put("v", progress);
                        btController.write(messageObject.toString().getBytes());
                    }
                } catch (JSONException e) {
                    System.out.println("There was an issue creating the JSON message object");
                }
                try{
                    Thread.sleep(0);
                }
                catch (InterruptedException e){
                    System.out.println("There was an interrupted exception");
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {}

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {}
        });

        // This defines the break button
        stopButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch(event.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        speedController.setProgress(50);
                }
                return false;
            }
        });

        // This button opens the trim menu
        trimButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch(event.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        openSetTrim();
                }
                return false;
            }
        });

        // This defines the connect button
        connectButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch(event.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        btController.startBluetooth();
                }
                return false;
            }
        });
    }

    // This opens the trim settings
    public void openSetTrim(){
        Intent intent = new Intent(this, SetTrim.class);
        startActivity(intent);
    }

    // This creates a connection service between the phone and the
    // controller.
    private ServiceConnection connection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName className, IBinder service) {
            // We've bound to LocalService, cast the IBinder and get LocalService instance
            BluetoothService.LocalBinder binder = (BluetoothService.LocalBinder) service;
            btService = binder.getService();
            btController = btService.getBtController();
            serviceBound = true;
        }

        @Override
        public void onServiceDisconnected(ComponentName arg0) {
            serviceBound = false;
        }
    };

    // This binds to the bluetooth controller
    @Override
    protected void onStart() {
        super.onStart();
        // Bind to LocalService
        Intent intent = new Intent(this, BluetoothService.class);
        startService(intent);
        bindService(intent, connection, Context.BIND_AUTO_CREATE);
    }

    // This handles disconnecting from the controller
    @Override
    protected void onStop() {
        super.onStop();
        unbindService(connection);
        serviceBound = false;
    }

}