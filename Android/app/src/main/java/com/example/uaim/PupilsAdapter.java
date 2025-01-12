package com.example.uaim;

import android.app.Activity;
import android.content.Intent;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.TextView;

import java.util.List;

public class PupilsAdapter extends ArrayAdapter<Pet> {

    private final Activity context;
    private final List<Pet> petData;

    public PupilsAdapter(Activity context, List<Pet> petData) {
        super(context, R.layout.single_row_pup, petData);
        this.context = context;
        this.petData = petData;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View rowView = convertView;


        if (rowView == null) {
            LayoutInflater inflater = context.getLayoutInflater();
            rowView = inflater.inflate(R.layout.single_row_pup, null, true);
        }


        TextView textViewIDPup = rowView.findViewById(R.id.textViewIDPup);
        TextView textViewImiePup = rowView.findViewById(R.id.textViewImiePup);
        TextView textViewWiek = rowView.findViewById(R.id.textViewWiek);
        TextView textViewPlec = rowView.findViewById(R.id.textViewPlec);
        TextView textViewRasa = rowView.findViewById(R.id.textViewRasa);
        TextView textViewOpisPup = rowView.findViewById(R.id.textViewOpisPup);
        Button buttonHistW = rowView.findViewById(R.id.buttonHistW);
        Button buttonEdit = rowView.findViewById(R.id.buttonEdit);

        Pet pet = petData.get(position);


        textViewIDPup.setText("ID: " + pet.getId());
        textViewImiePup.setText("  " +pet.getName());
        textViewWiek.setText("Wiek: " + pet.getAge());
        textViewPlec.setText("Płeć: " + pet.getGender());
        textViewRasa.setText("Rasa: " + pet.getBreed());
        textViewOpisPup.setText("Opis: " + pet.getDescription());


        buttonHistW.setOnClickListener(v -> {

            Intent intent = new Intent(context, AppointmentHistorySingleActivity.class);


            intent.putExtra("pupilID", pet.getId());
            intent.putExtra("pupilName", pet.getName());
            Log.d("PupilID", "Sent ID: "+ pet.getId());
            Log.d("PupilName", "Sent name: "+ pet.getName());
            context.startActivity(intent);
        });

        buttonEdit.setOnClickListener(v -> {
            Intent intent = new Intent(context, EditPupilActivity.class);
            intent.putExtra("pupilID", pet.getId());
            intent.putExtra("pupilName", pet.getName());
            Log.d("PupilID", "Sent ID: " + pet.getId());
            Log.d("PupilName", "Sent name: " + pet.getName());
            context.startActivity(intent);
        });


        return rowView;
    }
}
