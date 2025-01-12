package com.example.uaim;


public class Service {

    private int id;
    private String name;
    private String description;
    private double price;
    private String available;

    public Service(int id, String name, String description, double price, String available) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.price = price;
        this.available = available;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public double getPrice() {
        return price;
    }

    public String isAvailable() {
        return available;
    }
}
