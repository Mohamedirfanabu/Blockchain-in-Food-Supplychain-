#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 11:51:52 2021

@author: win10
"""

### import the libraries
import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse

## PArt 1- Building the BlockChain

class BlockChain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.nodes=set()
        self.create_block(proof=1,previous_hash='0')
        
    def create_block(self,proof,previous_hash):
        block={'index':len(self.chain)+1,
               'timestamp':str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':previous_hash,
               'transactions':self.transactions
            
            }
        self.transactions=[]
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True 
    
    def add_transaction_farmer(self,Farmer,Quantity,Batch_ID,Shipped_To,Shipped_Date,Item_Type,Fertilizer_Used):
        self.transactions.append({
            'Farmer':Farmer,
            'Quantity':Quantity,
            'Batch_ID':Batch_ID,
            'Shipped_To':Shipped_To,
            'Shipped_Date':Shipped_Date,
            'Item_Type':Item_Type,
            'Fertilizer_Used':Fertilizer_Used
            })
        previous_block=self.get_previous_block()
        return previous_block['index']+1
    
    def add_transaction_processor(self,Batch_ID,Consignment_Received_Date,Shipped_To,Shipped_Date,Processing_Date,Processor):
        self.transactions.append({
            'Batch_ID':Batch_ID,
            'Consignment_Received_Date':Consignment_Received_Date,
            'Shipped_To':Shipped_To,
            'Shipped_Date':Shipped_Date,
            'Processing_Date':Processing_Date,
            'Processor':Processor
            })
        previous_block=self.get_previous_block()
        return previous_block['index']+1
    
    def add_transaction_retailer(self,Batch_ID,Consignment_Received_Date,Sold_To,Retailer):
        self.transactions.append({
            'Batch_ID':Batch_ID,
            'Consignment_Received_Date':Consignment_Received_Date,
            'Sold_To':Sold_To,
            'Retailer':Retailer
            
            })
        previous_block=self.get_previous_block()
        return previous_block['index']+1
    
    def add_transaction_distributor(self,Batch_ID,Consignment_Received_Date,Shipped_To,Shipped_Date,Distributor):
        self.transactions.append({
            'Batch_ID':Batch_ID,
            'Consignment_Received_Date':Consignment_Received_Date,
            'Shipped_To':Shipped_To,
            'Shipped_Date':Shipped_Date,
            'Distributor':Distributor
            })
        previous_block=self.get_previous_block()
        return previous_block['index']+1
    
    
    def add_node(self,address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    ### consensus protocol
    
    def replace_chain(self):
        network=self.nodes
        longest_chain=None
        max_length=len(self.chain)
        
        for node in network:
            response=requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
        
            

## Part 2- Mining the BlockChain

app=Flask(__name__)

### creating an address for the node on Port 5000
node_address=str(uuid4()).replace('-','')

### Create The BlockChain
blockchain=BlockChain()

## Create a web app for the API
### Mining the new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    #blockchain.add_transaction(company_type='Farmer',company='GIM Farms',arrival_date='25-11-2021',shipped_date='27-11-2021')
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


# Adding a new transaction to the Blockchain
@app.route('/add_transaction_farmer', methods = ['POST'])
def add_transaction_farmer():
    json = request.get_json()
    transaction_keys = ['Farmer', 'Quantity', 'Batch_ID','Shipped_To','Shipped_Date','Item_Type','Fertilizer_Used']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction_farmer(json['Farmer'],json['Quantity'], json['Batch_ID'], json['Shipped_To'], json['Shipped_Date'], json['Item_Type'],json['Fertilizer_Used'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/add_transaction_processor', methods = ['POST'])
def add_transaction_processor():
    json = request.get_json()
    transaction_keys = ['Batch_ID', 'Consignment_Received_Date', 'Shipped_To','Shipped_Date','Processing_Date','Processor']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction_processor(json['Batch_ID'], json['Consignment_Received_Date'], json['Shipped_To'], json['Shipped_Date'], json['Processing_Date'], json['Processor'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/add_transaction_retailer', methods = ['POST'])
def add_transaction_retailer():
    json = request.get_json()
    transaction_keys = ['Batch_ID', 'Consignment_Received_Date', 'Sold_To','Retailer']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction_retailer(json['Batch_ID'], json['Consignment_Received_Date'], json['Sold_To'], json['Retailer'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/add_transaction_distributor', methods = ['POST'])
def add_transaction_distributor():
    json = request.get_json()
    transaction_keys = ['Batch_ID', 'Consignment_Received_Date', 'Shipped_To','Shipped_Date','Distributor']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction_distributor(json['Batch_ID'], json['Consignment_Received_Date'], json['Shipped_To'], json['Shipped_Date'],                   json['Distributor'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200



# Running the app
app.run(host = '127.0.0.1', port = 5015)






# In[ ]:



    





# In[ ]:





# In[ ]:




