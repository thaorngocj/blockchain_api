import json, os, logging
from flask import Flask, request, render_template
from blockchain import Blockchain

# Cấu hình logging để ghi log vào file
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Tạo ứng dụng Flask
app = Flask(__name__)
# Khởi tạo blockchain
blockchain = Blockchain()

@app.before_request
def log_request_info():
    logging.info(f"Request: {request.method} {request.url} - Data: {request.get_json()}")

# Trang chủ
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Đào block mới
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(last_block['proof'])
    block = blockchain.create_block(proof, blockchain.hash(last_block))
    return {'message': 'New Block Mined!', 'block': block}, 200

# Lấy toàn bộ blockchain
@app.route('/chain', methods=['GET'])
def get_chain():
    return render_template('status.html', chain=blockchain.chain)

# Thêm giao dịch mới
@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    if not data or 'sender' not in data or 'receiver' not in data or 'amount' not in data:
        return {'error': 'Invalid transaction data'}, 400
    
    index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
    return {'message': f'Transaction added to block {index}'}, 201

# Xem log của server
@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open("server.log", "r") as log_file:
            logs = log_file.readlines()[-20:]  # Lấy 20 dòng log gần nhất
        return {"logs": logs}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# Chạy server
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
