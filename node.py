import json, os, logging, traceback
from flask import Flask, request, render_template, jsonify, redirect
from blockchain import Blockchain
from waitress import serve

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)  # Khởi tạo ứng dụng Flask.
blockchain = Blockchain()  # Tạo một đối tượng blockchain để quản lý dữ liệu blockchain.

@app.before_request
def log_request_info():
    data = None
    if request.method in ["POST", "PUT", "PATCH"]:
        try:
            data = request.get_json(silent=True)
        except Exception:
            data = None
    logging.info(f"Request: {request.method} {request.url} - Data: {data}")

@app.route('/', methods=['GET', 'HEAD'])
def home():
    print(f"Request headers: {request.headers}")
    return render_template('home.html')

@app.route('/mine', methods=['GET'])
def mine():
    if blockchain.transactions:
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash)
        
        print(f"Block đã được tạo: {block}")
        blockchain.transactions = []
        print("Blockchain hiện tại:", json.dumps(blockchain.chain, indent=4, ensure_ascii=False))

        return render_template('mine.html', message="Block đã được tạo!", block=block)
    else:
        return render_template('mine.html', message="Không có giao dịch để đào.")

@app.route('/chain', methods=['GET'])
def get_chain():
    try:
        print("Blockchain hiện tại:", json.dumps(blockchain.chain, indent=4, ensure_ascii=False))
        return render_template('status.html', chain=blockchain.chain)
    except Exception as e:
        error_message = f"Lỗi khi render template: {e}\n{traceback.format_exc()}"
        print(error_message)
        
        with open("error.log", "w", encoding="utf-8") as log_file:
            log_file.write(error_message + "\n")

        return f"<pre>{error_message}</pre>", 500

@app.route('/transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template('transaction.html')

    if request.method == 'POST':
        try:
            data = request.get_json(silent=True) or request.form

            print("Received Data:", data)

            if 'sender' not in data or 'receiver' not in data or 'amount' not in data:
                return jsonify({'error': 'Invalid transaction data'}), 400

            sender = data['sender']
            receiver = data['receiver']
            
            try:
                amount = int(data['amount'])
            except ValueError:
                return jsonify({'error': 'Amount must be a valid number'}), 400

            index = blockchain.add_transaction(sender, receiver, amount)
            print(f"Transaction added to block {index}")

            return redirect('/mine')

        except Exception as e:
            print("Error:", str(e))
            return jsonify({'error': str(e)}), 500

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open("server.log", "r") as log_file:
            logs = log_file.readlines()[-20:]
        return jsonify({"logs": logs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Không dùng app.run() khi sử dụng Gunicorn
    pass
