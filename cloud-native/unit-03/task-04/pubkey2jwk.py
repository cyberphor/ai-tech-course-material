from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from jwcrypto import jwk
from os import getenv

def pem_to_jwk(pem_key):
    # Load the public key from PEM format
    public_key = serialization.load_pem_public_key(
        pem_key.encode('utf-8'),
        backend=default_backend()
    )

    # Convert to JWK format
    jwk_key = jwk.JWK.from_pem(pem_key.encode('utf-8'))

    # Need to add alg to JWK otherwise KrakenD fails
    jwk_key["alg"] = "RS256"
    jwk_key["kid"] = "yourcoolkid"
    
    # Return the JWK as a JSON string
    return jwk_key.export()

# Example usage
pem_public_key = getenv("PUBLIC_KEY")

jwk_public_key = pem_to_jwk(pem_public_key)
print(jwk_public_key)