#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import streamlit as st
from jsonify.convert import jsonify
from pymongo import MongoClient
import pymongo
import json
from pymongo import MongoClient

st.title('Food Tracebility Blockchain Portal')



add_selectbox = st.sidebar.selectbox(
    "You Are?",
    ("Farmer", "Processor","Distributor", "Retailer")
)



if add_selectbox=="Farmer":
    
    #def getDetails_farmer():
        st.header("Enter your details")
        Farmer = st.text_input("FullName", "BDA Framer")
        Quantity = st.text_input("Quantity in Kg", " ")
        Batch_Id = st.text_input("Batch Id", " ")
        Shipped_To = st.text_input("Shipped To", " ")
        Shipped_Date = st.text_input("Shipped Date", " ")
        Item_Type = st.text_input("Item Type", " ")
        Fertilizer_Used = st.text_input("Fertilizer Used", " ")
        farmer_block={
             'Farmer':Farmer,
             'Quantity':Quantity,
             'Batch_ID':Batch_Id,
             'Shipped_To':Shipped_To,
             'Shipped_Date':Shipped_Date,
             'Item_Type':Item_Type,
             'Fertilizer_Used':Fertilizer_Used
          }

        if st.button('Add Details'):
            print("Farmer block details",farmer_block)
            
            try:
                r = requests.post("http://127.0.0.1:5017/add_transaction_farmer", data=json.dumps(farmer_block))
                print("r", r)
                st.write(r.content)
                st.write("Details Added for", Farmer)
                r = requests.get("http://127.0.0.1:5017/mine_block", data=json.dumps(farmer_block))
                

                try:
                    r = requests.get("http://127.0.0.1:5017/replace_chain", data=json.dumps(farmer_block))
                except:
                    st.write(r.content)
                    st.write("Connection Issues in adding data for other nodes")
       
            except:
                st.write(r.content)
                st.write("Connection Issues in adding transaction block")




if add_selectbox=="Processor":
    #def getDetails_Processor():
        st.header("Enter your details")
        Batch_ID = st.text_input("FullName", " ")
        Consignment_Received_Date = st.text_input("Consignment Received Date", " ")
        Shipped_To = st.text_input("Shipped To", " ")
        Shipped_Date = st.text_input("Shipped Date", " ")
        Processing_Date = st.text_input("Processing Date", " ")
        Processor = st.text_input("Processor", " ")

        Processor_block={
             'Batch_ID':Batch_ID,
             'Consignment_Received_Date':Consignment_Received_Date,
             'Shipped_To':Shipped_To,
             'Shipped_Date':Shipped_Date,
             'Processing_Date':Processing_Date,
             'Processor':Processor

          }
        
        if st.button('Add Details'):
            print("Processor block details",Processor_block)
            
            try:
                r = requests.post("http://127.0.0.1:5017/add_transaction_processor", data=json.dumps(Processor_block))
                print("r", r)
                st.write(r.content)
                st.write("Details Added for", Farmer)
                r = requests.get("http://127.0.0.1:5017/mine_block", data=json.dumps(Processor_block))
                

                try:
                    r = requests.get("http://127.0.0.1:5017/replace_chain", data=json.dumps(Processor_block))
                except:
                    st.write(r.content)
                    st.write("Connection Issues in adding data for other nodes")
       
            except:
                st.write(r.content)
                st.write("Connection Issues in adding transaction block")




    



if add_selectbox=="Distributor":
    #def getDetails_distributor():
        st.header("Enter your details")
        Batch_ID = st.text_input("Enter Batch id", " ")
        Consignment_Received_Date = st.text_input("Consignment_Received_Date", " ")
        Shipped_To = st.text_input("Shipped_To", " ")
        Shipped_Date = st.text_input("Shipped_Date", " ")
        Distributor = st.text_input("Distributor", " ")

        distributor_block={
             'Batch_ID':Batch_ID,
             'Consignment_Received_Date':Consignment_Received_Date,
             'Shipped_To':Shipped_To,
             'Shipped_Date':Shipped_Date,
             'Distributor':Distributor
         }

        if st.button('Add Details'):
            print("Distributorr block details",distributor_block)
            
            try:
                r = requests.post("http://127.0.0.1:5017/add_transaction_distributor", data=json.dumps(distributor_block))
                print("r", r)
                st.write(r.content)
                st.write("Details Added for", Farmer)
                r = requests.get("http://127.0.0.1:5017/mine_block", data=json.dumps(distributor_block))
                

                try:
                    r = requests.get("http://127.0.0.1:5017/replace_chain", data=json.dumps(distributor_block))
                except:
                    st.write(r.content)
                    st.write("Connection Issues in adding data for other nodes")
       
            except:
                st.write(r.content)
                st.write("Connection Issues in adding transaction block")
    

    


if add_selectbox=="Retailer":
    #def getDetails_retailer():
        st.header("Enter your details")
        Batch_ID = st.text_input("Enter Batch id", " ")
        Consignment_Received_Date = st.text_input("Consignment_Received_Date", " ")
        Sold_To = st.text_input("Sold_To", " ")
        Retailer = st.text_input("Retailer", " ")

        retailer_block={
             'Batch_ID':Batch_ID,
             'Consignment_Received_Date':Consignment_Received_Date,
             'Sold_To':Sold_To,
             'Retailer':Retailer,
             
         }


        if st.button('Add Details'):
            print("Retailer block details",retailer_block)
            
            try:
                r = requests.post("http://127.0.0.1:5016/add_transaction_retailer", data=json.dumps(retailer_block))
                print("r", r)
                st.write(r.content)
                st.write("Details Added for", Farmer)
                r = requests.get("http://127.0.0.1:5017/mine_block", data=json.dumps(retailer_block))
                

                try:
                    r = requests.get("http://127.0.0.1:5017/replace_chain", data=json.dumps(retailer_block))
                except:
                    st.write(r.content)
                    st.write("Connection Issues in adding data for other nodes")
       
            except:
                st.write(r.content)
                st.write("Connection Issues in adding transaction block")



    
    
    
    
    
    
    

