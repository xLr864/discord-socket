import socket,sys
import threading


HOST = "127.0.0.1"
PORT = 6969     

#Listen for other clients messages
def Listen_for_messages(client:object) -> None:
    '''This function will listen for incoming messages which other clients will send,This
        function will execute concurrently and will listen for any message, and will decode
        the message and print it to the client.
    '''
    while True:
        try:
            message = client.recv(2048).decode("utf-8")
            if message!="":
                username = message.split(">")[0]
                content = message.split(">")[1]
                print(f"[{username}]:-  {content}")
            else:
                print("Message recieved from the client is empty.")
        except:
            print("Server unavailable/offline.")
            sys.exit(0)

#This function will send the message from client to the server 
def send_message(client:object) -> None:
    '''This function will take message as input and it will encode and broadcast the
        message to all other clients or the users.
    '''
    error = 0
    while True:
        try:
            message = input(">")
            if message!="":
                client.sendall(message.encode())
            else:
                print("No message was written")
                error = 1
                break
        except:
            error = 1
            print("Connection was closed, Try again later.")
            break

    if(error):
        sys.exit(0)

#This function will communicate to the server and pass a username to it
def communicate_to_server(client:object) -> None:
    '''This function will take a username and send it to the server and it will run
       concurrent thread which will listen for message from other users
    '''
    username = input("Enter username:- ")
    if username!="":
        client.sendall(username.encode())
    else:
        print("Username can not be empty")
        sys.exit(0)

    threading.Thread(target=Listen_for_messages,args=(client,)).start()
    send_message(client)

def main():
    '''This function will create the client side socket object and will bind it to 
       the HOST IP address and PORT.
    '''
    # root.mainloop()
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client.connect((HOST,PORT))
        print("Successfully connected to the server")
    except:
        print(f"Unable to connect to the server {HOST} PORT:{PORT}")
        exit(0)

    communicate_to_server(client)

if __name__=="__main__":
    main()