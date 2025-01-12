package com.example.uaim;

import android.os.Bundle;
import android.util.Log;
import android.widget.ListView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class UslugiActivity extends AppCompatActivity {

    private ListView listView;
    private List<Service> serviceList;
    private ServiceAdapter serviceAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.list_view);

        listView = findViewById(R.id.ListView);
        serviceList = new ArrayList<>();
        serviceAdapter = new ServiceAdapter(this, serviceList);
        listView.setAdapter(serviceAdapter);


        fetchServices();
    }

    private void fetchServices() {
        String url = "http://10.0.2.2:5000/service-list";


        String authToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTIzLCJleHAiOjE3MzY3MDE0OTF9.E03Js8RCeXvzV4krzZMErsiB2USWzm4RpTngs74TfO0";


        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {

                            for (int i = 0; i < response.length(); i++) {
                                JSONObject serviceJson = response.getJSONObject(i);

                                int id = serviceJson.getInt("id");
                                String name = serviceJson.getString("nazwa");
                                String description = serviceJson.getString("opis");
                                double price = serviceJson.getDouble("cena");
                                String available = serviceJson.getString("dostepnosc");

                                Service service = new Service(id, name, description, price, available);
                                serviceList.add(service);
                            }


                            serviceAdapter.notifyDataSetChanged();
                        } catch (JSONException e) {
                            e.printStackTrace();
                            Toast.makeText(UslugiActivity.this, "Error parsing data", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                error -> {

                    Log.e("Volley Error", "Error: " + error.getMessage());
                    if (error.networkResponse != null) {
                        Log.e("Volley Error", "Status Code: " + error.networkResponse.statusCode);
                        Log.e("Volley Error", "Response Data: " + new String(error.networkResponse.data));
                    }
                    Toast.makeText(UslugiActivity.this, "Error fetching data", Toast.LENGTH_SHORT).show();
                }
        ) {
            @Override
            public java.util.Map<String, String> getHeaders() {
                java.util.Map<String, String> headers = new java.util.HashMap<>();
                headers.put("Authorization", "Bearer " + authToken);
                return headers;
            }

        };


        Volley.newRequestQueue(this).add(jsonArrayRequest);
    }
}
