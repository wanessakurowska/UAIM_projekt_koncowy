package com.example.uaim;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.CalendarView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import org.json.JSONArray;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import android.app.AlertDialog;
import android.widget.Toast;

public class CalendarActivity extends AppCompatActivity {

    private int vetID;
    private CalendarView calendarView;
    private RecyclerView recyclerViewSlots;
    private SlotAdapter slotAdapter;
    private String selectedDateFinal;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_calendar);

        calendarView = findViewById(R.id.calendarView);
        recyclerViewSlots = findViewById(R.id.recyclerViewSlots);


        slotAdapter = new SlotAdapter(slotTime -> onSlotSelected(slotTime));
        recyclerViewSlots.setLayoutManager(new LinearLayoutManager(this));
        recyclerViewSlots.setAdapter(slotAdapter);

        vetID = getIntent().getIntExtra("vetID", -1);
        if (vetID == -1) {
            Toast.makeText(this, "Invalid vet ID", Toast.LENGTH_SHORT).show();
            return;
        }

        calendarView.setOnDateChangeListener((view, year, month, dayOfMonth) -> {
            String selectedDate = String.format("%d-%02d-%02d", year, month + 1, dayOfMonth);
            selectedDateFinal = selectedDate;
            try {
                getAvailableSlots(selectedDate);
            } catch (ParseException e) {
                throw new RuntimeException(e);
            }
        });
    }

    private void getAvailableSlots(String selectedDate) throws ParseException {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        Date date = dateFormat.parse(selectedDate);

        Calendar calendar = Calendar.getInstance();
        calendar.setTime(date);
        calendar.add(Calendar.DAY_OF_MONTH, 1);
        String newSelectedDate = dateFormat.format(calendar.getTime());

        HashMap<String, String> params = new HashMap<>();
        params.put("date_from", selectedDate);
        params.put("date_to", newSelectedDate);
        params.put("id_weterynarza", String.valueOf(vetID));

        String apiUrl = "http://10.0.2.2:5000/api/available-slots";

        new Thread(() -> {
            try {
                String response = makeApiRequest(apiUrl, params);
                runOnUiThread(() -> {
                    try {
                        JSONArray slots = new JSONArray(response);
                        slotAdapter.updateSlots(slots);
                    } catch (Exception e) {
                        e.printStackTrace();
                        Toast.makeText(CalendarActivity.this, "Error parsing response", Toast.LENGTH_SHORT).show();
                    }
                });
            } catch (Exception e) {
                runOnUiThread(() -> Toast.makeText(CalendarActivity.this, "Error: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }
        }).start();
    }

    private String makeApiRequest(String url, HashMap<String, String> params) {
        StringBuilder urlWithParams = new StringBuilder(url);
        if (params != null && !params.isEmpty()) {
            urlWithParams.append("?");
            Iterator<HashMap.Entry<String, String>> iterator = params.entrySet().iterator();
            while (iterator.hasNext()) {
                HashMap.Entry<String, String> entry = iterator.next();
                urlWithParams.append(entry.getKey()).append("=").append(entry.getValue());
                if (iterator.hasNext()) {
                    urlWithParams.append("&");
                }
            }
        }

        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url(urlWithParams.toString())
                .build();

        try {
            Response response = client.newCall(request).execute();
            if (response.isSuccessful()) {
                return response.body().string();
            } else {
                return "{\"error\": \"Failed to retrieve slots\"}";
            }
        } catch (Exception e) {
            e.printStackTrace();
            return "{\"error\": \"Request failed: " + e.getMessage() + "\"}";
        }
    }

    private void onSlotSelected(String slotTime) {

        if (vetID == -1 || slotTime == null || slotTime.isEmpty()) {
            Toast.makeText(this, "Invalid data. Cannot proceed to book appointment.", Toast.LENGTH_SHORT).show();
            Log.e("onSlotSelected", "Invalid vetID: " + vetID + " or slotTime: " + slotTime);
            return;
        }


        Log.d("onSlotSelected", "vetID: " + vetID + ", slotTime: " + slotTime);


        new AlertDialog.Builder(this)
                .setTitle("Confirm Appointment")
                .setMessage("Do you want to book an appointment for " + slotTime + "?")
                .setPositiveButton("Yes", (dialog, which) -> {

                    Intent intent = new Intent(CalendarActivity.this, AppointmentActivity.class);
                    intent.putExtra("vetID", vetID);
                    intent.putExtra("appointmentDateTime", slotTime);
                    intent.putExtra("appointmentDate", selectedDateFinal);


                    Log.d("onSlotSelected", "Starting AppointmentActivity with vetID: " + vetID + ", appointmentDateTime: " + slotTime + "selectedDate:" + selectedDateFinal);

                    startActivity(intent);
                })
                .setNegativeButton("No", null)
                .show();
    }




}
