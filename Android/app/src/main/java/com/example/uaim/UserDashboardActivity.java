package com.example.uaim;



import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class UserDashboardActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logged);
        Button logoutButton = findViewById(R.id.buttonLog);

        logoutButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(UserDashboardActivity.this, MainActivity.class);
                startActivity(intent);
                finish();
            }
        });

        Button buttonUW = findViewById(R.id.buttonUW);


        buttonUW.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // Intent to start AppointmentActivity for scheduling the appointment
                Intent intent = new Intent(UserDashboardActivity.this, ChooseVetActivity.class);
                startActivity(intent);
            }
        });


        Button buttonVets = findViewById(R.id.buttonVets);


        buttonVets.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent intent = new Intent(UserDashboardActivity.this, VetsActivity.class);
                startActivity(intent);
            }
        });

        Button buttonHistWiz = findViewById(R.id.buttonHistWiz);


        buttonHistWiz.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                Intent intent = new Intent(UserDashboardActivity.this, AppointmentHistoryActivity.class);
                startActivity(intent);
            }
        });

        Button buttonHZW = findViewById(R.id.buttonHZW);
        buttonHZW.setOnClickListener(v -> {
            Intent intent = new Intent(UserDashboardActivity.this, PupilsActivity.class);
            startActivity(intent);
        });

        Button buttonDpup = findViewById(R.id.buttonDpup);

        buttonDpup.setOnClickListener(v -> {
            Intent intent = new Intent(UserDashboardActivity.this, AddPupilActivity.class);
            startActivity(intent);
        });
    }

}
