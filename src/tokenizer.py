import bcrypt

salt = bcrypt.gensalt()

def generate(name, password):
    """Генерирует токен в виде строки"""
    combined = f"{name}:{password}"
    token_bytes = bcrypt.hashpw(combined.encode(), salt=salt)
    return token_bytes.decode('utf-8')  # Возвращаем строку

def verify_token(token, name, password):
    """Проверяет токен"""
    combined = f"{name}:{password}"
    # Если токен пришел как строка, преобразуем в bytes для проверки
    if isinstance(token, str):
        token = token.encode('utf-8')
    return bcrypt.checkpw(combined.encode(), token)