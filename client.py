import sqlite3
import socket
import tkinter as tk
from threading import Thread
import datetime

# Database file
DATABASE_FILE = "chat_history.db"


def receive_message():
    while True:
        try:
            # receive message from server
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # save message to the database
                save_message_to_database(message, timestamp)

                # dispaly message
                if message.startswith("You:"):
                    # dispaly message
                    msg_listbox.insert(tk.END, f"{message[4:]} ({timestamp})")
                else:
                    # dispaly message
                    msg_listbox.insert(tk.END, f"{message} ({timestamp})")
        except OSError:
            break


def send_message(event=None):
    #get message
    message = my_msg.get()
    my_msg.set("") 

    # calc timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # display message
    msg_listbox.insert(tk.END, f"You: {message} ({timestamp})")

    # save msg
    save_message_to_database(f"You: {message}", timestamp)

    # send message to server
    client_socket.send(f"{message}".encode("utf-8"))

def save_message_to_database(message, timestamp):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # using parameterized query to insert message to prevent against  SQL injection attacks
    cursor.execute("INSERT INTO messages (message, timestamp) VALUES (?, ?)", (message, timestamp))

    conn.commit()
    conn.close()
    


def on_closing(event=None):
    # when window is closed, send "close" to the server and close the connection
    my_msg.set("close")
    send_message()
    root.destroy()


def run_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  
    server_port = 8000 

    # connect with server
    client_socket.connect((server_ip, server_port))

    # get username from user
    username = input("Enter your username: ")
    client_socket.send(username.encode("utf-8"))


    # GUI window
    global root
    root = tk.Tk()
    root.title("Chat App")

    # frame to hold the messages
    messages_frame = tk.Frame(root)
    scrollbar = tk.Scrollbar(messages_frame)  # navigate through past messages

    # display messages
    global msg_listbox
    msg_listbox = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    msg_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    msg_listbox.pack()
    messages_frame.pack()

   

    # widget to input messages
    global my_msg
    my_msg = tk.StringVar()  
    entry_field = tk.Entry(root, textvariable=my_msg)
    entry_field.bind("<Return>", send_message)
    entry_field.pack()
    entry_field.focus()

    # send button to send messages
    send_button = tk.Button(root, text="Send", command=send_message)
    send_button.pack()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # thread to receive messages from the server
    receive_thread = Thread(target=receive_message)
    receive_thread.start()

    # run GUI
    root.mainloop()


if __name__ == "__main__":
    run_client()
