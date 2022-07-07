import socket
import threading


#Define HOST IP,PORT and Max allowed clients which can be connected to server
HOST = "127.0.0.1"
PORT = 6969     
MAX_ALLOWED_CONNECTIONS = 3 
ACTIVE_CLIENTS = []

#Listen for other clients messages
def Message_listner(client:object,username:str) -> None: 
    '''This function will listen for incoming messages which other clients will send,This
        function will execute concurrently and will listen for any message, and will decode
        the message and print it to the client.
    '''
    while True:
        message = client.recv(2048).decode("utf-8")
        if message!="":
            final_formatted_message = username + "> " + message
            Broadcast_message(final_formatted_message)
        else:
            print(f"No message was sent by {username}.")

#This function will send message to the client from the server
def Send_message_to_client(client:object,message:str) -> None: 
    '''This function will take client socket and message as an argumrent and will send
        it to the rest of the connected clients.
    '''
    client.sendall(message.encode())

#Function to send new message to all the clients that are currently connected to the server.
def Broadcast_message(message:str) -> None: 
    '''This function will iterate over ACTIVE_CLIENTS list and will send message of all
        the connected users.
    '''
    for user in ACTIVE_CLIENTS:
        Send_message_to_client(user[1],message)


#function to handle client
def Client_handler(client:object) -> None: 
    '''
    This function will handle client and will maintain active client list
    It will concurrently listen for new connection and will gather the active
    client list, and will pass on the client object to another function which will
    handle messages sent from the clients.
    args: client object
    '''
    while True:
        username = client.recv(1024).decode('utf-8')
        if username!='':
            ACTIVE_CLIENTS.append((username,client))
            new_joiner_prompt = "SERVER" + f"{username} joined the chat."
            Broadcast_message(new_joiner_prompt)
            break
        else:
            print("Error no username was provided, Please try again.")
    threading.Thread(target=Message_listner,args=(client,username)).start()

def main() -> None: 
    '''This function will create the server side socket object and will bind it to 
       the HOST IP address and PORT.
    '''
    
    #creating server side socket object, here "AF_INET" represents IPv4 and "SOCK_STREAM" represents TCP protocol
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        #binding the host IP address and PORT
        server.bind((HOST,PORT))
        print(f"Succeeded to bind to host {HOST}, PORT:{PORT}")
    except:
        print(f"Unable to bind to host {HOST}, PORT:{PORT}")

    #listening for incomiing connections, Here 3 specifies Maximun allowed connections.
    server.listen(MAX_ALLOWED_CONNECTIONS)
    print("Listening for the client....")
    while True:
        #accepting the conncection 
        client,address = server.accept()
        print(f">> Successfully connected to {address}")
        threading.Thread(target=Client_handler,args=(client,)).start()


if __name__=='__main__':
    main()