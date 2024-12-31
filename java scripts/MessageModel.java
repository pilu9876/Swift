package com.example.bankbot;

public class MessageModel
{
    private String cnt;

    public void setCnt(String cnt) {
        this.cnt = cnt;
    }
    public String getCnt() {
        return cnt;
    }

    public MessageModel(String cnt) {
        this.cnt = cnt;
    }
}
