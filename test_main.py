import zmq
import json

def main():
    """
    Test program. Sends string & cipher, gets back encrypted string, over ZMQ
    """

    # Setting up ZMQ
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:4949")  # Matching port to caesar.py. Feel free to change

    input("Press ENTER to send string & cipher.")

    # Create a test message containing the input string and cipher.
    data = {
        'input_string': "Hello, world!",
        'cipher': "abC"
    }

    # Sanity check message. Are we sending what we want to send?
    string_sent = data['input_string']
    cipher_sent = data['cipher']
    print(f"Sent string '{string_sent}' for encryption with cipher '{cipher_sent}'.")

    # Send the JSON message
    socket.send_string(json.dumps(data))

    # Wait for reply from caesar
    reply = socket.recv()
    response = json.loads(reply.decode('utf-8'))

    # Check and print the response. Variable name "result" IS IMPORTANT, make sure
    # you match it in the caesar.py if changed.

    if 'result' in response:
        print("Encrypted message:", response['result'])
    else:
        print("Error:", response.get('error', 'Unknown error'))

    input("Press ENTER to close.")

if __name__ == '__main__':
    main()