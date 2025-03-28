import json, os
from flask import Flask, request, jsonify
from blockchain import Blockchain

# Tạo ứng dụng Flask
app = Flask(__name__)
# Khởi tạo một blockchain mới
blockchain = Blockchain()

# Route trang chủ -> Truy cập http://127.0.0.1:5000/
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Blockchain App!'}), 200

# Route để đào một block mới -> Truy cập http://127.0.0.1:5000/mine
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(last_block['proof'])
    previous_hash = blockchain.hash(last_block)

    # Thêm phần thưởng cho thợ đào
    blockchain.add_transaction(sender="System", receiver="Miner", amount=10)

    # Tạo block mới
    block = blockchain.create_block(proof, previous_hash)
    
    return jsonify({'message': 'New Block Mined!', 'block': block}), 200

# Route để hiển thị toàn bộ blockchain -> Truy cập http://127.0.0.1:5000/chain
@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({'chain': blockchain.chain}), 200

# Route để thêm giao dịch mới -> Truy cập http://127.0.0.1:5000/transaction
@app.route('/transaction', methods=['POST'])
def add_transaction():
    if not request.is_json:
        return jsonify({'message': 'Request phải là JSON!'}), 400

    data = request.get_json()
    
    # Kiểm tra nếu thiếu dữ liệu
    required_fields = ['sender', 'receiver', 'amount']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Thiếu dữ liệu!'}), 400

    index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
    return jsonify({'message': f'Transaction added to block {index}'}), 201

# Chạy server Flask
if __name__ == '__main__':
    port = os.getenv("PORT")  # Lấy biến môi trường PORT
    try:
        port = int(port) if port else 5000
    except ValueError:
        port = 5000  # Nếu giá trị không hợp lệ, mặc định 5000

    app.run(host='0.0.0.0', port=port, debug=True)
