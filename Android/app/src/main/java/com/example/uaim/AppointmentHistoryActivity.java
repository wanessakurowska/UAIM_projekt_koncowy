package com.example.uaim;

import android.os.Bundle;
import android.util.Log;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;

public class AppointmentHistoryActivity extends AppCompatActivity {
    private static final String APPOINTMENTS_URL = "http://10.0.2.2:5000/client-appointments";
    private ListView listView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.list_view);

        listView = findViewById(R.id.ListView);


        fetchCompletedAppointments();
    }

    private void fetchCompletedAppointments() {
        String token = MySingleton.getInstance(AppointmentHistoryActivity.this).getAuthToken();

        if (token == null) {
            Toast.makeText(AppointmentHistoryActivity.this, "User not logged in", Toast.LENGTH_SHORT).show();
            return;
        }

        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(Request.Method.GET, APPOINTMENTS_URL, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        ArrayList<Appointment> appointmentList = new ArrayList<>();

                        try {
                            for (int i = 0; i < response.length(); i++) {
                                JSONObject appointmentObject = response.getJSONObject(i);

                                String idW = appointmentObject.getString("id_wizyty");
                                String date = appointmentObject.getString("data_wizyty");
                                String time = appointmentObject.getString("godzina_wizyty_od");
                                String petName = appointmentObject.getString("imie_pupila");


                                Appointment appointment = new Appointment(idW, date, time, "", "", "", petName);
                                appointmentList.add(appointment);
                            }


                            AppointmentHistoryAdapter adapter = new AppointmentHistoryAdapter(AppointmentHistoryActivity.this, appointmentList);
                            listView.setAdapter(adapter);

                        } catch (Exception e) {
                            Log.e("AppointmentHistory", "Error parsing appointments data", e);
                            Toast.makeText(AppointmentHistoryActivity.this, "Failed to load appointments", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e("AppointmentHistory", "Error fetching appointments", error);
                        Toast.makeText(AppointmentHistoryActivity.this, "Error fetching appointments", Toast.LENGTH_SHORT).show();
                    }
                }) {
            @Override
            public java.util.Map<String, String> getHeaders() {
                java.util.Map<String, String> headers = new java.util.HashMap<>();
                headers.put("Authorization", "Bearer " + token);
                return headers;
            }
        };

        MySingleton.getInstance(this).addToRequestQueue(jsonArrayRequest);
    }
}
