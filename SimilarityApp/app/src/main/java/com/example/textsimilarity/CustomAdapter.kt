package com.example.textsimilarity

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView
import com.example.textsimilarity.Complaint

class CustomAdapter(private var dataList: List<Complaint>, private val context: Context) : BaseAdapter() {

    fun setData(newData: List<Complaint>) {
        dataList = newData
        notifyDataSetChanged()
    }

    override fun getCount(): Int {
        return dataList.size
    }

    override fun getItem(position: Int): Any {
        return dataList[position]
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
        var convertView = convertView
        if (convertView == null) {
            val inflater = context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater
            convertView = inflater.inflate(R.layout.list_item, null)
        }

        val fraseTextView: TextView = convertView!!.findViewById(R.id.fraseTextView)
        val categoriaTextView: TextView = convertView.findViewById(R.id.categoriaTextView)

        val data = dataList[position]

        fraseTextView.text = data.frase
        categoriaTextView.text = data.categoria

        return convertView
    }
}
