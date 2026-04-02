import subprocess
from scapy.all import *

# Hàm lấy danh sách các giao diện mạng (interfaces) trên máy tính
def get_interfaces():
    # Chạy lệnh netsh để lấy danh sách interface trên Windows
    result = subprocess.run(["netsh", "interface", "show", "interface"], 
                            capture_output=True, text=True)
    output_lines = result.stdout.splitlines()[3:]
    # Tách lấy tên của interface từ kết quả trả về
    interfaces = [line.split()[-1] for line in output_lines if len(line.split()) >= 4]
    return interfaces

# Hàm xử lý mỗi gói tin khi bắt được
def packet_handler(packet):
    if packet.haslayer(Raw):
        print(f"Captured Packet: {str(packet)}")

# --- Chương trình chính ---

# 1. Lấy danh sách các giao diện mạng
interfaces = get_interfaces()

# 2. In danh sách để người dùng lựa chọn
print("Danh sách các giao diện mạng:")
for i, iface in enumerate(interfaces, start=1):
    print(f"{i}. {iface}")

# 3. Lựa chọn giao diện từ người dùng
choice = int(input("Chọn một giao diện mạng (nhập số): "))
selected_iface = interfaces[choice - 1]

# 4. Bắt đầu bắt gói tin trên giao diện đã chọn
print(f"Đang bắt gói tin trên: {selected_iface}...")
sniff(iface=selected_iface, prn=packet_handler, filter="tcp")