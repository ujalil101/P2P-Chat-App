import socket
import tkinter as tk
from threading import Thread
import datetime

def receive_message():
    while True:
        try:
            # Receive message from server
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                # Split the message and timestamp
                split_message = message.rsplit('(', 1)
                content = split_message[0].rstrip()
                timestamp = split_message[1] if len(split_message) > 1 else ""

                # Calculate padding to align timestamp to the right
                padding = " " * (msg_listbox.winfo_width() - len(content) - len(timestamp))

                # Display the received message in the chat window with timestamp aligned to the right
                msg_listbox.insert(tk.END, f"{content}{padding}{timestamp}")
        except OSError:
            # Possibly server has closed the connection
            break


def send_message(event=None):
    # Get the message from the entry widget
    message = my_msg.get()
    my_msg.set("")  # Clear the input field

    # Calculate timestamp
    timestamp = datetime.datetime.now().strftime(" (%I:%M %p)")

    # Calculate padding to align timestamp to the right
    padding = " " * (msg_listbox.winfo_width() - len(f"You: {message}") - len(timestamp))

    # Display the sent message in the chat window with timestamp aligned to the right
    msg_listbox.insert(tk.END, f"You: {message}{padding}{timestamp}")

    # Send the message to the server
    client_socket.send(message.encode("utf-8"))


def on_closing(event=None):
    # When the window is closed, send "close" to the server and close the connection
    my_msg.set("close")
    send_message()
    root.destroy()

def run_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  # Replace with the server's IP address
    server_port = 8000  # Replace with the server's port number

    # Establish connection with server
    client_socket.connect((server_ip, server_port))

    # Get username from the user
    username = input("Enter your username: ")
    client_socket.send(username.encode("utf-8"))

    # Create a GUI window
    global root
    root = tk.Tk()
    root.title("Chat App")

    # Create a frame to hold the messages
    messages_frame = tk.Frame(root)
    scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages

    # Listbox to display messages
    global msg_listbox
    msg_listbox = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    msg_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    msg_listbox.pack()
    messages_frame.pack()

    # Create an entry widget to input messages
    global my_msg
    my_msg = tk.StringVar()  # For the messages to be sent
    entry_field = tk.Entry(root, textvariable=my_msg)
    entry_field.bind("<Return>", send_message)
    entry_field.pack()
    entry_field.focus()

    # Create a send button to send messages
    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack()

    # Handle window closing event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start a thread to receive messages from the server
    receive_thread = Thread(target=receive_message)
    receive_thread.start()

    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    run_client()