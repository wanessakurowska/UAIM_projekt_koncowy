package com.example.uaim;

import java.io.Serializable;

public class Appointment implements Serializable {
    private String visitDate;
    private String visitTime;
    private String doctorName;
    private String visitReason;
    private String serviceName;
    private String petName;
    private String id_wiz;

    public Appointment(String idwiz, String visitDate, String visitTime, String doctorName, String visitReason, String serviceName, String petName) {
        this.id_wiz = idwiz;
        this.visitDate = visitDate;
        this.visitTime = visitTime;
        this.doctorName = doctorName;
        this.visitReason = visitReason;
        this.serviceName = serviceName;
        this.petName = petName;
    }

    public String getVisitDate() { return visitDate; }
    public String getVisitTime() { return visitTime; }
    public String getPetName() { return petName; }
    public String getId_wiz() { return id_wiz; }
}
