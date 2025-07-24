# OneDrive File Upload via Microsoft Graph API

This Python script demonstrates how to upload a file to OneDrive using the Microsoft Graph API and an interactive authentication flow via MSAL (Microsoft Authentication Library), which is designed to work whether the account is personal or corporate.

## Features

- Interactive login using MSAL
- Upload session creation via Microsoft Graph
- File upload with support for conflict resolution

## Requirements
- Python 3.7+
- `msal`
- `requests`

Install dependencies:

```bash
pip install msal requests
```

## Configuration

Update the following variables in the script:

```python
CLIENT_ID = "YOUR_CLIENT_ID_HERE"
FILE_PATH = "path/to/your/file.txt"
```

- CLIENT_ID: Your Azure App registration's client/app ID
- FILE_PATH: Full local path to the file you want to download

## Usage

Run the script.

You will be prompted to sign in with your Microsoft account. After authentication, the file will be uploaded ot your OneDrive root directory

## Permissions

The only permission leveraged in this application is the delegated permission: 

- Files.ReadWrite

