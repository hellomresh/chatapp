import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Define server IP and port
SERVER_HOST = '0.0.0.0'  # Listen on all available network interfaces
SERVER_PORT = 12345

# Initialize and bind the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Server is listening on {SERVER_HOST}:{SERVER_PORT}")
except OSError as e:
    messagebox.showerror("Socket Error", f"Unable to start server: {e}")
    exit()

client_socket = None  # Declare client_socket as a global variable

# Function to handle the client connection
def handle_client():
    global client_socket
    client_socket, client_address = server_socket.accept()
    display_message(f"Connected to {client_address}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                display_message(f"Client: {message}")
        except ConnectionResetError:
            display_message("Client disconnected.")
            client_socket = None  # Reset client_socket if the client disconnects
            break

# Function to display messages in the GUI
def display_message(message):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, message + "\n")
    chat_area.config(state='disabled')
    chat_area.yview(tk.END)  # Scroll to the bottom

# Function to send messages to the client
def send_message():
    global client_socket
    message = message_entry.get()
    if client_socket and message:
        client_socket.send(message.encode('utf-8'))
        display_message(f"You: {message}")
        message_entry.delete(0, tk.END)
    elif not client_socket:
        messagebox.showwarning("Connection Warning", "No client connected.")

# Setting up the GUI window
root = tk.Tk()
root.title("Server Chat Host")

# Chat display area
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state='disabled')
chat_area.pack(padx=10, pady=10)

# Message entry box
message_entry = tk.Entry(root, width=40)
message_entry.pack(padx=10, pady=5, side=tk.LEFT)

# Bind the Enter key to send_message
message_entry.bind("<Return>", lambda event: send_message())

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(padx=5, pady=5, side=tk.RIGHT)

# Start the thread to accept a client connection
thread = threading.Thread(target=handle_client)
thread.daemon = True
thread.start()

# Run the GUI event loop
root.mainloop()
