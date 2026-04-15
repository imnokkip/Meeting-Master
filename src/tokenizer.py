import bcrypt

salt = bcrypt.gensalt()
def generate(name):
   out = bcrypt.hashpw(name.encode(), salt = salt)
   print(out)
   return out

def cooky_token_set(resp, token):
    resp.set_cookie(key = "session", value = token)