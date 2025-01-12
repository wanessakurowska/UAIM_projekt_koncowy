package com.example.uaim;

import android.app.AlertDialog;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class DetailsActivity extends AppCompatActivity {

    private TextView textViewIDW, textViewData, textViewTime, textViewImiePupila, textViewIDS,
            textViewNU, textViewOU, textViewCU, textViewIDWet, textViewNazWet,
            textViewImieWet;
    private Button buttonCancel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.appo_details_view);


        textViewIDW = findViewById(R.id.textViewIDW);
        textViewData = findViewById(R.id.textViewData);
        textViewTime = findViewById(R.id.textViewTime);
        textViewImiePupila = findViewById(R.id.textViewImiePupila);

        textViewNU = findViewById(R.id.textViewNU);
        textViewOU = findViewById(R.id.textViewOU);
        textViewCU = findViewById(R.id.textViewCU);

        textViewNazWet = findViewById(R.id.textViewNazWet);

        buttonCancel = findViewById(R.id.buttonODW);


        String appointmentIdStr = getIntent().getStringExtra("appointmentId");
        String petName = getIntent().getStringExtra("PetName");
        int appointmentId = (appointmentIdStr != null) ? Integer.parseInt(appointmentIdStr) : -1;
        Log.d("DetailsActivity", "Received appointmentId: " + appointmentId + ", petName: " + petName);


        if (petName != null) {
            _get_pet_id_by_name(petName, new PetIdCallback() {
                @Override
                public void onPetIdFetched(int petId) {
                    if (petId != -1) {
                        fetchAppointmentDetails(petId, appointmentId);
                    } else {
                        Toast.makeText(DetailsActivity.this, "Pet not found", Toast.LENGTH_SHORT).show();
                    }
                }
            });
        }

        buttonCancel.setOnClickListener(v -> {
            new AlertDialog.Builder(this)
                    .setTitle("Confirm deleting the appointment")
                    .setMessage("Do you want to cancel the appointment " + appointmentId + "?")
                    .setPositiveButton("Yes", (dialog, which) -> {
                        String urlC = "http://10.0.2.2:5000/api/cancel-appointment/" + appointmentId;
                        String tokenC = MySingleton.getInstance(DetailsActivity.this).getAuthToken();

                        if (tokenC == null) {
                            Toast.makeText(DetailsActivity.this, "User not logged in", Toast.LENGTH_SHORT).show();
                            return;
                        }

                        RequestQueue requestQueue = MySingleton.getInstance(DetailsActivity.this).getRequestQueue();

                        StringRequest stringRequest = new StringRequest(Request.Method.DELETE, urlC,
                                response -> {

                                    Toast.makeText(DetailsActivity.this, "Appointment cancelled successfully", Toast.LENGTH_SHORT).show();
                                },
                                error -> {

                                    String errorMessage = "An error occurred";
                                    if (error.networkResponse != null) {
                                        if (error.networkResponse.statusCode == 404) {
                                            errorMessage = "Appointment not found";
                                        } else if (error.networkResponse.statusCode == 403) {
                                            errorMessage = "You don't have permission to cancel this appointment";
                                        } else if (error.networkResponse.statusCode == 500) {
                                            errorMessage = "Internal server error";
                                        }
                                    }
                                    Toast.makeText(DetailsActivity.this, errorMessage, Toast.LENGTH_SHORT).show();
                                }) {
                            @Override
                            public Map<String, String> getHeaders() throws AuthFailureError {
                                Map<String, String> headers = new HashMap<>();
                                headers.put("Authorization", "Bearer " + tokenC);
                                return headers;
                            }
                        };

                        requestQueue.add(stringRequest);
                    })
                    .setNegativeButton("No", null)
                    .show();
        });
    }


    public interface PetIdCallback {
        void onPetIdFetched(int petId);
    }

    private void _get_pet_id_by_name(String petName, final PetIdCallback callback) {
        String url = "http://10.0.2.2:5000/api/my-pets";
        String token = MySingleton.getInstance(DetailsActivity.this).getAuthToken();

        if (token == null) {
            Toast.makeText(DetailsActivity.this, "User not logged in", Toast.LENGTH_SHORT).show();
            callback.onPetIdFetched(-1); // Return -1 for failure if no token
            return;
        }


        JsonArrayRequest request = new JsonArrayRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {
                            int petId = -1;

                            for (int i = 0; i < response.length(); i++) {
                                JSONObject pet = response.getJSONObject(i);
                                if (pet.getString("imie").equalsIgnoreCase(petName)) {
                                    petId = pet.getInt("id_pupila");
                                    break;
                                }
                            }
                            callback.onPetIdFetched(petId);
                        } catch (JSONException e) {
                            e.printStackTrace();
                            callback.onPetIdFetched(-1);
                        }
                    }
                },
                error -> {
                    error.printStackTrace();
                    callback.onPetIdFetched(-1);
                }) {
            @Override
            public Map<String, String> getHeaders() {
                Map<String, String> headers = new HashMap<>();
                headers.put("Authorization", "Bearer " + token);
                return headers;
            }
        };

        Volley.newRequestQueue(this).add(request);
    }

    private void fetchAppointmentDetails(int petId, int appointmentId) {
        String url = "http://10.0.2.2:5000/appointment-list?id_pupila=" + petId;
        String token = MySingleton.getInstance(DetailsActivity.this).getAuthToken();

        if (token == null) {
            Toast.makeText(DetailsActivity.this, "User not logged in", Toast.LENGTH_SHORT).show();
            return;
        }

        JsonArrayRequest request = new JsonArrayRequest(Request.Method.GET, url, null,
                response -> {
                    try {
                        boolean appointmentFound = false;

                        for (int i = 0; i < response.length(); i++) {
                            JSONObject appointment = response.getJSONObject(i);

                            if (appointment.getInt("id_wizyty") == appointmentId) {
                                appointmentFound = true;


                                textViewIDW.setText("ID Wizyty: " + appointment.getString("id_wizyty"));
                                textViewData.setText(appointment.getString("data_wizyty"));
                                textViewTime.setText(appointment.getString("godzina_wizyty"));

                                JSONObject pet = appointment.getJSONObject("pupil");
                                textViewImiePupila.setText(pet.getString("imie"));
                                textViewNU.setText(pet.getString("rasa"));
                                textViewCU.setText(String.valueOf(pet.getInt("wiek")));

                                JSONObject service = appointment.getJSONObject("usluga");
                                textViewNU.setText(service.getString("nazwa"));
                                textViewOU.setText(service.getString("opis"));
                                textViewCU.setText("Koszt: " + String.valueOf(service.getDouble("cena")));

                                textViewNazWet.setText("Lekarz: " + appointment.getString("lekarz"));
                                break;
                            }
                        }

                        if (!appointmentFound) {
                            Toast.makeText(DetailsActivity.this, "Appointment not found", Toast.LENGTH_SHORT).show();
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                        Toast.makeText(DetailsActivity.this, "Error parsing appointment details", Toast.LENGTH_SHORT).show();
                    }
                },
                error -> {
                    error.printStackTrace();
                    Toast.makeText(DetailsActivity.this, "Error fetching appointment details", Toast.LENGTH_SHORT).show();
                }) {
            @Override
            public Map<String, String> getHeaders() {
                Map<String, String> headers = new HashMap<>();
                headers.put("Authorization", "Bearer " + token);
                return headers;
            }
        };

        Volley.newRequestQueue(this).add(request);
    }


}
