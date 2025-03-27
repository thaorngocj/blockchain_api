# Khai báo thư viện sẽ sử dụng 
import hashlib, json  

def hash_data(data):
    """Tạo hash SHA-256 cho dữ liệu"""  
    # Chuyển đổi dữ liệu thành chuỗi JSON có thứ tự khóa cố định và mã hóa thành bytes
    encoded_data = json.dumps(data, sort_keys=True).encode() 
    # Tạo hash SHA-256 cho dữ liệu đã mã hóa và trả về chuỗi hash
    return hashlib.sha256(encoded_data).hexdigest() 

def validate_proof(previous_proof, new_proof):
    """Kiểm tra Proof of Work hợp lệ"""  
    guess = f'{previous_proof}{new_proof}'.encode()  # Ghép hai giá trị proof thành một chuỗi và mã hóa thành bytes
    guess_hash = hashlib.sha256(guess).hexdigest()  # Tạo hash SHA-256 từ chuỗi proof
    return guess_hash[:4] == "0000"  # Kiểm tra nếu hash bắt đầu bằng "0000" thì proof hợp lệ, ngược lại thì không hợp lệ
