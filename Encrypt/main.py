import Encrypt

if __name__ == "__main__":
    test_file = "me.txt"
    with open(test_file, "w") as f:
        f.write("This is a secret message inside the text file.")
    
    print(f"Created dummy file: {test_file}")
    
    # Run the encryption function
    target_file = input("Enter the filename to encrypt (e.g., me.txt): ")
    
    result_key = Encrypt.encrypt_specific_file(target_file)
    
    if isinstance(result_key, bytes):
        print(f"\nEncryption Key (Keep this safe!): {result_key.decode()}")
    else:
        print(f"\n{result_key}")