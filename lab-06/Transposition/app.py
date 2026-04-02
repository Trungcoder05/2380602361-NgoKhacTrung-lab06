from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# --- THUẬT TOÁN MÃ HÓA ---
def encrypt_logic(key, text):
    key_len = len(key)
    rows = math.ceil(len(text) / key_len)
    # Thêm ký tự X cho đủ bảng
    text += "X" * (rows * key_len - len(text))
    matrix = [text[i:i + key_len] for i in range(0, len(text), key_len)]
    key_indices = sorted(range(len(key)), key=lambda k: key[k])
    result = ""
    for col in key_indices:
        for row in range(rows):
            result += matrix[row][col]
    return result

# --- THUẬT TOÁN GIẢI MÃ ---
def decrypt_logic(key, ciphertext):
    key_len = len(key)
    rows = math.ceil(len(ciphertext) / key_len)
    key_indices = sorted(range(len(key)), key=lambda k: key[k])
    matrix = [['' for _ in range(key_len)] for _ in range(rows)]
    curr_idx = 0
    for col in key_indices:
        for row in range(rows):
            matrix[row][col] = ciphertext[curr_idx]
            curr_idx += 1
    return "".join("".join(row) for row in matrix)

# --- ĐƯỜNG DẪN WEB ---
@app.route('/')
def index():
    # Flask sẽ tìm file này trong thư mục templates/
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '')
    key = data.get('key', '')
    mode = data.get('mode', 'encrypt')
    
    if mode == 'encrypt':
        res = encrypt_logic(key, text)
    else:
        res = decrypt_logic(key, text)
        
    return jsonify({"result": res})

# --- QUAN TRỌNG: DÒNG NÀY ĐỂ CHẠY SERVER ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)