package com.example.musedata;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.text.format.Formatter;
import android.util.Log;
import android.widget.Button;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import weka.classifiers.Classifier;
import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.Instances;

import static android.os.SystemClock.sleep;

public class MainActivity extends AppCompatActivity {

    Button direction;
    Boolean start = false;
    double finalResult = 0;
    float [][] lisst = null;
    // ArrayList<String> array = new ArrayList<>();         Test set
    String ipAddress;
    ArrayList<Attribute> attribute = null;
    Instances dataUnpredicted = null;

    Classifier cls;

    String[] columns = {"Accelerometer-X-max","Accelerometer-X-min","Accelerometer-X-avg","Accelerometer-X-var","Accelerometer-X-skew","Accelerometer-X-kurt",
            "Accelerometer-X-aut1","Accelerometer-X-aut2","Accelerometer-X-aut3","Accelerometer-X-aut4","Accelerometer-X-aut5","Accelerometer-X-aut6",
            "Accelerometer-X-aut7","Accelerometer-X-aut8","Accelerometer-X-aut9","Accelerometer-X-aut10","Accelerometer-X-pks1","Accelerometer-X-pks2",
            "Accelerometer-X-pks3","Accelerometer-X-pks4","Accelerometer-X-pks5","Accelerometer-X-fpk1","Accelerometer-X-fpk2","Accelerometer-X-fpk3",
            "Accelerometer-X-fpk4","Accelerometer-X-fpk5","Accelerometer-Y-max","Accelerometer-Y-min","Accelerometer-Y-avg","Accelerometer-Y-var",
            "Accelerometer-Y-skew","Accelerometer-Y-kurt","Accelerometer-Y-aut1","Accelerometer-Y-aut2","Accelerometer-Y-aut3","Accelerometer-Y-aut4",
            "Accelerometer-Y-aut5","Accelerometer-Y-aut6","Accelerometer-Y-aut7","Accelerometer-Y-aut8","Accelerometer-Y-aut9","Accelerometer-Y-aut10",
            "Accelerometer-Y-pks1","Accelerometer-Y-pks2","Accelerometer-Y-pks3","Accelerometer-Y-pks4","Accelerometer-Y-pks5","Accelerometer-Y-fpk1",
            "Accelerometer-Y-fpk2","Accelerometer-Y-fpk3","Accelerometer-Y-fpk4","Accelerometer-Y-fpk5","Accelerometer-Z-max","Accelerometer-Z-min",
            "Accelerometer-Z-avg","Accelerometer-Z-var","Accelerometer-Z-skew","Accelerometer-Z-kurt","Accelerometer-Z-aut1","Accelerometer-Z-aut2",
            "Accelerometer-Z-aut3","Accelerometer-Z-aut4","Accelerometer-Z-aut5","Accelerometer-Z-aut6","Accelerometer-Z-aut7","Accelerometer-Z-aut8",
            "Accelerometer-Z-aut9","Accelerometer-Z-aut10","Accelerometer-Z-pks1","Accelerometer-Z-pks2","Accelerometer-Z-pks3","Accelerometer-Z-pks4",
            "Accelerometer-Z-pks5","Accelerometer-Z-fpk1","Accelerometer-Z-fpk2","Accelerometer-Z-fpk3","Accelerometer-Z-fpk4","Accelerometer-Z-fpk5",
            "Gyro-X-max","Gyro-X-min","Gyro-X-avg","Gyro-X-var","Gyro-X-skew","Gyro-X-kurt","Gyro-X-aut1","Gyro-X-aut2","Gyro-X-aut3","Gyro-X-aut4",
            "Gyro-X-aut5","Gyro-X-aut6","Gyro-X-aut7","Gyro-X-aut8","Gyro-X-aut9","Gyro-X-aut10","Gyro-X-pks1","Gyro-X-pks2","Gyro-X-pks3","Gyro-X-pks4",
            "Gyro-X-pks5","Gyro-X-fpk1","Gyro-X-fpk2","Gyro-X-fpk3","Gyro-X-fpk4","Gyro-X-fpk5","Gyro-Y-max","Gyro-Y-min","Gyro-Y-avg","Gyro-Y-var",
            "Gyro-Y-skew","Gyro-Y-kurt","Gyro-Y-aut1","Gyro-Y-aut2","Gyro-Y-aut3","Gyro-Y-aut4","Gyro-Y-aut5","Gyro-Y-aut6","Gyro-Y-aut7","Gyro-Y-aut8",
            "Gyro-Y-aut9","Gyro-Y-aut10","Gyro-Y-pks1","Gyro-Y-pks2","Gyro-Y-pks3","Gyro-Y-pks4","Gyro-Y-pks5","Gyro-Y-fpk1","Gyro-Y-fpk2","Gyro-Y-fpk3",
            "Gyro-Y-fpk4","Gyro-Y-fpk5","Gyro-Z-max","Gyro-Z-min","Gyro-Z-avg","Gyro-Z-var","Gyro-Z-skew","Gyro-Z-kurt","Gyro-Z-aut1","Gyro-Z-aut2",
            "Gyro-Z-aut3","Gyro-Z-aut4","Gyro-Z-aut5","Gyro-Z-aut6","Gyro-Z-aut7","Gyro-Z-aut8","Gyro-Z-aut9","Gyro-Z-aut10","Gyro-Z-pks1","Gyro-Z-pks2",
            "Gyro-Z-pks3","Gyro-Z-pks4","Gyro-Z-pks5","Gyro-Z-fpk1","Gyro-Z-fpk2","Gyro-Z-fpk3","Gyro-Z-fpk4","Gyro-Z-fpk5"};


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        direction = (Button)findViewById(R.id.direction);
        Button btn = findViewById(R.id.stop);

        WifiManager wifiManager = (WifiManager) getApplicationContext().getSystemService(WIFI_SERVICE);
        ipAddress = Formatter.formatIpAddress(wifiManager.getConnectionInfo().getIpAddress());

        attribute = new ArrayList<Attribute>();
        for (int i = 0; i < 156; i++) {
            attribute.add(new Attribute(columns[i]));
        }
        final List<String> classes = new ArrayList<String>() {
            {
                add("-1");
                add("0");
                add("1");
                add("2");
                add("3");
            }
        };

        ArrayList<Attribute> attributeList = new ArrayList<Attribute>(2) {
            {
                for (int i = 0; i < attribute.size(); i++)
                    add(attribute.get(i));
                Attribute attributeClass = new Attribute("@@class@@", classes);
                add(attributeClass);
            }
        };


        dataUnpredicted = new Instances("TestInstances",
                attributeList, 1);
        dataUnpredicted.setClassIndex(dataUnpredicted.numAttributes() - 1);

        try {
            cls = (Classifier) weka.core.SerializationHelper
                    .read(getAssets().open("RandomForest.model"));
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (cls == null)
            return;

        btn.setOnClickListener( v -> {
            start = !start;
            int i = 0;
            while (i<10) {
                AsyncTaskExample asyncT = new AsyncTaskExample();
                asyncT.execute();
                i++;
            }
            sleep(45000);
            // Save(array);     Function used to extract test set

        });


    }


    @SuppressLint("StaticFieldLeak")
    private class AsyncTaskExample extends AsyncTask<Void, Void, String> {
        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            if (!Python.isStarted()) {
                Python.start(new AndroidPlatform(getApplicationContext()));
            }
        }
        @Override
        protected String doInBackground(Void... voids) {
            Python py = Python.getInstance();
            PyObject osc_server = py.getModule("OSCserver");
            osc_server.callAttr("main", ipAddress);
            sleep(500);
            PyObject pyobj = py.getModule("myscript");
            PyObject obj = pyobj.callAttr("main");
            if (obj==null)
                lisst = null;
            else
                lisst = obj.toJava(float[][].class);

            if (lisst != null ) {
                DenseInstance newInstance = new DenseInstance(dataUnpredicted.numAttributes()) {
                    {
                        for (int i = 0; i < attribute.size(); i++)
                            setValue(attribute.get(i), lisst[0][i]);
                    }
                };

                lisst = null;
                newInstance.setDataset(dataUnpredicted);

                try {
                    finalResult = cls.classifyInstance(newInstance);
                    Log.d("NEW INSTANCE : ", String.valueOf(newInstance));
                    //array.add(String.valueOf(newInstance)+",3");                  Add desired class to the test set
                    Log.d("Result ---> ", dataUnpredicted.classAttribute().value((int) finalResult));
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            return (dataUnpredicted.classAttribute().value((int) finalResult));
        }
        @SuppressLint("SetTextI18n")
        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            if(result!=null) {
                if (result.equals("-1"))
                    direction.setBackgroundResource(R.drawable.down);
                else if (result.equals("0"))
                    direction.setBackgroundResource(R.drawable.stop);
                else if (result.equals("1"))
                    direction.setBackgroundResource(R.drawable.up);
                else if (result.equals("2"))
                    direction.setBackgroundResource(R.drawable.turn_left);
                else if (result.equals(("3")))
                    direction.setBackgroundResource(R.drawable.turn_right);
            }else {
                direction.setText("Error");
            }
        }
    }


    // Funzione per la scrittura su file
    public void Save(ArrayList<String> data)
    {
        String state = Environment.getExternalStorageState();
        if (!Environment.MEDIA_MOUNTED.equals(state)) {
            //If it isn't mounted - we can't write into it.
            return;
        }
        //Create a new file that points to the root directory, with the given name:
        File file = new File(getExternalFilesDir(null) , "test.csv");
        int n=1;
        while (file.exists()) {
            file = new File(getExternalFilesDir(null), "test"+n+".csv");
            n++;
        }
        FileOutputStream fos = null;
        try
        {
            fos = new FileOutputStream(file, true);
        }
        catch (FileNotFoundException e) {e.printStackTrace();}
        try
        {
            try
            {
                for (int i = 0; i<data.size(); i++)
                {
                    fos.write(data.get(i).getBytes());
                    if (i < data.size()-1)
                    {
                        fos.write("\n".getBytes());
                    }
                }
                fos.write("\n".getBytes());
            }
            catch (IOException e) {e.printStackTrace();}
        }
        finally
        {
            try
            {
                fos.close();
            }
            catch (IOException e) {e.printStackTrace();}
        }
    }
}