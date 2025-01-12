package com.example.uaim;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class SlotAdapter extends RecyclerView.Adapter<SlotAdapter.SlotViewHolder> {

    private List<String> slotList = new ArrayList<>();
    private OnSlotClickListener onSlotClickListener;


    public interface OnSlotClickListener {
        void onSlotClick(String slotTime);
    }

    public SlotAdapter(OnSlotClickListener onSlotClickListener) {
        this.onSlotClickListener = onSlotClickListener;
    }

    public void updateSlots(JSONArray slots) {
        slotList.clear();
        for (int i = 0; i < slots.length(); i++) {
            try {
                JSONObject slot = slots.getJSONObject(i);
                String time = slot.getString("time");
                slotList.add(time);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public SlotViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(android.R.layout.simple_list_item_1, parent, false);
        return new SlotViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull SlotViewHolder holder, int position) {
        String time = slotList.get(position);
        holder.textView.setText(time);


        holder.itemView.setOnClickListener(v -> onSlotClickListener.onSlotClick(time));
    }

    @Override
    public int getItemCount() {
        return slotList.size();
    }

    static class SlotViewHolder extends RecyclerView.ViewHolder {
        TextView textView;

        SlotViewHolder(@NonNull View itemView) {
            super(itemView);
            textView = itemView.findViewById(android.R.id.text1);
        }
    }
}

