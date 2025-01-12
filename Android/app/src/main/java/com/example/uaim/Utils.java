package com.example.uaim;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.io.InputStream;

public class Utils {
    public static String readStream(InputStream inputStream) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
        StringBuilder stringBuilder = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            stringBuilder.append(line);
        }
        return stringBuilder.toString();
    }
}
