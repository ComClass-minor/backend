import os
import secrets

def generate_secret_key():
    return secrets.token_urlsafe(32)

if not os.path.exists('core/.env'):
    with open('core/.env', 'w') as f:
        f.write(f'SECRET_KEY={str(generate_secret_key())}\n')

