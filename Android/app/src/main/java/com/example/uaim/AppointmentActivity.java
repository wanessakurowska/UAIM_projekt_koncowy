package com.example.uaim;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

public class AppointmentActivity extends AppCompatActivity {

    private static final String BOOK_APPOINTMENT_URL = "http://10.0.2.2:5000/api/book-appointment";
    private static final String SERVICE_LIST_URL = "http://10.0.2.2:5000/service-list";
    private static final String MY_PETS_URL = "http://10.0.2.2:5000/api/my-pets";
    private static final String AVAILABLE_SLOTS_URL = "http://10.0.2.2:5000/api/available-slots";
    private static final String VET_LIST_URL = "http://10.0.2.2:5000/veterinarian-list";
    private ArrayList<SpinnerItem> serviceItems = new ArrayList<>();
    private ArrayList<SpinnerItem> petItems = new ArrayList<>();
    private ArrayList<String> availableSlots = new ArrayList<>();

    private Spinner spinnerPupil, spinnerUs, spinnerSlots;
    private EditText editTextDescription;
    private Button buttonFin;
    private TextView textViewVet, textViewDate;

    private String vetId;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_uw);



        Intent intent = getIntent();
        Integer vetID = intent.getIntExtra("vetID", -1);
        String appointmentDateTime = intent.getStringExtra("appointmentDateTime");
        String appointmentDate = intent.getStringExtra("appointmentDate");

        Log.d("AppointmentActivity", "Received vetID: " + vetID + ", appointmentDateTime: " + appointmentDateTime + ", appointmentDate: " + appointmentDate);

        if (vetID == -1 || appointmentDateTime == null || appointmentDateTime.isEmpty() || appointmentDate == null || appointmentDate.isEmpty()) {
            Toast.makeText(this, "Invalid or missing appointment data.", Toast.LENGTH_SHORT).show();
            finish();
        }


        spinnerPupil = findViewById(R.id.spinnerPupil);
        spinnerUs = findViewById(R.id.spinnerUs);
        editTextDescription = findViewById(R.id.editTextOpis);
        buttonFin = findViewById(R.id.buttonFin);

        textViewVet = findViewById(R.id.textViewVet);
        textViewDate = findViewById(R.id.textViewDate);


        fetchVets(vetID, new VetCallback() {
            @Override
            public void onVetFound(String vetName) {
                if (vetName != null) {
                    Log.d("VetInfo", "Vet found: " + vetName);
                    textViewVet.setText(vetName);
                } else {
                    Log.d("VetInfo", "Vet not found or error");
                    textViewVet.setText("Vet not found");
                }
            }
        });






        textViewDate.setText(appointmentDate + " " + appointmentDateTime);



        fetchServices();
        fetchPets();



        buttonFin.setOnClickListener(v -> {
            String selectedPupil = getSpinnerSelection(spinnerPupil);
            String selectedService = getSpinnerSelection(spinnerUs);

            String description = editTextDescription.getText().toString().trim();

            if (validateInputs(selectedPupil, selectedService, description)) {
                sendAppointmentRequest(selectedPupil, String.valueOf(vetID), selectedService, appointmentDateTime, appointmentDate, description);
            }
        });
    }

    private String getSpinnerSelection(Spinner spinner) {
        return spinner.getSelectedItem() != null ? ((SpinnerItem) spinner.getSelectedItem()).getId() : "";
    }

    private boolean validateInputs(String pupil, String service, String description) {
        if (TextUtils.isEmpty(pupil)) {
            Toast.makeText(this, "Please select a pupil", Toast.LENGTH_SHORT).show();
            return false;
        }
        if (TextUtils.isEmpty(service)) {
            Toast.makeText(this, "Please select a service", Toast.LENGTH_SHORT).show();
            return false;
        }
        if (TextUtils.isEmpty(description)) {
            editTextDescription.setError("Description cannot be empty");
            editTextDescription.requestFocus();
            return false;
        }
        return true;
    }



    private void fetchServices() {
        StringRequest request = new StringRequest(Request.Method.GET, SERVICE_LIST_URL,
                response -> {
                    try {
                        JSONArray servicesArray = new JSONArray(response);
                        for (int i = 0; i < servicesArray.length(); i++) {
                            JSONObject service = servicesArray.getJSONObject(i);
                            String id = service.getString("id");
                            String name = service.getString("nazwa");
                            serviceItems.add(new SpinnerItem(id, name));
                        }
                        ArrayAdapter<SpinnerItem> serviceAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, serviceItems);
                        serviceAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                        spinnerUs.setAdapter(serviceAdapter);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                },
                error -> Toast.makeText(this, "Error fetching services", Toast.LENGTH_SHORT).show());
        Volley.newRequestQueue(this).add(request);
    }

    private void fetchPets() {
        String token = MySingleton.getInstance(this).getAuthToken();

        if (token == null) {
            Toast.makeText(this, "User not logged in", Toast.LENGTH_SHORT).show();
            return;
        }

        StringRequest request = new StringRequest(Request.Method.GET, MY_PETS_URL,
                response -> {
                    try {
                        JSONArray petsArray = new JSONArray(response);
                        for (int i = 0; i < petsArray.length(); i++) {
                            JSONObject pet = petsArray.getJSONObject(i);
                            String id = pet.getString("id_pupila");
                            String name = pet.getString("imie");
                            petItems.add(new SpinnerItem(id, name));
                        }
                        ArrayAdapter<SpinnerItem> petAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, petItems);
                        petAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                        spinnerPupil.setAdapter(petAdapter);
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                },
                error -> Toast.makeText(this, "Error fetching pets", Toast.LENGTH_SHORT).show()) {
            @Override
            public java.util.Map<String, String> getHeaders() {
                java.util.Map<String, String> headers = new java.util.HashMap<>();
                headers.put("Authorization", "Bearer " + token);
                return headers;
            }
        };
        Volley.newRequestQueue(this).add(request);
    }

    public void fetchVets(Integer vetID, final VetCallback callback) {
        JsonArrayRequest request = new JsonArrayRequest(Request.Method.GET, VET_LIST_URL, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {

                        JSONArray vets = response;
                        Log.d("AppointmentActivity", "Vets response: " + response.toString());
                        try {

                            for (int i = 0; i < vets.length(); i++) {
                                JSONObject vet = vets.getJSONObject(i);


                                int vetIdFromResponse = vet.getInt("id_weterynarza");

                                Log.d("VetInfo", "Comparing vet ID: " + vetIdFromResponse + " with received vetID: " + vetID);


                                if (vetIdFromResponse == vetID) {

                                    String vetName = vet.getString("nazwisko") + " " + vet.getString("imię");
                                    callback.onVetFound(vetName);
                                    return;
                                }
                            }
                            callback.onVetFound(null);
                        } catch (Exception e) {
                            e.printStackTrace();
                            callback.onVetFound(null);
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

                error.printStackTrace();
                callback.onVetFound(null);
            }
        });

        MySingleton.getInstance(this).addToRequestQueue(request);
    }



    public interface VetCallback {
        void onVetFound(String vetName);
    }

    private void sendAppointmentRequest(String selectedPupil, String selectedVet, String selectedService, String selectedTime, String selectedDate, String description) {
        JSONObject requestBody = new JSONObject();
        Log.d("AppointmentActivity", "Selected pupil: " + selectedPupil);
        Log.d("AppointmentActivity", "Selected vet: " + selectedVet);
        Log.d("AppointmentActivity", "Selected service: " + selectedService);
        Log.d("AppointmentActivity", "Selected time: " + selectedTime);
        Log.d("AppointmentActivity", "Selected date: " + selectedDate);
        Log.d("AppointmentActivity", "Description: " + description);

        try {
            requestBody.put("id_pupila", Integer.parseInt(selectedPupil));
            requestBody.put("id_weterynarza", Integer.parseInt(selectedVet));
            requestBody.put("data_wizyty", selectedDate);
            requestBody.put("godzina_wizyty_od", selectedDate + "T" + selectedTime);
            requestBody.put("id_uslugi", Integer.parseInt(selectedService));
            requestBody.put("opis_dolegliwosci", description);

            } catch (Exception e) {
            e.printStackTrace();
        }
        Log.d("AppointmentActivity", "Sending appointment request with data: " + requestBody.toString());
        String token = MySingleton.getInstance(this).getAuthToken();
        if (token == null) {
            Toast.makeText(this, "User not logged in", Toast.LENGTH_SHORT).show();
            return;
        }

        StringRequest request = new StringRequest(Request.Method.POST, BOOK_APPOINTMENT_URL,
                response -> {
                    Toast.makeText(this, "Appointment scheduled successfully!", Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(this, UserDashboardActivity.class);
                    startActivity(intent);
                    finish();
                },
                error -> Toast.makeText(this, "Error scheduling appointment. Try again.", Toast.LENGTH_SHORT).show()) {

            @Override
            public byte[] getBody() {
                return requestBody.toString().getBytes(StandardCharsets.UTF_8);
            }

            @Override
            public java.util.Map<String, String> getHeaders() {
                java.util.Map<String, String> headers = new java.util.HashMap<>();
                headers.put("Authorization", "Bearer " + token);
                headers.put("Content-Type", "application/json");
                return headers;
            }
        };

        Volley.newRequestQueue(this).add(request);
    }

    public static class SpinnerItem {
        private final String id;
        private final String name;

        public SpinnerItem(String id, String name) {
            this.id = id;
            this.name = name;
        }

        public String getId() {
            return id;
        }

        public String getName() {
            return name;
        }

        @Override
        public String toString() {
            return name;
        }
    }
}
