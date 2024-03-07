import os
import hashlib
from Crypto.Cipher import AES
from Crypto import Random

class FileEncryptorDecryptor:
    def __init__(self, key):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt_file(self, input_file, output_file):
        chunk_size = 64 * 1024
        init_vector = Random.new().read(AES.block_size)
        encryptor = AES.new(self.key, AES.MODE_CBC, init_vector)
        
        with open(input_file, 'rb') as infile:
            with open(output_file, 'wb') as outfile:
                outfile.write(init_vector)
                while True:
                    chunk = infile.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)
                    outfile.write(encryptor.encrypt(chunk))

    def decrypt_file(self, input_file, output_file):
        chunk_size = 64 * 1024
        with open(input_file, 'rb') as infile:
            init_vector = infile.read(AES.block_size)
            decryptor = AES.new(self.key, AES.MODE_CBC, init_vector)
            with open(output_file, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                    
    def encrypt_directory(self, directory, output_directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_directory, file + '.encrypted')
                self.encrypt_file(input_file, output_file)

    def decrypt_directory(self, directory, output_directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.encrypted'):
                    input_file = os.path.join(root, file)
                    output_file = os.path.join(output_directory, file[:-10])  # Remove the '.encrypted' extension
                    self.decrypt_file(input_file, output_file)

# Example usage:
if __name__ == "__main__":
    encryptor_decryptor = FileEncryptorDecryptor("Hasini@project")

    # Encrypt a single file
    encryptor_decryptor.encrypt_file("plaintext.txt", "encrypted_file.enc")

    # Decrypt a single file
    encryptor_decryptor.decrypt_file("encrypted_file.enc", "decrypted_file.txt")

    # Encrypt all files in a directory
    encryptor_decryptor.encrypt_directory("directory_to_encrypt", "output_directory_encrypted")

    # Decrypt all files in a directory
    encryptor_decryptor.decrypt_directory("directory_to_decrypt", "output_directory_decrypted")
