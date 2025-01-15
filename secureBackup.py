import pyzipper
import os

# Zipping a folder with a password
def zip_folder_with_password(folder_path, zip_file_path, password):
    # Create a password-protected zip file
    with pyzipper.AESZipFile(zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED) as zip_file:
        zip_file.setpassword(password.encode('utf-8'))
        
        # Walk through the folder and add all files to the zip
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

# Example usage
folder_to_zip = 'path/to/your/folder'
zip_output_path = 'path/to/output.zip'
password = 'your-secure-password'

zip_folder_with_password(folder_to_zip, zip_output_path, password)



# Extracting a password-protected zip file
def extract_zip_with_password(zip_file_path, extract_to, password):
    with pyzipper.AESZipFile(zip_file_path, 'r') as zip_file:
        zip_file.setpassword(password.encode('utf-8'))
        zip_file.extractall(extract_to)

# Example usage
zip_file_path = 'path/to/output.zip'
extract_folder = 'path/to/extract/folder'
password = 'your-secure-password'

extract_zip_with_password(zip_file_path, extract_folder, password)