package com.example.bluetoothcontroller;

import android.app.Activity;
import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.os.Handler;
import android.os.Message;

import androidx.annotation.Nullable;

/*
 * This service is used to reconnect to the vehicle
 */
public class BluetoothService extends Service {
    private final  IBinder binder = new LocalBinder();
    private String receivedMessage = null;
    private BluetoothController btController;
    private Activity activity = new Activity();

    public class LocalBinder extends Binder{
        BluetoothService getService(){
            return BluetoothService.this;
        }
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        Handler handler = new Handler(new Handler.Callback() {
            @Override
            public boolean handleMessage(Message msg) {
                switch (msg.what) {
                    case 0:
                        byte[] readBuff = (byte[]) msg.obj;
                        receivedMessage = new String(readBuff, 0, msg.arg1);
                        break;
                }
                return true;
            }
        });
        btController = new BluetoothController(activity, handler);
        btController.startBluetooth();
        return binder;
    }

    // This method gets a bluetooth controller
    // to connect with
    public BluetoothController getBtController(){
        return this.btController;
    }

    // This method returns a message to the caller
    // and sets the receivedMessage variable
    // to be empty
    public String getReceivedMessage(){
        String returnMessage = receivedMessage;
        receivedMessage = "";
        return returnMessage;
    }
}