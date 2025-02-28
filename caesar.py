import zmq  # ZeroMQ for cross-file comms


def caesar(input_string, cipher):
    """
    Applies a caesar cipher, modified to use a cipher string (ex. the cipher is
    'abc' so the first letter shifts by 1 for 'a', 2nd letter by 2 for b...)
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

        # Accounting for spaces, punctuation, etc. which will NOT change
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
            output += chr(shifted)  # Put in the output array
            cipher_index += 1  # Move to the next cipher character for the next letter

        # Character is NOT a letter, so it should go back in as it is.
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

        # Wait for the input string from the client.
        input_string = socket.recv().decode('utf-8')
        print(f"Input string received: {input_string}")  # DEBUG

        # Send null string for ZMQ req/rep
        socket.send_string("DUMMY")
        print("Waiting for cipher...")

        # Wait for the cipher key from the client
        cipher_str = socket.recv().decode('utf-8')
        print(f"Cipher string received: {cipher_str}")  # DEBUG

        try:
            # Encrypt the message using the caesar cipher.
            print("Running encryption...")  # DEBUG
            encrypted_string = caesar(input_string, cipher_str)
            output = encrypted_string
            print(f"Encryption complete. Sending {encrypted_string}")

        # Error in pulling in data
        except Exception as e:
            output = f"Error: {e}"

        # Send the encrypted string back to the client.
        socket.send_string(output)

        # Sent success message, prompt to close
        input("Encrypted message sent. Press Enter to close.")
        raise SystemExit


if __name__ == '__main__':
    main()
