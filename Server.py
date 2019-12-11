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

app = Flask(__name__)
myWallet = Wallet()
blockchain = Blockchain(myWallet)


@app.route('/status', methods=['GET'])
def status():
    if myWallet and blockchain:
        return "alive", 200
    return "dead", 400


@app.route('/register_node', methods=['POST'])
def register_node():
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
    node_list = requests.get('http://' + node + '/get_nodes')
    if node_list.status_code == 200:
        node_list = node_list.json()['nodes']
        for node in node_list:
            blockchain.register_node(node)
    for new_nodes in blockchain.nodes:
        # Sending type B request
        requests.post('http://' + new_nodes + '/register_node', data={'com_port': str(port)})
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
    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def part_chain():
    response = {
        'chain': json.dumps(blockchain.chain[-10:]),
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/fullchain', methods=['GET'])
def full_chain():
    response = {
        'chain': json.dumps(blockchain.chain),
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/lightweight', methods=['GET'])
def lightweight():
    fullchain = [json.loads(block) for block in blockchain.chain]
    lightweight = []
    for block in fullchain:
        block_object = Block(block['index'], block['transaction'], block['timestamp'], block['previous_hash'])
        block_object.merkle_root = block['merkle_root']
        block_object.nonce = block['nonce']
        lightweight.append(block_object.to_dict())
    response = {
        'chain': json.dumps(lightweight),
        'length': len(lightweight)
    }
    return jsonify(response), 200


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
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


@app.route('/get_transactions', methods=['GET'])
def get_transactions():
    # Get transactions from transactions pool
    transactions = json.dumps(blockchain.unconfirmed_transactions)
    response = {'transactions': transactions}
    return jsonify(response), 200


@app.route('/consensus', methods=['GET'])
def consensus():
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
    new_block = blockchain.mine(myWallet)
    for node in blockchain.nodes:
        requests.get('http://' + node + '/consensus')
    response = {
        'index': new_block.index,
        'transactions': new_block.transaction,
        'timestamp': new_block.timestamp,
        'previous_hash': new_block.previous_hash,
        'hash': new_block.hash,
        'merkle_root': new_block.merkle_root,
        'nonce': new_block.nonce,
    }
    return jsonify(response), 200


@app.route('/merkle_path', methods=['POST'])
def merkle_path():
    values = request.form
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
