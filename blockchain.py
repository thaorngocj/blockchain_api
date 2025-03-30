import hashlib
import json
import time
from flask import Flask, request

class Blockchain:
    def __init__(self):
        self.chain = []  # Danh sách chứa các block trong chuỗi
        self.transactions = []  # Danh sách các giao dịch đang chờ xử lý
        self.create_block(proof=1, previous_hash='0')  # Tạo block khởi đầu (Genesis Block)
    
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions.copy(),  # Sao chép danh sách giao dịch trước khi thêm vào block
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)  # Đưa block vào blockchain trước khi xóa danh sách giao dịch
        self.transactions = []  # Reset danh sách giao dịch sau khi đã ghi vào block
        return block
    
    def get_previous_block(self):
        # return self.chain[-1]  # Lấy block cuối cùng trong chuỗi
        return json.loads(json.dumps(self.chain[-1], ensure_ascii=False))
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        while not self.valid_proof(previous_proof, new_proof):
            new_proof += 1
        return new_proof
    
    def valid_proof(self, previous_proof, new_proof):
        guess = f'{previous_proof}{new_proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # def add_transaction(self, sender, receiver, amount):
    #     self.transactions.append({
    #         'sender': sender,
    #         'receiver': receiver,
    #         'amount': amount
    #     })
    #     return self.get_previous_block()['index'] + 1  # Block tiếp theo dự kiến chứa giao dịch này
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return True 