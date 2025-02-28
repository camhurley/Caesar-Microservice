import zmq


def send_request(socket, message):
    """
    Prepares and sends a request containing a string.
    """

    # Send the message to the server.
    socket.send_string(message)
    print("Request sent.")


def receive_response(socket):
    """
    Receives responses from the microservice. Decodes message as a string
    """

    # Get the data.
    reply = socket.recv()

    # Decode the data into a string
    reply_str = reply.decode('utf-8')

    # Output the string.
    return reply_str


def main():

    # Prompt user for input string
    input_string = input("Type in what you wish to encrypt, then press Enter: ")

    # Setup ZMQ
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:4949")  # Port 4949 again

    # Send the input string
    send_request(socket, input_string)

    # Receive 1st/DUMMY response (necessary for ZMQ)
    receive_response(socket)

    # Prompt for the cipher
    cipher = input("Type in the cipher string, then press Enter: ")

    # Send the cipher key string
    send_request(socket, cipher)

    # Receive the encrypted string
    result = receive_response(socket)

    # Check and print the response.
    if result:
        print("Encrypted message received:", result)
    else:
        print("Error receiving response")

    # ZMQ cleanup
    if socket:
        socket.close()
    if context:
        context.term()

    input("Press Enter to close.")


if __name__ == '__main__':
    main()
