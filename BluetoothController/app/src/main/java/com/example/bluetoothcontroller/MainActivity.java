package com.example.bluetoothcontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.os.Handler;
import android.widget.Button;

public class MainActivity extends AppCompatActivity {

    private BluetoothController btController;
    private static final String MOVE_FORWARD = "moveForward";
    private static final String STOP_MOVE_FORWARD = "stopMoveForward";
    private static final String MOVE_BACKWARD = "moveBackward";
    private static final String STOP_MOVE_BACKWARD = "stopMoveBackward";
    private static final String TURN_LEFT = "turnLeft";
    private static final String STOP_TURN_LEFT = "stopTurnLeft";
    private static final String TURN_RIGHT = "turnRight";
    private static final String STOP_TURN_RIGHT = "stopTurnRight";

    private Button forwardButton;
    private Button backwardButton;
    private Button leftButton;
    private Button rightButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        Handler handler = new Handler();
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        btController = new BluetoothController(this, handler);
        btController.startBluetooth();

        forwardButton = (Button) findViewById(R.id.forwardbutton);
        backwardButton = (Button) findViewById(R.id.backwardbutton);
        leftButton = (Button) findViewById(R.id.leftbutton);
        rightButton = (Button) findViewById(R.id.rightbutton);

        forwardButton.setOnTouchListener(new View.OnTouchListener(){
            @Override
            public boolean onTouch(View view, MotionEvent event){
                switch (event.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        btController.write(MOVE_FORWARD.getBytes());
                        return true;
                    case MotionEvent.ACTION_UP:
                        btController.write(STOP_MOVE_FORWARD.getBytes());
                        return true;
                    default:
                        return false;
                }
            }
        });

        backwardButton.setOnTouchListener(new View.OnTouchListener(){
            @Override
            public boolean onTouch(View view, MotionEvent event){
                switch (event.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        btController.write(MOVE_BACKWARD.getBytes());
                        return true;
                    case MotionEvent.ACTION_UP:
                        btController.write(STOP_MOVE_BACKWARD.getBytes());
                        return true;
                    default:
                        return false;
                }
            }
        });

        leftButton.setOnTouchListener(new View.OnTouchListener(){
            @Override
            public boolean onTouch(View view, MotionEvent event){
                switch (event.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        btController.write(TURN_LEFT.getBytes());
                        return true;
                    case MotionEvent.ACTION_UP:
                        btController.write(STOP_TURN_LEFT.getBytes());
                        return true;
                    default:
                        return false;
                }
            }
        });

        rightButton.setOnTouchListener(new View.OnTouchListener(){
            @Override
            public boolean onTouch(View view, MotionEvent event){
                switch (event.getAction()){
                    case MotionEvent.ACTION_DOWN:
                        btController.write(TURN_RIGHT.getBytes());
                        return true;
                    case MotionEvent.ACTION_UP:
                        btController.write(STOP_TURN_RIGHT.getBytes());
                        return true;
                    default:
                        return false;
                }
            }
        });
    }
}
