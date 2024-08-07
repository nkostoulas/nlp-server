import argparse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

def parse_args():
    parser = argparse.ArgumentParser(description="NLP server app")
    parser.add_argument("--token-file-path", type=str, default="secrets/token", help="Path to file containing the auth token")
    return parser.parse_args()

# Set up command-line argument parsing
args = parse_args()

# Define Bearer authentication
security = HTTPBearer()

# Load the valid token from a file
def load_valid_token():
    try:
        with open(args.token_file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        raise RuntimeError("Token file not found")

# Get the valid token
valid_token = load_valid_token()

def get_auth_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
