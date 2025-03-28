# Khai báo thư viện cần sử dụng
import json, os
from flask import Flask, request
from blockchain import Blockchain

# Tạo ứng dụng Flask
app = Flask(__name__)
# Khởi tạo một blockchain mới
blockchain = Blockchain()

# Route trang chủ -> Truy cập http://127.0.0.1:5000/ 
@app.route('/', methods=['GET'])
def home():
    # Thông báo của trang chủ
    return {'message': 'Welcome to the Blockchain App!'}, 200
# Route để đào một block mới -> Truy cập http://127.0.0.1:5000/mine
@app.route('/mine', methods=['GET'])
def mine():
    # Lấy block cuối cùng trong blockchain
    last_block = blockchain.get_previous_block()
    # Tìm proof hợp lệ
    proof = blockchain.proof_of_work(last_block['proof'])
     # Tạo block mới
    block = blockchain.create_block(proof, blockchain.hash(last_block))
    # Thông báo blockchain vừa đào được
    return {'message': 'New Block Mined!', 'block': block}, 200
# Route để hiển thị toàn bộ blockchain -> Truy cập http://127.0.0.1:5000/chain
@app.route('/chain', methods=['GET'])
def get_chain():
    # Hiển thị toàn bộ block
    return {'chain': blockchain.chain}, 200
# Route để thêm giao dịch mới -> Truy cập http://127.0.0.1:5000/transaction
@app.route('/transaction', methods=['POST'])
def add_transaction():
    try:
        # Lấy dữ liệu từ request json
        data = request.get_json()
    except:
        # Nếu request không có JSON, đọc dữ liệu từ file "data.json"
        with open('data.json', 'r') as file:
            data = json.load(file)
    # Thêm giao dịch vào danh sách chờ
    index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
    # Trả về giao dịch được thêm vào 
    return {'message': f'Transaction added to block {index}'}, 201
# Chạy server cổng 5000
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  
    app.run(host='0.0.0.0', port=port, debug=True)

# NOTE:
# curl -X POST http://127.0.0.1:5000/transaction -H "Content-Type: application/json" -d "{\"sender\": \"Alice\", \"receiver\": \"Bob\", \"amount\": 100}"
# curl -X POST http://127.0.0.1:5000/transaction
# curl -X GET http://127.0.0.1:5000/mine