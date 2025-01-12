package com.example.uaim;

import android.content.Context;
import android.content.SharedPreferences;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;

public class MySingleton {
    private static MySingleton instance;
    private RequestQueue requestQueue;
    private static Context context;

    private MySingleton(Context context) {
        this.context = context;
        requestQueue = getRequestQueue();
    }

    public static synchronized MySingleton getInstance(Context context) {
        if (instance == null) {
            instance = new MySingleton(context);
        }
        return instance;
    }

    public RequestQueue getRequestQueue() {
        if (requestQueue == null) {
            requestQueue = Volley.newRequestQueue(context.getApplicationContext());
        }
        return requestQueue;
    }
    public void saveToken(String token) {
        SharedPreferences sharedPreferences = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("token", token);
        editor.apply();
    }


    public String getAuthToken() {
        SharedPreferences sharedPreferences = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE);
        return sharedPreferences.getString("token", null);
    }
    public <T> void addToRequestQueue(Request<T> request) {
        getRequestQueue().add(request);
    }
}
