package com.example.myapplication.model;

public class AppData {

    private int temperature;
    private int luminosite;

    public AppData(int temperature, int luminosite) {
        this.temperature = temperature;
        this.luminosite = luminosite;
    }

    public int getTemperature() {
        return temperature;
    }

    public int getLuminosite() {
        return luminosite;
    }
}
