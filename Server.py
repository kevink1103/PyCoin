import sys
import json
from hashlib import sha256

import requests
from pyprnt import prnt
from flask import Flask, jsonify, request

from pycoin import Wallet
from pycoin import Transaction
from pycoin import Block
from pycoin import Blockchain

# EE4017 Lab 6

# Initializing Flask framework and the client
# Flask is a lightweight web application framework for Python
# use it to build APIs to interact with the blockchain client through http requests.
app = Flask(__name__)

# Initialize the wallet, the blockchain
myWallet = Wallet()
blockchain = Blockchain(myWallet)

# Flask uses the @app.route() decorator to define an API.
# All API return messages in JSON file format and a number (HTTP status code) behind it.
# All Flask API must be placed outside of all classes and the main method.

@app.route('/status', methods=['GET'])
def status():
    if myWallet and blockchain:
        return "alive", 200
    return "dead", 400


@app.route('/register_node', methods=['POST'])
def register_node():
    '''
    This API
    a) registers new node with provided IP address
    b) retrieves IP list from provided IP address using source IP address of this request and the provided com_port
    '''
    values = request.form
    node = values.get('node')
    com_port = values.get('com_port')
    # Handle type A invalid request
    if node is None and com_port is None:
        return "Error: Please supply a valid nodes", 400
    # Handle type B request
    if com_port is not None:
        blockchain.register_node(request.remote_addr + ":" + com_port)
        return "ok", 200
    # Register node
    blockchain.register_node(node)
    # Retrieve nodes list
    try:
        node_list = requests.get('http://' + node + '/get_nodes')
    except:
        return "Error: the address is invalid", 400
    if node_list.status_code == 200:
        node_list = node_list.json()['nodes']
        for node in node_list:
            blockchain.register_node(node)

    for new_node in blockchain.nodes:
        # Sending type B request
        requests.post('http://' + new_node + '/register_node', data={'com_port': str(port)})
        requests.get('http://' + new_node + '/consensus')
    # Check if our chain is authoritative from other nodes
    replaced = blockchain.consensus()
    if replaced:
        response = {
            'message': 'Longer authoritative chain found from peers, replacing ours',
            'total_nodes': [node for node in blockchain.nodes]
        }
    else:
        response = {
            'message': 'New nodes have been added, but our chain is authoritative',
            'total_nodes': [node for node in blockchain.nodes]
        }
    return jsonify(response), 201


@app.route('/get_nodes', methods=['GET'])
def get_nodes():
    '''This API accesses IP addresses stored in class Blockchain for other nodes'''
    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def part_chain():
    '''
    This API returns the last 10 blocks only
    Because transferring the whole chain is time consuming especially when the size of chain is long
    Sometimes, we just need the last few blocks to confirm our transactions.
    '''
    response = {
        'chain': json.dumps(blockchain.chain[-10:]),
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/fullchain', methods=['GET'])
def full_chain():
    '''This API returns the whole blockchain'''
    response = {
        'chain': json.dumps(blockchain.chain),
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# ----------------------------------------------------------------------------------------------------------------------
# New APIs beyond EE4017 Lab 6
# Develop a lightweight node that store block header

@app.route('/lightweight', methods=['GET'])
def lightweight():
    fullchain = [json.loads(block) for block in blockchain.chain]
    lightweight = []
    for block in fullchain:
        block_object = Block(block['index'], block['transaction'], block['timestamp'], block['previous_hash'])
        block_object.merkle_root = block['merkle_root']
        block_object.nonce = block['nonce']
        block_object.difficulty = block['difficulty']
        lightweight.append(block_object.to_dict())
    response = {
        'chain': json.dumps(lightweight),
        'length': len(lightweight)
    }
    return jsonify(response), 200


@app.route('/check_balance', methods=['POST'])
def check_balance():
    values = request.form
    required = ['address']
    # Check that the required fields are in the POST data
    if not all(k in values for k in required):
        return 'Missing values', 400
    address = values.get('address')
    balance = blockchain.check_balance(address)
    return jsonify(balance), 200

# ----------------------------------------------------------------------------------------------------------------------


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    '''This API adds transactions to the transaction pool'''
    values = request.form
    required = ['recipient_address', 'value']
    # Check that the required fields are in the POST data
    if not all(k in values for k in required):
        return 'Missing values', 400
    transaction = Transaction(myWallet.pubkey, values['recipient_address'], values['value'])
    transaction.add_signature(myWallet.sign_transaction(transaction))
    transaction_result = blockchain.add_new_transaction(transaction)
    if transaction_result:
        response = {'message': 'Transaction will be added to Block'}
        return jsonify(response), 201
    else:
        response = {'message': 'Invalid Transaction!'}
        return jsonify(response), 406


@app.route('/new_transaction_signed', methods=['POST'])
def new_transaction_signed():
    values = request.form
    required = ['sender', 'recipient_address', 'value', 'signature']
    # Check that the required fields are in the POST data
    if not all(k in values for k in required):
        return 'Missing values', 400
    transaction = Transaction(values['sender'], values['recipient_address'], values['value'])
    transaction.signature = values['signature']
    transaction_result = blockchain.add_new_transaction(transaction)
    if transaction_result:
        response = {'message': 'Transaction will be added to Block'}
        return jsonify(response), 201
    else:
        response = {'message': 'Invalid Transaction!'}
        return jsonify(response), 406


@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    '''This API gets the transaction pool'''
    # Get transactions from transactions pool
    transactions = json.dumps(blockchain.unconfirmed_transactions)
    response = {'transactions': transactions}
    return jsonify(response), 200


@app.route('/consensus', methods=['GET'])
def consensus():
    '''
    A consensus API is needed for other nodes to notify us
    that a new block is formed and should have initialized a synchronization process.
    '''
    replaced = blockchain.consensus()
    if replaced:
        response = {
            'message': 'Our chain was replaced'
        }
    else:
        response = {
            'message': 'Our chain is authoritative'
        }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    '''A mining API'''
    new_block = blockchain.mine(myWallet)
    for node in blockchain.nodes:
        try:
            requests.get('http://' + node + '/consensus')
        except:
            continue
    response = {
        'index': new_block.index,
        'transactions': new_block.transaction,
        'timestamp': new_block.timestamp,
        'previous_hash': new_block.previous_hash,
        'hash': new_block.hash,
        'merkle_root': new_block.merkle_root,
        'nonce': new_block.nonce,
        'difficulty': new_block.difficulty
    }
    return jsonify(response), 200

# ----------------------------------------------------------------------------------------------------------------------
# New APIs beyond EE4017 Lab 6


@app.route('/merkle_path', methods=['POST'])
def merkle_path():
    values = request.form
    required = ['sender', 'recipient', 'value']
    # Check that the required fields are in the POST data
    if not all(k in values for k in required):
        return 'Missing values', 400
    transaction = Transaction(values.get('sender'), values.get('recipient'), values.get('value'))
    if values.get('signature'):
        transaction.signature = values.get('signature')
    path = blockchain.merkle_path(transaction)

    if len(path) > 0:
        root = path[-1]
        path = path[:-1]
    return jsonify(path), 200


@app.route('/partial_validation', methods=['POST'])
def partial_validation():
    values = request.form
    required = ['root', 'path', 'sender', 'recipient', 'value']
    # Check that the required fields are in the POST data
    if not all(k in values for k in required):
        return 'Missing values', 400
    root = values.get('root')
    path = json.loads(values.get('path'))
    transaction = Transaction(values.get('sender'), values.get('recipient'), values.get('value'))
    if values.get('signature'):
        transaction.signature = values.get('signature')
    h = sha256(str(transaction.to_json()).encode()).hexdigest()
    new_root = blockchain.partialValidation(path, h)
    result = root == new_root
    return jsonify(result), 200


@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return "Shutting down...", 200


@app.errorhandler(404)
def not_found(error):
    return "Not found", 404


@app.errorhandler(405)
def method_not_allowed(error):
    return "Method not allowed", 405

@app.errorhandler(500)
def internal_server_error(error):
    return "Internal server error", 500
  
# ----------------------------------------------------------------------------------------------------------------------
# Main method: run the Flask object.
if __name__ == "__main__":
    # dummy_trans = Transaction(myWallet.pubkey, "professor", 4.0)
    # dummy_trans.add_signature(myWallet.sign_transaction(dummy_trans))
    # blockchain.add_new_transaction(dummy_trans)
    # blockchain.mine(myWallet)
    # bal = blockchain.check_balance(myWallet.pubkey)
    # print(bal)
    # prnt(blockchain.last_block, enable=False)
    # port = 5000

    port = int(sys.argv[1])
    print(port)
    app.run(host='127.0.0.1', port=port, debug=True)
