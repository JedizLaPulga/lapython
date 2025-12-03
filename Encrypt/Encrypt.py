import os
from cryptography.fernet import Fernet

def encrypt_specific_file(filename):
    """
    Checks if a file exists and is a .txt file, encrypts it, 
    and saves it with a custom extension.
    
    Args:
        filename (str): The name of the file to encrypt.
        
    Returns:
        bytes: The encryption key if successful.
        str: Error message if unsuccessful.
    """
    
    # 1. Restrict to .txt files
    if not filename.endswith('.txt'):
        return "Error: This program only accepts .txt files."

    # 2. Check if file exists in the current directory
    if not os.path.exists(filename):
        return f"Error: The file '{filename}' was not found in the current directory."

    try:
        # 3. Generate a key
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # 4. Read the original file content
        with open(filename, 'rb') as file:
            original_data = file.read()

        # 5. Encrypt the data
        encrypted_data = fernet.encrypt(original_data)

        # 6. Determine output filename
        # Removes .txt and adds .jedizlapulga
        # e.g., 'me.txt' becomes 'me.jedizlapulga'
        output_filename = filename.replace('.txt', '.jedizlapulga')

        # 7. Write the encrypted file
        with open(output_filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_data)

        print(f"Success! '{filename}' has been encrypted to '{output_filename}'.")
        
        # Return the key so the user can decrypt it later
        return key

    except Exception as e:
        return f"An error occurred during encryption: {str(e)}"
    
def decrypt_specific_file(filename, key):
    """
    Checks if a file exists and is a .jedizlapulga file, decrypts it,
    and restores it to a .txt file using the provided key.
    """
    # 1. Restrict to .jedizlapulga files
    if not filename.endswith('.jedizlapulga'):
        return "Error: Input file must end with .jedizlapulga"

    # 2. Check if file exists
    if not os.path.exists(filename):
        return f"Error: The file '{filename}' was not found."

    try:
        # 3. Initialize Fernet with the provided key
        fernet = Fernet(key.encode() if isinstance(key, str) else key)

        # 4. Read the encrypted data
        with open(filename, 'rb') as file:
            encrypted_data = file.read()

        # 5. Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)

        # 6. Restore original filename (.jedizlapulga -> .txt)
        output_filename = filename.replace('.jedizlapulga', '.txt')

        # 7. Write the decrypted file
        with open(output_filename, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        return f"Success! File decrypted and saved as '{output_filename}'."
    except Exception as e:
        return f"An error occurred during decryption: {str(e)}"