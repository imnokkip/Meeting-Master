import bcrypt

SALT = bcrypt.genSALT()

def generate(name, password):
    combined = f"{name}:{password}"
    token_bytes = bcrypt.hashpw(combined.encode(), salt=SALT)
    return token_bytes.decode('utf-8')

def verify_token(token, name, password):
    combined = f"{name}:{password}"
    if isinstance(token, str):
        token = token.encode('utf-8')
    return bcrypt.checkpw(combined.encode(), token)