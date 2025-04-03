import hashlib # Thư viện tính toán hash
import json # Thư viện xử lý dữ liệu json
import time # Thư viện làm việc với thời gian
from flask import Flask, request # Thư viện Flask cho ứng dụng web

class Blockchain:
    def __init__(self):
        self.chain = []  # Danh sách lưu trữ tất cả các khối trong blockchain.
        self.transactions = []  # Danh sách lưu trữ các giao dịch chờ để thêm vào khối.
        self.create_block(proof=1, previous_hash='0')  # Tạo khối đầu tiên (genesis block) với proof là 1 và previous_hash là '0'.
    
    def create_block(self, proof, previous_hash):
        # Hàm tạo một khối mới với proof và previous_hash được cung cấp
        block = {
            'index': len(self.chain) + 1,  # Tính toán chỉ số của khối mới (index).
            'timestamp': time.time(),  # Ghi lại thời gian tạo khối (timestamp).
            'transactions': self.transactions.copy(),  # Sao chép danh sách giao dịch hiện tại vào khối.
            'proof': proof,  # Ghi lại proof (được tính toán từ quá trình mining).
            'previous_hash': previous_hash  # Ghi lại hash của khối trước đó.
        }
        self.chain.append(block)  # Thêm khối mới vào blockchain (self.chain).
        self.transactions = []  # Làm sạch danh sách giao dịch sau khi đã tạo khối.
        return block  # Trả về khối mới tạo
    
    def get_previous_block(self):
        # Hàm trả về khối trước đó trong blockchain (khối cuối cùng).
        return json.loads(json.dumps(self.chain[-1], ensure_ascii=False))
    
    def proof_of_work(self, previous_proof):
        # Hàm tìm proof mới cho khối tiếp theo bằng cách thực hiện thuật toán proof-of-work
        new_proof = 1  # Khởi tạo proof ban đầu là 1.
        # Tiến hành tăng dần proof mới cho đến khi tìm được proof hợp lệ
        while not self.valid_proof(previous_proof, new_proof):
            new_proof += 1  # Tăng dần giá trị của proof nếu chưa hợp lệ.
        return new_proof  # Trả về proof hợp lệ tìm được.
    
    def valid_proof(self, previous_proof, new_proof):
        # Hàm kiểm tra tính hợp lệ của proof mới bằng cách tạo hash từ proof cũ và proof mới
        guess = f'{previous_proof}{new_proof}'.encode()  # Ghép nối proof cũ và proof mới và mã hóa thành bytes.
        guess_hash = hashlib.sha256(guess).hexdigest()  # Tính toán SHA256 của giá trị vừa mã hóa.
        # Kiểm tra xem hash có bắt đầu với 4 chữ số 0 hay không (có nghĩa là proof hợp lệ).
        return guess_hash[:4] == "0000"
    
    def hash(self, block):
        # Hàm tính toán hash của một block
        encoded_block = json.dumps(block, sort_keys=True).encode()  # Mã hóa khối thành định dạng JSON.
        return hashlib.sha256(encoded_block).hexdigest()  # Trả về hash SHA256 của khối đã mã hóa.
    
    def add_transaction(self, sender, receiver, amount):
        # Hàm thêm giao dịch vào danh sách giao dịch
        transaction = {
            "sender": sender, 
            "receiver": receiver, 
            "amount": amount
            }  # Tạo giao dịch dưới dạng dictionary.
        self.transactions.append(transaction)  # Thêm giao dịch vào danh sách giao dịch.

        # Không tạo block ngay tại đây
        return len(self.chain) + 1  # Trả về số khối hiện tại trong blockchain + 1, tức là vị trí của khối tiếp theo.

    def mine_block(self):
        # Hàm đào block mới
        previous_block = self.get_previous_block()  # Lấy khối trước đó từ blockchain.
        previous_proof = previous_block['proof']  # Lấy proof của khối trước đó.
        proof = self.proof_of_work(previous_proof)  # Tìm proof mới cho khối tiếp theo.
        previous_hash = self.hash(previous_block)  # Tính toán hash của khối trước đó.

        # Tạo khối mới và thêm vào blockchain
        block = self.create_block(proof, previous_hash)  # Tạo block mới với proof và previous_hash.
        
        # Làm sạch danh sách giao dịch sau khi tạo block mới
        self.transactions = []  # Sau khi block được tạo, danh sách giao dịch được làm sạch.
        return block  # Trả về khối mới tạo.

