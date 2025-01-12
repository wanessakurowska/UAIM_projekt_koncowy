package com.example.uaim;

public class Pet {

    private String id;
    private String name;
    private String age;
    private String gender;
    private String breed;
    private String description;

    public Pet(String id, String name, String age, String gender, String breed, String description) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.gender = gender;
        this.breed = breed;
        this.description = description;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getAge() {
        return age;
    }

    public String getGender() {
        return gender;
    }

    public String getBreed() {
        return breed;
    }

    public String getDescription() {
        return description;
    }
}
