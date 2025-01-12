package com.example.uaim;

import android.os.Bundle;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;

import org.json.JSONArray;

public class ChooseVetActivity extends AppCompatActivity {

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

                        ChooseVetAdapter vetAdapter = new ChooseVetAdapter(ChooseVetActivity.this, response);
                        listView.setAdapter(vetAdapter);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

                error.printStackTrace();

            }
        });


        MySingleton.getInstance(this).addToRequestQueue(request);
    }
}
