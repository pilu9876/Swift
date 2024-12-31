package com.example.bankbot;

import retrofit2.http.GET;
import retrofit2.http.Url;
import retrofit2.Call;
public interface RetrofitAPI {
    @GET Call<MessageModel> getMessage(@Url String url);

}