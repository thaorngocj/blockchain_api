import hashlib
import json
import time
from flask import Flask, request

class Blockchain:
    def __init__(self):
        self.chain = []  
        self.transactions = []  
        self.create_block(proof=1, previous_hash='0')  
    
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.transactions.copy(), 
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)  
        self.transactions = [] 
        return block
    
    def get_previous_block(self):
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
    #    self.transactions.append({
    #        'sender': sender,
    #        'receiver': receiver,
    #        'amount': amount
    #    })
    #    return self.get_previous_block()['index'] + 1  # Block tiếp theo dự kiến chứa giao dịch này
    
    # def add_transaction(self, sender, receiver, amount):
    #    self.transactions.append({
    #        'sender': sender,
    #        'receiver': receiver,
    #        'amount': amount
    #    })
    #    return True 
    
    # def add_transaction(self, sender, receiver, amount):
    #     transaction = {"sender": sender, "receiver": receiver, "amount": amount}
    #     self.transactions.append(transaction)
    #     return len(self.chain) + 1
    
    def add_transaction(self, sender, receiver, amount):
    # Thêm giao dịch vào danh sách giao dịch
        transaction = {"sender": sender, "receiver": receiver, "amount": amount}
        self.transactions.append(transaction)

        # Tạo một khối mới sau khi thêm giao dịch
        previous_block = self.get_previous_block()
        previous_proof = previous_block['proof']
        proof = self.proof_of_work(previous_proof)
        previous_hash = self.hash(previous_block)

        # Tạo block mới và thêm vào chain
        block = self.create_block(proof, previous_hash)

        return len(self.chain)  # Trả về số lượng block hiện tại (số khối đã tạo)
