import zmq  # ZeroMQ for cross-file comms
import json  # JSON will handle the two inputs we need



def caesar(input_string, cipher):
    """
    Applies a caesar cipher, modified to use a cipher string (ex. the cipher is
    'abc' so the first letter shifts by 1 for a, 2nd letter by 2 for b...)
    :param input_string: Unencrypted string.
    :param cipher: Cipher string.
    :return: Encrypted string.
    """

    # Initialize the output string, get the cipher string length, and initialize the
    # cipher index to 0.
    output = ""
    cipher_length = len(cipher)
    cipher_index = 0

    # Iterate over the unencrypted string. Thank god for the ord() function
    for char in input_string:

        # Accounting for spaces, punctuation, etc which will NOT change
        if char.isalpha():
            current_shift_char = cipher[cipher_index % cipher_length]
            shift = ord(current_shift_char.lower()) - ord('a') + 1

            # Going to have to account for upper/lowercase as they have different
            # ASCII values.
            if char.isupper():
                case = ord('A')  # ASCII val = 65
            else:
                case = ord('a')  # ASCII val = 97

            # Apply the shift to the input string. Thanks to wikipedia.org/wiki/Caesar_cipher
            # The mod operator in shifted handles wraparound (like Z shifting "right" back to A...)
            shifted = (ord(char) - case + shift) % 26 + case
            output += chr(shifted) # Put in the output array
            cipher_index += 1  # Move to the next cipher character for the next letter

        # Character is NOT a letter so it should go back in as it is.
        else:
            # Non-letters added back in as they are.
            output += char

    return output

def main():
    """
    ZeroMQ handler function. Waits for input string to encrypt and the cipher
    and then sends back the encrypted string.
    """

    # Setup ZeroMQ
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:4949")  # Binds to port 4949 by default. Feel free to change.

    # Verification of functionality message...
    print("Caesar cipher server is waiting for requests...")

    while True:

        # Wait for the next request from the client.
        message = socket.recv()
        print("Message received")  # DEBUG

        try:
            # Expecting a JSON message with 'input_string' and 'cipher'.
            # If the JSON message vars are different be sure to update them here.
            data = json.loads(message.decode('utf-8'))
            input_string = data['input_string']
            cipher_str = data['cipher']

            # Encrypt the message using the caesar cipher.
            print("Running encryption...")  # DEBUG
            encrypted_string = caesar(input_string, cipher_str)
            print(f"Encryption complete. Sending {encrypted_string}")
            output = {"result": encrypted_string}

        # Error in pulling in data
        except Exception as e:
            output = {"error": str(e)}

        # Send the encrypted string back to the client.
        socket.send_string(json.dumps(output))

if __name__ == '__main__':
    main()