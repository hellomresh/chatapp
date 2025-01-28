import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

# Replace with the server's IP address
SERVER_HOST = '192.168.193.202'  # Replace with the actual server IP
SERVER_PORT = 12345

# Initialize the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to the server.")
except ConnectionRefusedError:
    messagebox.showerror("Connection Error", "Could not connect to the server.")
    exit()

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            display_message(f"Server: {message}")
        except ConnectionResetError:
            display_message("Server disconnected.")
            break

# Function to display messages in the GUI
def display_message(message):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, message + "\n")
    chat_area.config(state='disabled')
    chat_area.yview(tk.END)  # Scroll to the bottom

# Function to send messages to the server
def send_message():
    message = message_entry.get()
    if message:
        client_socket.send(message.encode('utf-8'))
        display_message(f"You: {message}")
        message_entry.delete(0, tk.END)

# Setting up the GUI window
root = tk.Tk()
root.title("Client Chat")

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

# Start the thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Run the GUI event loop
root.mainloop()
