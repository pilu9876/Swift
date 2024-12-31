package com.example.bankbot;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.*;
import android.annotation.SuppressLint;
import android.content.Context;
import android.os.Bundle;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import android.view.View;
import android.widget.*;
import android.widget.Toast;
import retrofit2.converter.gson.GsonConverterFactory;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import android.webkit.WebView;
import retrofit2.Retrofit;

public class MainActivity extends AppCompatActivity {
    WebView webView;
    private boolean isButtonActivated = false;
    private RecyclerView chatsRV;
    private EditText userMsgEdt;
    private FloatingActionButton sendMsgFAB, SendMsgFAB1;
    private final String BOT_KEY = "bot";
    private final String USER_KEY = "user";
    private ArrayList<ChatsModel> chatsModelArrayList;
    private ChatRVAdapter chatRVAdapter;
    public String url, fileContent;

    public int  messageIndex = -1;
    public Boolean integerTrue, floatTrue, block = false, withdraw;
    private void getResponse(String message) throws FileNotFoundException {
        chatsModelArrayList.add(new ChatsModel(message, USER_KEY));
        chatRVAdapter.notifyDataSetChanged();
        messageIndex = messageIndex + 1;
        if (message.toLowerCase().contains("expenses") || message.toLowerCase().contains("transactions") || message.toLowerCase().contains("statement") || message.toLowerCase().contains("activities")) {
            fileContent = readTextFile("accountno.txt");
            if (fileContent != null) {
                setContentView(R.layout.mysql);
                webView = (WebView) findViewById(R.id.webview1);
                webView.getSettings().setJavaScriptEnabled(true);
                url = "http://192.168.99.180:5000/api?input=" + message + " " + fileContent;
                webView.loadUrl(url);
                webView.setVisibility(View.VISIBLE);
                SendMsgFAB1 = findViewById(R.id.idFABSend1);
                SendMsgFAB1.setOnClickListener(new View.OnClickListener() {
                    @SuppressLint("SetJavaScriptEnabled")
                    @Override
                    public void onClick(View v1) {
                        setContentView(R.layout.activity_main);
                        performAdditionalTasks();
                    }
                });
            }
            messageIndex = -2;
        }
        String BASE_URL = "http://192.168.99.180:5000/";
        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl(BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        RetrofitAPI retrofitAPI = retrofit.create(RetrofitAPI.class);
        if (message.length() == 10 && integerTrue == true) {
            createTextFile("accountno.txt", message);
            url = "http://192.168.99.180:5000/api?input=" + message;
        } else if (floatTrue == true && withdraw ==true){
            ChatsModel chat = chatsModelArrayList.get(messageIndex-2);
            String messagePrevious = chat.getMessage();
            url = "http://192.168.99.180:5000/api?input=" + message+" " + messagePrevious+ " "+ "withdrawtrue" + " " + fileContent;
            withdraw = false;
        } else if (block) {
            url = "http://192.168.99.180:5000/api?input=" + message + " "+ "blocktrue" + " " + fileContent;
            block = false;
        } else {
            fileContent = readTextFile("accountno.txt");
            url = "http://192.168.99.180:5000/api?input=" + message + " " + fileContent;
        }
        Call<MessageModel> callsync = retrofitAPI.getMessage(url);
        callsync.enqueue(new Callback<MessageModel>() {
            @Override
            public void onResponse(Call<MessageModel> callsync, Response<MessageModel> response) {
                if (response.isSuccessful()) {
                    MessageModel model = response.body();
                    if (model.getCnt().contains("valid number")){
                        withdraw = true;
                        String modifiedString = model.getCnt().replace("valid number", "");
                        chatsModelArrayList.add(new ChatsModel(modifiedString, BOT_KEY));
                    } else if (model.getCnt().contains("Please provide details about the card number and recent transactions associated with the card")){
                        block = true;
                        chatsModelArrayList.add(new ChatsModel(model.getCnt(), BOT_KEY));
                    } else if (model.getCnt().contains("Please enter valid Card Number")){
                        block = true;
                        chatsModelArrayList.add(new ChatsModel(model.getCnt(), BOT_KEY));
                    }
                    else {
                        chatsModelArrayList.add(new ChatsModel(model.getCnt(), BOT_KEY));
                    }
                        chatsRV.smoothScrollToPosition(chatsModelArrayList.size() - 0);
                        chatRVAdapter.notifyDataSetChanged();
                        messageIndex = messageIndex + 1;
                }
            }

            @Override
            public void onFailure(Call<MessageModel> callsync, Throwable t) {
                chatsModelArrayList.add(new ChatsModel("Please revert your question", BOT_KEY));
                messageIndex = messageIndex + 1;
                chatsRV.smoothScrollToPosition(chatsModelArrayList.size() - 2);
                chatRVAdapter.notifyDataSetChanged();
            }
       });
    }

    private String createTextFile(String fileName, String filecontent) {
       try {
            FileOutputStream fos = openFileOutput(fileName, Context.MODE_PRIVATE);
            fos.write(filecontent.getBytes());
            fos.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }



    private String readTextFile(String fileName) {
        StringBuilder stringBuilder = new StringBuilder();

        try {

            Context context = getApplicationContext();
            FileInputStream fis = context.openFileInput(fileName);
            InputStreamReader inputStreamReader = new InputStreamReader(fis);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            String line = bufferedReader.readLine();
            System.out.println(line);
            if (line != null) {
                stringBuilder.append(line);
            }

            bufferedReader.close();
            inputStreamReader.close();
            fis.close();
            return stringBuilder.toString();
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        performAdditionalTasks();
    }
    private void performAdditionalTasks() {

        chatsRV = findViewById(R.id.idRVChats);
        userMsgEdt = findViewById(R.id.idEdtMessage);
        sendMsgFAB = findViewById(R.id.idFABSend);
        chatsModelArrayList = new ArrayList<>();
        sendMsgFAB.setOnClickListener(new View.OnClickListener() {
            @SuppressLint("SetJavaScriptEnabled")
            @Override
            public void onClick(View v) {

                if(userMsgEdt.getText().toString().isEmpty()){
                    Toast.makeText(MainActivity.this, "Please enter your message", Toast.LENGTH_SHORT).show();
                    return;
                }
                try {
                    try {
                        Long.parseLong(userMsgEdt.getText().toString());
                        integerTrue = true;
                        floatTrue = false;
                    } catch (NumberFormatException e1) {
                        try {
                            Double.parseDouble(userMsgEdt.getText().toString());
                            integerTrue = false;
                            floatTrue = true;
                        } catch (NumberFormatException e2) {
                            integerTrue = false;
                            floatTrue = false;
                        }
                    }
                    getResponse(userMsgEdt.getText().toString());
                } catch (FileNotFoundException e) {
                    throw new RuntimeException(e);
                }
                userMsgEdt.setText("");
            }
        });
        chatRVAdapter = new ChatRVAdapter(chatsModelArrayList, this);
        LinearLayoutManager manager = new LinearLayoutManager(this, RecyclerView.VERTICAL, false);
        chatsRV.setLayoutManager(manager);
        chatsRV.setAdapter(chatRVAdapter);
    }
}
