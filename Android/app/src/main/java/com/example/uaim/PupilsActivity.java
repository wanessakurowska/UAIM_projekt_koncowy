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

public class PupilsActivity extends AppCompatActivity {

    private static final String MY_PETS_URL = "http://10.0.2.2:5000/api/my-pets";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.list_view);

        ListView listView = findViewById(R.id.ListView);


        fetchPets(listView);
    }

    private void fetchPets(ListView listView) {

        String token = MySingleton.getInstance(PupilsActivity.this).getAuthToken();

        if (token == null) {
            Toast.makeText(PupilsActivity.this, "User not logged in", Toast.LENGTH_SHORT).show();
            return;
        }


        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(Request.Method.GET, MY_PETS_URL, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {

                        ArrayList<Pet> petList = new ArrayList<>();

                        try {

                            for (int i = 0; i < response.length(); i++) {
                                JSONObject petObject = response.getJSONObject(i);


                                String id = petObject.getString("id_pupila");
                                String name = petObject.getString("imie");
                                String age = petObject.getString("wiek");
                                String gender = petObject.getString("plec");
                                String breed = petObject.getString("rasa");
                                String description = petObject.getString("opis");


                                Pet pet = new Pet(id, name, age, gender, breed, description);
                                petList.add(pet);
                            }


                            PupilsAdapter adapter = new PupilsAdapter(PupilsActivity.this, petList);
                            listView.setAdapter(adapter);

                        } catch (Exception e) {
                            Log.e("PupilsActivity", "Error parsing pets data", e);
                            Toast.makeText(PupilsActivity.this, "Failed to load pets", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.e("PupilsActivity", "Error fetching pets", error);
                        Toast.makeText(PupilsActivity.this, "Error fetching pets", Toast.LENGTH_SHORT).show();
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
