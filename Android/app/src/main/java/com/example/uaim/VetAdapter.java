package com.example.uaim;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;
import org.json.JSONArray;
import org.json.JSONObject;

public class VetAdapter extends BaseAdapter {

    private Context context;
    private JSONArray vets;

    public VetAdapter(Context context, JSONArray vets) {
        this.context = context;
        this.vets = vets;
    }

    @Override
    public int getCount() {
        return vets.length();
    }

    @Override
    public Object getItem(int position) {
        return null;
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            LayoutInflater inflater = LayoutInflater.from(context);
            convertView = inflater.inflate(R.layout.single_row_wet, parent, false);
        }

        ImageView imageView = convertView.findViewById(R.id.imageView);  // Vet Image
        TextView textViewID = convertView.findViewById(R.id.textViewID);
        TextView textViewImie = convertView.findViewById(R.id.textViewImie);
        TextView textViewNaz = convertView.findViewById(R.id.textViewNaz);
        TextView textViewKwa = convertView.findViewById(R.id.textViewKwa);
        TextView textViewDos = convertView.findViewById(R.id.textViewDos);
        TextView textViewOc = convertView.findViewById(R.id.textViewOc);
        TextView textViewStatus = convertView.findViewById(R.id.textViewStatus);

        try {
            JSONObject vet = vets.getJSONObject(position);
            textViewID.setText("ID: " + vet.getString("id_weterynarza"));
            textViewImie.setText("Imie: " + vet.getString("imię"));
            textViewNaz.setText("Nazwisko: " + vet.getString("nazwisko"));
            textViewKwa.setText("Kwalifikacje: " + vet.getString("doświadczenie"));
            textViewDos.setText("Doswiadczenie: " + vet.getString("kwalifikacje"));
            textViewOc.setText("Ocena: " + vet.getString("ocena"));
            textViewStatus.setText("Wyksztalcenie: " + vet.getString("wyksztalcenie"));
        } catch (Exception e) {
            e.printStackTrace();
        }



        return convertView;
    }
}
