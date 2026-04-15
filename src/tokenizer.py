import bcrypt

salt = bcrypt.gensalt()


def cooky_token_set(resp, token):
    resp.set_cookie(key = "session", value = token)