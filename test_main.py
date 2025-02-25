import zmq
import json


def send_request(socket, input_string, cipher):
    """
    Prepares and sends a JSON request containing the input string and cipher.
    """

    # Create a JSON payload with the input string and cipher.
    payload = {
        "input_string": input_string,
        "cipher": cipher
    }

    # Send the JSON-encoded message to the server.
    socket.send_string(json.dumps(payload))
    print("Request sent.")


def receive_response(socket):
    """
    Receives and decodes the JSON response from the microservice.
    """

    # Wait for the reply from the server
    reply = socket.recv()

    # Decode the JSON string
    response = json.loads(reply.decode('utf-8'))
    return response


def main():

    # Prompt user for inputs
    input_string = input("Type in what you wish to encrypt, then press Enter: ")
    cipher = input("Type in the cipher string, then press Enter: ")

    # Setup ZMQ
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:4949")  # Port 4949 again

    # Send the request
    send_request(socket, input_string, cipher)

    # Receive response
    response = receive_response(socket)

    # Check and print the response.
    if 'result' in response:
        print("Encrypted message received:", response['result'])
    else:
        print("Error:", response.get('error', 'Unknown error'))


    # ZMQ cleanup
    socket.close()
    context.term()

    input("Press Enter to close.")

if __name__ == '__main__':
    main()
