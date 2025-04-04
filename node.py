import json, os, logging, traceback  # Các thư viện cần thiết cho việc xử lý JSON, cấu hình hệ thống, ghi log, và xử lý ngoại lệ.
from flask import Flask, request, render_template, jsonify, redirect  # Import các phương thức của Flask như tạo ứng dụng, yêu cầu HTTP, render template, JSON, và redirect.
from blockchain import Blockchain  # Import lớp Blockchain từ file blockchain.py để sử dụng trong ứng dụng.
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')  # Cấu hình ghi log vào file server.log, mức log là INFO.

app = Flask(__name__)  # Khởi tạo ứng dụng Flask.
blockchain = Blockchain()  # Tạo một đối tượng blockchain để quản lý dữ liệu blockchain.

@app.before_request
def log_request_info():
    data = None  # Khởi tạo biến data để lưu dữ liệu yêu cầu.
    if request.method in ["POST", "PUT", "PATCH"]:  # Kiểm tra xem phương thức yêu cầu có phải là POST, PUT hoặc PATCH không.
        try:
            data = request.get_json(silent=True)  # Nếu là JSON, lấy dữ liệu JSON từ yêu cầu.
        except Exception:
            data = None  # Nếu có lỗi khi lấy dữ liệu JSON, gán data = None.
    logging.info(f"Request: {request.method} {request.url} - Data: {data}")  # Ghi log thông tin yêu cầu.

@app.route('/', methods=['GET', 'HEAD'])
def home():
    print(f"Request headers: {request.headers}")  # In ra các header của yêu cầu, dùng cho mục đích debug.
    return render_template('home.html')  # Render và trả về template 'home.html' cho trang chủ.

# @app.route('/mine', methods=['GET'])
# def mine():
#     if blockchain.transactions:  # Kiểm tra xem có giao dịch chưa được đào không.
#         previous_block = blockchain.get_previous_block()  # Lấy khối trước đó trong blockchain.
#         previous_proof = previous_block['proof']  # Lấy proof của khối trước đó.

#         proof = blockchain.proof_of_work(previous_proof)  # Tính toán proof-of-work cho khối mới.
#         previous_hash = blockchain.hash(previous_block)  # Tính toán hash của khối trước đó.

#         block = blockchain.create_block(proof, previous_hash)  # Tạo block mới và thêm vào blockchain.
        
#         blockchain.transactions = []  # Làm sạch danh sách giao dịch sau khi đã tạo block.

#         return render_template('mine.html', message="Block đã được tạo!", block=block)  # Render template 'mine.html' và hiển thị thông báo thành công.
#     else:
#         return render_template('mine.html', message="Không có giao dịch để đào.")  # Nếu không có giao dịch, hiển thị thông báo không có giao dịch để đào.

@app.route('/mine', methods=['GET'])
def mine():
    if blockchain.transactions:  # Kiểm tra xem có giao dịch chưa được đào không.
        previous_block = blockchain.get_previous_block()  # Lấy khối trước đó trong blockchain.
        previous_proof = previous_block['proof']  # Lấy proof của khối trước đó.

        proof = blockchain.proof_of_work(previous_proof)  # Tính toán proof-of-work cho khối mới.
        previous_hash = blockchain.hash(previous_block)  # Tính toán hash của khối trước đó.

        # Tạo block mới và thêm vào blockchain.
        block = blockchain.create_block(proof, previous_hash)

        print(f"Block đã được tạo: {block}")  # In ra khối mới tạo để kiểm tra.

        blockchain.transactions = []  # Làm sạch danh sách giao dịch sau khi đã tạo block.

        # In ra chuỗi blockchain để kiểm tra.
        print("Blockchain hiện tại:", json.dumps(blockchain.chain, indent=4, ensure_ascii=False))

        return render_template('mine.html', message="Block đã được tạo!", block=block)
    else:
        return render_template('mine.html', message="Không có giao dịch để đào.")

@app.route('/chain', methods=['GET'])
def get_chain():
    try:
        print("Blockchain hiện tại:", json.dumps(blockchain.chain, indent=4, ensure_ascii=False))  # In ra blockchain hiện tại dưới dạng JSON đẹp.
        return render_template('status.html', chain=blockchain.chain)  # Render template 'status.html' để hiển thị trạng thái của blockchain.
    except Exception as e:
        error_message = f"Lỗi khi render template: {e}\n{traceback.format_exc()}"  # Xử lý ngoại lệ và ghi lại lỗi.
        print(error_message)  # In lỗi ra console.
        
        with open("error.log", "w", encoding="utf-8") as log_file:  # Mở file log lỗi và ghi lỗi vào đó.
            log_file.write(error_message + "\n")

        return f"<pre>{error_message}</pre>", 500  # Trả về thông báo lỗi dạng HTML và mã lỗi 500.

# @app.route('/transaction', methods=['GET', 'POST'])
# def add_transaction():
#     if request.method == 'GET':
#         return render_template('transaction.html')  # Nếu yêu cầu GET, trả về form giao dịch để người dùng nhập dữ liệu.
#     if request.method == 'POST':
#         try:
#             if request.is_json:  # Kiểm tra nếu dữ liệu yêu cầu là dạng JSON.
#                 data = request.get_json()  # Lấy dữ liệu JSON.
#             else:
#                 data = request.form  # Nếu không phải JSON, lấy từ form gửi lên.

#             print("Received Data:", data)  # In ra dữ liệu nhận được từ form hoặc JSON cho mục đích debug.

#             # Kiểm tra dữ liệu hợp lệ (có sender, receiver, amount).
#             if 'sender' not in data or 'receiver' not in data or 'amount' not in data:
#                 return jsonify({'error': 'Invalid transaction data'}), 400  # Nếu thiếu dữ liệu, trả về lỗi.

#             sender = data['sender']  # Lấy thông tin sender.
#             receiver = data['receiver']  # Lấy thông tin receiver.
#             amount = int(data['amount'])  # Lấy số tiền giao dịch và chuyển thành integer.

#             # Thêm giao dịch vào blockchain và trả về vị trí khối tiếp theo.
#             index = blockchain.add_transaction(sender, receiver, amount)
#             print(f"Transaction added to block {index}")  # In thông tin giao dịch đã được thêm.

#             return redirect('/mine')  # Sau khi thêm giao dịch, chuyển hướng người dùng tới trang mine để đào block mới.

#         except Exception as e:
#             print("Error:", str(e))  # In ra lỗi nếu có lỗi trong quá trình xử lý giao dịch.
#             return jsonify({'error': str(e)}), 500  # Trả về lỗi dưới dạng JSON.

# @app.route('/transaction', methods=['GET', 'POST'])
# def add_transaction():
#     if request.method == 'GET':
#         return render_template('transaction.html')  # Nếu yêu cầu GET, trả về form giao dịch để người dùng nhập dữ liệu.
    
#     if request.method == 'POST':
#         try:
#             # if request.is_json:  # Kiểm tra nếu dữ liệu yêu cầu là dạng JSON.
#             #     data = request.get_json()  # Lấy dữ liệu JSON.
#             # else:
#             #     data = request.form  # Nếu không phải JSON, lấy từ form gửi lên.
#             data = request.get_json(silent=True) or request.form


#             print("Received Data:", data)  # In ra dữ liệu nhận được từ form hoặc JSON cho mục đích debug.

#             # Kiểm tra dữ liệu hợp lệ (có sender, receiver, amount).
#             if 'sender' not in data or 'receiver' not in data or 'amount' not in data:
#                 return jsonify({'error': 'Invalid transaction data'}), 400  # Nếu thiếu dữ liệu, trả về lỗi.

#             sender = data['sender']  # Lấy thông tin sender.
#             receiver = data['receiver']  # Lấy thông tin receiver.
            
#             # Kiểm tra và chuyển đổi amount thành integer, xử lý trường hợp không hợp lệ.
#             try:
#                 amount = int(data['amount'])
#             except ValueError:
#                 return jsonify({'error': 'Amount must be a valid number'}), 400  # Nếu amount không phải là số hợp lệ, trả về lỗi.

#             # Thêm giao dịch vào blockchain và trả về vị trí khối tiếp theo.
#             index = blockchain.add_transaction(sender, receiver, amount)
#             print(f"Transaction added to block {index}")  # In thông tin giao dịch đã được thêm.
            
#             return redirect('/mine')  # Sau khi thêm giao dịch, chuyển hướng người dùng tới trang mine để đào block mới.

#         except Exception as e:
#             print("Error:", str(e))  # In ra lỗi nếu có lỗi trong quá trình xử lý giao dịch.
#             return jsonify({'error': str(e)}), 500  # Trả về lỗi dưới dạng JSON.

@app.route('/transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'GET':
        return render_template('transaction.html')  # Trả về form giao dịch

    if request.method == 'POST':
        try:
            # Kiểm tra xem có phải là JSON hay dữ liệu từ form
            data = request.get_json(silent=True) or request.form

            print("Received Data:", data)  # In dữ liệu nhận được cho debug

            # Kiểm tra tính hợp lệ của dữ liệu (có sender, receiver và amount)
            if 'sender' not in data or 'receiver' not in data or 'amount' not in data:
                return jsonify({'error': 'Invalid transaction data'}), 400  # Nếu thiếu dữ liệu, trả về lỗi

            sender = data['sender']  # Lấy thông tin sender
            receiver = data['receiver']  # Lấy thông tin receiver

            # Kiểm tra và chuyển đổi amount thành integer
            try:
                amount = int(data['amount'])
            except ValueError:
                return jsonify({'error': 'Amount must be a valid number'}), 400  # Nếu amount không hợp lệ

            # Thêm giao dịch vào blockchain
            index = blockchain.add_transaction(sender, receiver, amount)
            print(f"Transaction added to block {index}")  # In thông tin giao dịch đã được thêm

            # Sau khi thêm giao dịch, chuyển hướng tới trang mine để đào block mới
            return redirect('/mine')  # Chuyển hướng đến trang mine

        except Exception as e:
            print("Error:", str(e))  # In ra lỗi nếu có sự cố
            return jsonify({'error': str(e)}), 500  # Trả về lỗi dưới dạng JSON

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        with open("server.log", "r") as log_file:  # Mở file log và đọc 20 dòng cuối.
            logs = log_file.readlines()[-20:]
        return jsonify({"logs": logs}), 200  # Trả về các dòng log dưới dạng JSON.
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Nếu có lỗi, trả về lỗi dưới dạng JSON.

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))  # Lấy port từ biến môi trường, mặc định là 5000.
    app.run(host='0.0.0.0', port=port, debug=True)  # Chạy ứng dụng Flask trên tất cả các địa chỉ IP (0.0.0.0) và port đã chỉ định, bật chế độ debug.

