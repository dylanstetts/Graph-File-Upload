import msal  # Microsoft Authentication Library for acquiring tokens
import requests  # For making HTTP requests to Microsoft Graph API
import json  # For handling JSON data
import os  # For interacting with the file system

# Configuration variables
CLIENT_ID = "c437c758-941f-4100-996c-b55ab00f03a5"  # Azure AD app client ID
FILE_PATH = "C:\\Users\\dylanstetts\\Downloads\\Scripts\\Python\\uploadSession\\testFileCreation.txt"  # Path to the file to be uploaded
FILE_NAME = os.path.basename(FILE_PATH)  # Extracts the file name from the full path
AUTHORITY = "https://login.microsoftonline.com/common"  # Common authority endpoint for authentication
SCOPES = ["https://graph.microsoft.com/Files.ReadWrite"]  # Permissions required to read/write files in OneDrive

def acquire_token(client_id, authority, scopes):
    """Acquire an access token using MSAL interactive flow."""
    # Create a public client application instance
    app = msal.PublicClientApplication(client_id, authority=authority)
    
    # Prompt user to sign in and acquire token interactively
    result = app.acquire_token_interactive(scopes=scopes)
    
    # Check if token acquisition was successful
    if "access_token" not in result:
        print("Failed to acquire token.")
        print("Error details:", result.get("error_description", result))
        return None
    
    # Return the access token
    return result["access_token"]

def create_upload_session(access_token, file_name):
    """Create an upload session for the specified file name."""
    # Microsoft Graph API endpoint to create an upload session
    endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_name}:/createUploadSession"
    
    # Set request headers including the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Request body specifying conflict behavior and file name
    body = {
        "item": {
            "@microsoft.graph.conflictBehavior": "replace",  # Replace file if it already exists
            "name": file_name
        }
    }
    
    # Make POST request to create the upload session
    response = requests.post(endpoint, headers=headers, data=json.dumps(body))
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to create upload session: {response.status_code} {response.text}")
        return None
    
    # Return the upload URL from the response
    return response.json().get("uploadUrl")

def upload_file(upload_url, file_path):
    """Upload the file to the provided upload URL."""
    try:
        # Open the file in binary read mode
        with open(file_path, "rb") as f:
            file_data = f.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False

    # Set headers for the PUT request including content range and type
    headers = {
        "Content-Range": f"bytes 0-{len(file_data)-1}/{len(file_data)}",  # Specify byte range for upload
        "Content-Length": str(len(file_data)),  # Total size of the file
        "Content-Type": "application/octet-stream"  # Binary file type
    }

    # Make PUT request to upload the file
    response = requests.put(upload_url, headers=headers, data=file_data)
    
    # Check if upload was successful
    if response.status_code in [200, 201]:
        print("Upload successful.")
        return True
    else:
        print(f"Upload failed: {response.status_code} {response.text}")
        return False

def main():
    # Extract file name from path
    file_name = os.path.basename(FILE_PATH)
    
    # Acquire access token
    access_token = acquire_token(CLIENT_ID, AUTHORITY, SCOPES)
    if not access_token:
        return  # Exit if token acquisition failed

    # Create upload session
    upload_url = create_upload_session(access_token, file_name)
    if not upload_url:
        return  # Exit if upload session creation failed

    # Upload the file
    upload_file(upload_url, FILE_PATH)

# Entry point of the script
if __name__ == "__main__":
    main()
