import bcrypt

salt = bcrypt.gensalt()

def generate(name, password):
    combined = f"{name}:{password}"
    out = bcrypt.hashpw(combined.encode(), salt=salt)
    return out

def verify_token(token, name, password):
    combined = f"{name}:{password}"
    return bcrypt.checkpw(combined.encode(), token)