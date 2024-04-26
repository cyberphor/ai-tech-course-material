import jwcrypto.jwk as jwk
import json

with open("public_key.pem", "rb") as pemfile:
    public_key = jwk.JWK.from_pem(pemfile.read())
    public_key = public_key.export()
    public_key = json.loads(public_key)
    public_key = {"keys": [public_key]}

print(json.dumps(public_key))
