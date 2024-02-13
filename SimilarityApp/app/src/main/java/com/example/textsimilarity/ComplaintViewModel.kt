package com.example.textsimilarity

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject

class ComplaintViewModel : ViewModel() {

    private val _complaints = MutableLiveData<List<Complaint>>()
    val complaints: LiveData<List<Complaint>> get() = _complaints

    fun fetchDataFromApi() {
        GlobalScope.launch(Dispatchers.IO) {
            try {
                val apiResponse = HttpUtils.fetchDataFromApi("localhost:5000/complaints")
                val complaintsList = parseJsonResponse(apiResponse)
                _complaints.postValue(complaintsList)
            } catch (e: Exception) {

            }
        }
    }

    private suspend fun parseJsonResponse(jsonString: String): List<Complaint> {
        return withContext(Dispatchers.Default) {
            val complaintsList = mutableListOf<Complaint>()
            val jsonArray = JSONArray(jsonString)

            for (i in 0 until jsonArray.length()) {
                val jsonObject: JSONObject = jsonArray.getJSONObject(i)
                val complaint = Complaint(
                    jsonObject.getString("complaint"),
                    jsonObject.getString("category")
                )
                complaintsList.add(complaint)
            }

            complaintsList
        }
    }
}
