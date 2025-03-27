# Khai báo các thư viện cần sử dụng
import hashlib, json, time  
# Import Flask để tạo API
from flask import Flask, request  

class Blockchain:
    def __init__(self):
        self.chain = []  # Danh sách chứa các block trong chuỗi
        self.transactions = []  # Danh sách các giao dịch đang chờ xử lý
        self.create_block(proof=1, previous_hash='0')  # Tạo block khởi đầu (Genesis Block)
    
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,  # Vị trí của block trong chuỗi
            'timestamp': time.time(),  # Thời gian tạo block
            'transactions': self.transactions,  # Danh sách giao dịch trong block
            'proof': proof,  # Giá trị proof-of-work của block
            'previous_hash': previous_hash  # Hash của block trước đó
        }
        self.transactions = []  # Xóa danh sách giao dịch sau khi được thêm vào block
        self.chain.append(block)  # Thêm block vào chuỗi khối
        return block  # Trả về block vừa tạo
    
    def get_previous_block(self):
        return self.chain[-1]  # Lấy block cuối cùng trong chuỗi
    
    def proof_of_work(self, previous_proof):
        new_proof = 1  # Bắt đầu thử nghiệm giá trị proof từ 1
        while not self.valid_proof(previous_proof, new_proof):  # Kiểm tra xem proof có hợp lệ không
            new_proof += 1  # Nếu không, tăng giá trị proof và thử lại
        return new_proof  # Khi tìm được proof hợp lệ, trả về giá trị này
    
    def valid_proof(self, previous_proof, new_proof):
        guess = f'{previous_proof}{new_proof}'.encode()  # Ghép 2 giá trị proof lại và mã hóa thành bytes
        guess_hash = hashlib.sha256(guess).hexdigest()  # Băm dữ liệu bằng SHA-256
        return guess_hash[:4] == "0000"  # Kiểm tra xem hash có bắt đầu bằng "0000" không (độ khó của thuật toán)
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()  # Chuyển block thành chuỗi JSON và mã hóa
        return hashlib.sha256(encoded_block).hexdigest()  # Tạo hash bằng SHA-256 và trả về
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,  # Người gửi
            'receiver': receiver,  # Người nhận
            'amount': amount  # Số tiền giao dịch
        })
        return self.get_previous_block()['index'] + 1  # Trả về index của block tiếp theo dự kiến chứa giao dịch này
