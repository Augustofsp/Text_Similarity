package com.example.textsimilarity

import android.os.Bundle
import android.widget.ListView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.Observer
import androidx.lifecycle.ViewModelProvider
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    private lateinit var viewModel: ComplaintViewModel
    private lateinit var customAdapter: CustomAdapter
    private lateinit var listViewComplaints: ListView // Manually declare the ListView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Manually initialize the ListView using findViewById
        listViewComplaints = findViewById(R.id.listViewComplaints)
        customAdapter = CustomAdapter(emptyList(), this)

        listViewComplaints.adapter = customAdapter

        viewModel = ViewModelProvider(this).get(ComplaintViewModel::class.java)

        // Observe the complaints and update the UI
        viewModel.complaints.observe(this, Observer { complaints ->
            complaints?.let {
                customAdapter.setData(it)
            }
        })

        // Fetch data from the API
        GlobalScope.launch {
            // Introduce a delay to simulate an asynchronous operation
            delay(1000)
            viewModel.fetchDataFromApi()
        }
    }
}

