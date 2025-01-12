package com.example.uaim;

import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

public class AddPupilActivity extends AppCompatActivity {

    private static final String API_URL_ADD_PET = "http://10.0.2.2:5000/api/add-pet";
    private static final String API_URL_SPECIES = "http://10.0.2.2:5000/api/species";
    private static final String API_URL_RACES = "http://10.0.2.2:5000/api/races";

    private Spinner spinnerGatunek, spinnerRasa;
    private HashMap<String, Integer> speciesMap = new HashMap<>();
    private HashMap<String, Integer> raceMap = new HashMap<>();
    private int selectedSpeciesId = -1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_addpup);

        EditText editTextImiePup = findViewById(R.id.editTextImiePup);
        EditText editTextWiek = findViewById(R.id.editTextNumberWiek);
        EditText editTextOpisPupil = findViewById(R.id.editTextOpisPupil);
        spinnerGatunek = findViewById(R.id.spinnerGatunek);
        spinnerRasa = findViewById(R.id.spinnerRasa);
        Spinner spinnerPlecPupil = findViewById(R.id.spinnerPlecPupil);
        Button buttonFinAdP = findViewById(R.id.buttonFinAdP);


        loadSpecies();


        ArrayList<String> genderList = new ArrayList<>();
        genderList.add("Męska");
        genderList.add("Żeńska");

        ArrayAdapter<String> genderAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, genderList);
        genderAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinnerPlecPupil.setAdapter(genderAdapter);

        spinnerGatunek.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                String selectedSpecies = (String) parent.getItemAtPosition(position);
                selectedSpeciesId = speciesMap.get(selectedSpecies);
                loadRaces(selectedSpeciesId);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {}
        });

        buttonFinAdP.setOnClickListener(v -> {
            String name = editTextImiePup.getText().toString().trim();
            String age = editTextWiek.getText().toString().trim();
            String description = editTextOpisPupil.getText().toString().trim();
            String gender = (String) spinnerPlecPupil.getSelectedItem();
            String selectedRace = (String) spinnerRasa.getSelectedItem();

            if (name.isEmpty() || age.isEmpty() || description.isEmpty() || gender.isEmpty() || selectedRace == null) {
                Toast.makeText(AddPupilActivity.this, "Proszę wypełnić wszystkie pola.", Toast.LENGTH_SHORT).show();
                return;
            }


            String genderCode = gender.equals("Męska") ? "M" : "F";

            JSONObject petData = new JSONObject();
            try {
                petData.put("imie", name);
                petData.put("wiek", age);
                petData.put("opis", description);
                petData.put("plec", genderCode);
                petData.put("id_rasy", raceMap.get(selectedRace));
            } catch (JSONException e) {
                e.printStackTrace();
            }

            addPetToDatabase(petData);
        });
    }

    private void loadSpecies() {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(API_URL_SPECIES).build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                runOnUiThread(() -> Toast.makeText(AddPupilActivity.this, "Błąd ładowania gatunków: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        JSONArray speciesArray = new JSONArray(response.body().string());
                        ArrayList<String> speciesList = new ArrayList<>();
                        for (int i = 0; i < speciesArray.length(); i++) {
                            JSONObject speciesObj = speciesArray.getJSONObject(i);
                            String name = speciesObj.getString("nazwa");
                            int id = speciesObj.getInt("id_gatunku");
                            speciesList.add(name);
                            speciesMap.put(name, id);
                        }
                        runOnUiThread(() -> {
                            ArrayAdapter<String> adapter = new ArrayAdapter<>(AddPupilActivity.this, android.R.layout.simple_spinner_item, speciesList);
                            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                            spinnerGatunek.setAdapter(adapter);
                        });
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else {
                    runOnUiThread(() -> Toast.makeText(AddPupilActivity.this, "Błąd ładowania gatunków.", Toast.LENGTH_SHORT).show());
                }
            }
        });
    }

    private void loadRaces(int speciesId) {
        OkHttpClient client = new OkHttpClient();
        String url = API_URL_RACES + "?id_gatunku=" + speciesId;
        Request request = new Request.Builder().url(url).build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                runOnUiThread(() -> Toast.makeText(AddPupilActivity.this, "Błąd ładowania ras: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        JSONArray racesArray = new JSONArray(response.body().string());
                        ArrayList<String> racesList = new ArrayList<>();
                        raceMap.clear();
                        for (int i = 0; i < racesArray.length(); i++) {
                            JSONObject raceObj = racesArray.getJSONObject(i);
                            String name = raceObj.getString("rasa");
                            int id = raceObj.getInt("id_rasy");
                            racesList.add(name);
                            raceMap.put(name, id);
                        }
                        runOnUiThread(() -> {
                            ArrayAdapter<String> adapter = new ArrayAdapter<>(AddPupilActivity.this, android.R.layout.simple_spinner_item, racesList);
                            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                            spinnerRasa.setAdapter(adapter);
                        });
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                } else {
                    runOnUiThread(() -> Toast.makeText(AddPupilActivity.this, "Błąd ładowania ras.", Toast.LENGTH_SHORT).show());
                }
            }
        });
    }

    private void addPetToDatabase(JSONObject petData) {
        OkHttpClient client = new OkHttpClient();
        RequestBody body = RequestBody.create(
                petData.toString(), okhttp3.MediaType.get("application/json; charset=utf-8"));

        String token = MySingleton.getInstance(AddPupilActivity.this).getAuthToken();
        Request request = new Request.Builder()
                .url(API_URL_ADD_PET)
                .post(body)
                .addHeader("Authorization", "Bearer " + token)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                runOnUiThread(() -> Toast.makeText(AddPupilActivity.this, "Błąd połączenia: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    runOnUiThread(() -> {
                        Toast.makeText(AddPupilActivity.this, "Dodano pupila", Toast.LENGTH_SHORT).show();
                        finish();
                    });
                } else {
                    runOnUiThread(() -> Toast.makeText(AddPupilActivity.this, "Błąd: " + response.message(), Toast.LENGTH_SHORT).show());
                }
            }
        });
    }
}
