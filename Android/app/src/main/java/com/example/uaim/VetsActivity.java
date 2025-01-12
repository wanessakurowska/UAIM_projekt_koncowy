package com.example.uaim;

import android.os.Bundle;
import android.widget.ListView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import org.json.JSONArray;
import org.json.JSONObject;
import androidx.appcompat.app.AppCompatActivity;

public class VetsActivity extends AppCompatActivity {

    private ListView listView;
    private String url = "http://10.0.2.2:5000/veterinarian-list";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.list_view);

        listView = findViewById(R.id.ListView);


        fetchVets();
    }

    private void fetchVets() {
        JsonArrayRequest request = new JsonArrayRequest(Request.Method.GET, url, null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {
                            if (response.length() == 0) {


                                Toast.makeText(VetsActivity.this, "No veterinarians found.", Toast.LENGTH_SHORT).show();
                            } else {
                                VetAdapter vetAdapter = new VetAdapter(VetsActivity.this, response);
                                listView.setAdapter(vetAdapter);
                            }
                        } catch (Exception e) {
                            e.printStackTrace();

                            Toast.makeText(VetsActivity.this, "Error parsing response.", Toast.LENGTH_SHORT).show();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();

                Toast.makeText(VetsActivity.this, "Failed to fetch data.", Toast.LENGTH_SHORT).show();
            }
        });


        MySingleton.getInstance(this).addToRequestQueue(request);
    }

}
