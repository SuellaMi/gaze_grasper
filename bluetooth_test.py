import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 22
server_sock.bind(("", port))
server_sock.listen(1)
client_sock, address = server_sock.accept()
print("Connection established with: ", address)
