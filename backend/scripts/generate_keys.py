import os
import secrets
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def generate():
    KEYS_DIR = os.getenv("KEYS_DIR", "/app/keys")
    PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "private_key.pem")
    PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "public_key.pem")
    INTERNAL_TOKEN_PATH = os.path.join(KEYS_DIR, "internal_token.txt")

    os.makedirs(KEYS_DIR, exist_ok=True)

    if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
        print("Generating new RSA keys...")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
            
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        print("RSA keys generated.")
    else:
        print("RSA keys already exist.")

    if not os.path.exists(INTERNAL_TOKEN_PATH):
        env_token = os.getenv("INTERNAL_API_TOKEN")
        if not env_token:
            print("Generating new internal API token...")
            token = secrets.token_urlsafe(32)
            with open(INTERNAL_TOKEN_PATH, "w") as f:
                f.write(token)
            print("Internal API token generated.")
        else:
            print("Using INTERNAL_API_TOKEN from environment.")
    else:
        print("Internal API token already exists.")

    SESSION_SECRET_PATH = os.path.join(KEYS_DIR, "session_secret.txt")
    if not os.path.exists(SESSION_SECRET_PATH):
        env_secret = os.getenv("SECRET_KEY")
        if not env_secret:
            print("Generating new session secret key...")
            secret = secrets.token_urlsafe(64)
            with open(SESSION_SECRET_PATH, "w") as f:
                f.write(secret)
            print("Session secret key generated.")
        else:
            print("Using SECRET_KEY from environment.")
    else:
        print("Session secret key already exists.")

if __name__ == "__main__":
    generate()
