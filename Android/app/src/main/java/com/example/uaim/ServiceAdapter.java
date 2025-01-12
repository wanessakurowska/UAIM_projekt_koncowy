package com.example.uaim;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import java.util.List;

public class ServiceAdapter extends BaseAdapter {

    private Context context;
    private List<Service> serviceList;


    public ServiceAdapter(Context context, List<Service> serviceList) {
        this.context = context;
        this.serviceList = serviceList;
    }

    @Override
    public int getCount() {
        return serviceList.size();
    }

    @Override
    public Object getItem(int position) {
        return serviceList.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            LayoutInflater inflater = LayoutInflater.from(context);
            convertView = inflater.inflate(R.layout.single_row_us, parent, false);
        }

        TextView textViewId = convertView.findViewById(R.id.textViewId);
        TextView textViewNazwa = convertView.findViewById(R.id.textViewNazwa);
        TextView textViewOpis = convertView.findViewById(R.id.textViewOpis);
        TextView textViewCena = convertView.findViewById(R.id.textViewCena);
        TextView textViewDostepnosc = convertView.findViewById(R.id.textViewDostepnosc);


        Service service = serviceList.get(position);


        textViewId.setText("ID: " + service.getId());
        textViewNazwa.setText("Nazwa: " + service.getName());
        textViewOpis.setText("Opis: " + service.getDescription());
        textViewCena.setText("Cena: " + service.getPrice() + " PLN");
        textViewDostepnosc.setText("Dostepnosc: " + service.isAvailable());

        return convertView;
    }
}
