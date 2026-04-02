from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def encrypt_logic(key, text):
    key_len = len(key)
    rows = math.ceil(len(text) / key_len)
    text += "X" * (rows * key_len - len(text)) # Padding
    matrix = [text[i:i + key_len] for i in range(0, len(text), key_len)]
    key_indices = sorted(range(len(key)), key=lambda k: key[k])
    return "".join("".join(matrix[row][col] for row in range(rows)) for col in key_indices)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    text = data.get('text', '')
    key = data.get('key', '')
    mode = data.get('mode', 'encrypt')
    
    if not text or not key:
        return jsonify({"error": "Thiếu dữ liệu"}), 400
        
    result = encrypt_logic(key, text) if mode == 'encrypt' else decrypt_logic(key, text)
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)