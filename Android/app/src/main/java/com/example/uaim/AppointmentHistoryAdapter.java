package com.example.uaim;

import android.app.Activity;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.TextView;

import org.w3c.dom.Text;

import java.util.List;

public class AppointmentHistoryAdapter extends ArrayAdapter<Appointment> {

    private final Activity context;
    private final List<Appointment> appointments;

    public AppointmentHistoryAdapter(Activity context, List<Appointment> appointments) {
        super(context, R.layout.single_row_historiawizyt, appointments);
        this.context = context;
        this.appointments = appointments;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        View rowView = convertView;

        if (rowView == null) {
            LayoutInflater inflater = context.getLayoutInflater();
            rowView = inflater.inflate(R.layout.single_row_historiawizyt, null, true);
        }


        TextView textViewId = rowView.findViewById(R.id.textViewIDW);
        TextView textViewDate = rowView.findViewById(R.id.textViewData);
        TextView textViewTime = rowView.findViewById(R.id.textViewTime);
        TextView textViewPetName = rowView.findViewById(R.id.textViewImiePupila);

        Appointment appointment = appointments.get(position);

        textViewId.setText("ID: " + appointment.getId_wiz());
        textViewDate.setText(appointment.getVisitDate());
        textViewTime.setText(" " + appointment.getVisitTime());
        textViewPetName.setText(appointment.getPetName());

        Button buttonDetails = rowView.findViewById(R.id.buttonSW);
        buttonDetails.setOnClickListener(v -> {
            Intent intent = new Intent(context, DetailsActivity.class);
            intent.putExtra("appointmentId", appointment.getId_wiz());
            intent.putExtra("PetName", appointment.getPetName());
            context.startActivity(intent);
        });


        return rowView;
    }
}
