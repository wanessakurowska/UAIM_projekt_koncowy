package com.example.uaim;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import org.json.JSONException;
import org.json.JSONObject;
import com.android.volley.toolbox.JsonObjectRequest;
import org.json.JSONObject;

public class LoginActivity extends AppCompatActivity {

    private static final String LOGIN_URL = "http://10.0.2.2:5000/api/login";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        EditText editTextEmail = findViewById(R.id.editTextLogin);
        EditText editTextPassword = findViewById(R.id.editTextPassword);
        Button loginButton = findViewById(R.id.buttonLog);
        Button registerButton = findViewById(R.id.buttonReg);
        loginButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String emailText = editTextEmail.getText().toString().trim();
                String passwordText = editTextPassword.getText().toString().trim();


                if (TextUtils.isEmpty(emailText)) {
                    editTextEmail.setError("Email field cannot be empty");
                    editTextEmail.requestFocus();
                } else if (TextUtils.isEmpty(passwordText)) {
                    editTextPassword.setError("Password field cannot be empty");
                    editTextPassword.requestFocus();
                } else {

                    loginUser(emailText, passwordText);
                }
            }
        });
        registerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(LoginActivity.this, RegisterActivity.class);
                startActivity(intent);
            }
        });
    }



    private void loginUser(String email, String password) {

        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("adres_email", email);
            jsonBody.put("haslo", password);
        } catch (Exception e) {
            e.printStackTrace();
        }


        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, LOGIN_URL, jsonBody,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {

                            if (response.has("error")) {
                                String errorMessage = response.getString("error");
                                Toast.makeText(LoginActivity.this, errorMessage, Toast.LENGTH_SHORT).show();
                            } else {

                                String token = response.getString("token");

                                saveToken(token);

                                Intent intent = new Intent(LoginActivity.this, UserDashboardActivity.class);
                                startActivity(intent);
                                finish();
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                            Toast.makeText(LoginActivity.this, "Error processing response", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(LoginActivity.this, "Error: " + error.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                }) {
            @Override
            public java.util.Map<String, String> getHeaders() {

                java.util.Map<String, String> headers = new java.util.HashMap<>();
                headers.put("Content-Type", "application/json");
                return headers;
            }
        };


        MySingleton.getInstance(this).addToRequestQueue(jsonObjectRequest);
    }


    private void saveToken(String token) {

        SharedPreferences sharedPreferences = getSharedPreferences("app_prefs", MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putString("token", token);
        editor.apply();
    }

}
