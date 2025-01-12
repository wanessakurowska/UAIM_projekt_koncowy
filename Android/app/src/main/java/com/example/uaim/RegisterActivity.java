package com.example.uaim;

import android.content.Intent;
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
import com.android.volley.toolbox.JsonObjectRequest;
import org.json.JSONObject;

public class RegisterActivity extends AppCompatActivity {

    private static final String REGISTER_URL = "http://10.0.2.2:5000/api/register";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        EditText editTextImie = findViewById(R.id.editTextImie);
        EditText editTextNaz = findViewById(R.id.editTextNaz);
        EditText editTextTel = findViewById(R.id.editTextTel);
        EditText editTextAdres = findViewById(R.id.editTextAdres);
        EditText editTextLogin = findViewById(R.id.editTextLogin);
        EditText editTextPassword = findViewById(R.id.editTextPassword);
        EditText editTextPassword2 = findViewById(R.id.editTextPassword2);
        Button registerButton = findViewById(R.id.buttonReg);


        registerButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String imie = editTextImie.getText().toString().trim();
                String nazwisko = editTextNaz.getText().toString().trim();
                String telefon = editTextTel.getText().toString().trim();
                String adres = editTextAdres.getText().toString().trim();
                String login = editTextLogin.getText().toString().trim();
                String password = editTextPassword.getText().toString().trim();
                String password2 = editTextPassword2.getText().toString().trim();


                if (TextUtils.isEmpty(imie)) {
                    editTextImie.setError("First name cannot be empty");
                    editTextImie.requestFocus();
                } else if (TextUtils.isEmpty(nazwisko)) {
                    editTextNaz.setError("Last name cannot be empty");
                    editTextNaz.requestFocus();
                } else if (TextUtils.isEmpty(telefon)) {
                    editTextTel.setError("Phone number cannot be empty");
                    editTextTel.requestFocus();
                } else if (TextUtils.isEmpty(adres)) {
                    editTextAdres.setError("Address ID cannot be empty");
                    editTextAdres.requestFocus();
                } else if (TextUtils.isEmpty(login)) {
                    editTextLogin.setError("Email/Login cannot be empty");
                    editTextLogin.requestFocus();
                } else if (TextUtils.isEmpty(password)) {
                    editTextPassword.setError("Password cannot be empty");
                    editTextPassword.requestFocus();
                } else if (TextUtils.isEmpty(password2)) {
                    editTextPassword2.setError("Repeat password cannot be empty");
                    editTextPassword2.requestFocus();
                } else if (!password.equals(password2)) {
                    editTextPassword2.setError("Passwords do not match");
                    editTextPassword2.requestFocus();
                } else {

                    registerUser(imie, nazwisko, telefon, adres, login, password);
                }
            }
        });
    }

    private void registerUser(String imie, String nazwisko, String telefon, String adres, String login, String password) {

        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("imie", imie);
            jsonBody.put("nazwisko", nazwisko);
            jsonBody.put("adres_email", login);
            jsonBody.put("haslo", password);
            jsonBody.put("nr_telefonu", telefon);
            jsonBody.put("id_adresu", adres);
        } catch (Exception e) {
            e.printStackTrace();
        }


        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, REGISTER_URL, jsonBody,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        try {
                            if (response.has("error")) {
                                String errorMessage = response.getString("error");
                                Toast.makeText(RegisterActivity.this, errorMessage, Toast.LENGTH_SHORT).show();
                            } else {
                                String successMessage = response.getString("message");
                                Toast.makeText(RegisterActivity.this, successMessage, Toast.LENGTH_SHORT).show();

                                Intent intent = new Intent(RegisterActivity.this, MainActivity.class);
                                startActivity(intent);
                                finish();
                            }
                        } catch (Exception e) {
                            e.printStackTrace();
                            Toast.makeText(RegisterActivity.this, "Error processing response", Toast.LENGTH_SHORT).show();
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(RegisterActivity.this, "Error: " + error.getMessage(), Toast.LENGTH_SHORT).show();
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
}
