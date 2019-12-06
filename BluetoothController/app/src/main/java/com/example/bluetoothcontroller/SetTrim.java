package com.example.bluetoothcontroller;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

/*
* This class sets the trim for the vehicle. This
* helps to correct for any mistakes in the
* engineering.
 */
public class SetTrim extends AppCompatActivity {

    private Button trimButton;
    private Integer trimValue = 0;
    private EditText trimText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_set_trim);

        trimText = (EditText) findViewById(R.id.trimValue);
        trimButton = (Button) findViewById(R.id.trimButton);

        // When fired, this gets the text value and sets the
        // trim
       trimButton.setOnTouchListener(new View.OnTouchListener() {
           @Override
           public boolean onTouch(View v, MotionEvent event) {
               switch(event.getAction()) {
                   case MotionEvent.ACTION_UP:
                       trimValue = Integer.parseInt(trimText.getText().toString());
                       Intent intent = new Intent(SetTrim.this, MainActivity.class);
                       intent.putExtra("trimValue", trimValue.toString());
                       startActivity(intent);
                       return true;
               }
               return false;
           }
       });
    }
}
