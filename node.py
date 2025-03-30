# import json, os, logging
# from flask import Flask, request, render_template
# from blockchain import Blockchain

# # Cấu hình logging để ghi log vào file
# logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Tạo ứng dụng Flask
# app = Flask(__name__)
# # Khởi tạo blockchain
# blockchain = Blockchain()

# @app.before_request
# def log_request_info():
#     try:
#         data = request.get_json(silent=True)  # Không báo lỗi nếu request không phải JSON
#     except Exception:
#         data = None
#     logging.info(f"Request: {request.method} {request.url} - Data: {data}")

# # Trang chủ
# @app.route('/', methods=['GET'])
# def home():
#     return render_template('home.html')

# # Đào block mới
# @app.route('/mine', methods=['GET'])
# def mine():
#     last_block = blockchain.get_previous_block()
#     proof = blockchain.proof_of_work(last_block['proof'])
#     block = blockchain.create_block(proof, blockchain.hash(last_block))
#     return {'message': 'New Block Mined!', 'block': block}, 200

# # Lấy toàn bộ blockchain
# @app.route('/chain', methods=['GET'])
# def get_chain():
#     return render_template('status.html', chain=blockchain.chain)

# # Thêm giao dịch mới
# @app.route('/transaction', methods=['POST'])
# def add_transaction():
#     data = request.get_json()
#     if not data or 'sender' not in data or 'receiver' not in data or 'amount' not in data:
#         return {'error': 'Invalid transaction data'}, 400
    
#     index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
#     return {'message': f'Transaction added to block {index}'}, 201

# # Xem log của server
# @app.route('/logs', methods=['GET'])
# def get_logs():
#     try:
#         with open("server.log", "r") as log_file:
#             logs = log_file.readlines()[-20:]  # Lấy 20 dòng log gần nhất
#         return {"logs": logs}, 200
#     except Exception as e:
#         return {"error": str(e)}, 500

# # Chạy server
# if __name__ == '__main__':
#     port = int(os.getenv("PORT", 5000))
#     app.run(host='0.0.0.0', port=port, debug=True)
import json, os, logging, traceback
from flask import Flask, request, render_template, jsonify
from blockchain import Blockchain

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
blockchain = Blockchain()

@app.before_request
def log_request_info():
    data = None
    if request.method in ["POST", "PUT", "PATCH"]:  # Chỉ lấy JSON khi request có thể chứa JSON
        try:
            data = request.get_json(silent=True)
        except Exception:
            data = None
    logging.info(f"Request: {request.method} {request.url} - Data: {data}")

# @app.route('/', methods=['GET'])
# def home():
#     # return render_template('home.html')
#     # print(f"Received request with Content-Type: {request.content_type}")  # Debug
#     # return "<h1>Trang chủ Blockchain</h1>"  # Tạm thời thay vì render_template
#     print(f"Request headers: {request.headers}")
    
#     if request.content_type and request.content_type != "text/html":
#         return jsonify({'error': f'Invalid Content-Type: {request.content_type}'}), 415

#     return render_template('home.html') 
@app.route('/', methods=['GET', 'HEAD'])
def home():
    # print(f"Request method: {request.method}")
    # print(f"Request headers: {request.headers}")

    # # Chỉ kiểm tra Content-Type nếu request không phải GET hoặc HEAD
    # if request.method not in ["GET", "HEAD"] and request.content_type and request.content_type != "application/json":
    #     return jsonify({'error': f'Invalid Content-Type: {request.content_type}'}), 415

    # return render_template('home.html')
    # return "API is running!", 200
    # return jsonify({"message": "API is running!"}), 200
    print(f"Request headers: {request.headers}")  # Debug request headers
    return render_template('home.html')
@app.route('/mine', methods=['GET'])
def mine():
    # last_block = blockchain.get_previous_block()
    # proof = blockchain.proof_of_work(last_block['proof'])
    # block = blockchain.create_block(proof, blockchain.hash(last_block))
    # return jsonify({'message': 'New Block Mined!', 'block': block}), 200
    # try:
    #     block = blockchain.mine_block()  # Gọi hàm đào block
    #     print(f"Block vừa được đào: {block}")  # Debug log
    #     return render_template('mine.html', block=block)
    # except Exception as e:
    #     print(f"Lỗi khi render templates: {e}")
    #     return "Lỗi hiển thị blockchain", 500
    try:
        last_block = blockchain.get_previous_block()  # Lấy block cuối cùng
        proof = blockchain.proof_of_work(last_block['proof'])  # Tìm proof mới
        previous_hash = blockchain.hash(last_block)  # Hash của block trước
        block = blockchain.create_block(proof, previous_hash)  # Tạo block mới

        print(f"Block vừa được đào: {block}")  # Debug log
        return render_template('mine.html', block=block)
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"Lỗi khi đào block:\n{error_msg}")
        return f"Lỗi hệ thống:<br><pre>{error_msg}</pre>", 500
@app.route('/chain', methods=['GET'])
def get_chain():
    try:
        print("Blockchain hiện tại:", json.dumps(blockchain.chain, indent=4, ensure_ascii=False))  # Hiển thị Unicode rõ ràng
        return render_template('status.html', chain=blockchain.chain)
    except Exception as e:
        error_message = f"Lỗi khi render template: {e}\n{traceback.format_exc()}"
        print(error_message)  # Xuất lỗi ra terminal

        # Ghi log lỗi với UTF-8 để tránh lỗi UnicodeEncodeError
        with open("error.log", "w", encoding="utf-8") as log_file:
            log_file.write(error_message + "\n")

        return f"<pre>{error_message}</pre>", 500
    
@app.route('/transaction', methods=['POST'])
def add_transaction():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 415
    
    try:
        data = request.get_json()
        if not data or 'sender' not in data or 'receiver' not in data or 'amount' not in data:
            return jsonify({'error': 'Invalid transaction data'}), 400
        
        index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
        return jsonify({'message': f'Transaction added to block {index}'}), 201
    except Exception as e:
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
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
