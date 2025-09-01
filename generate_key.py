import secrets

# Generate a new secret key
new_key = secrets.token_hex(32)
print("Your new SECRET_KEY:")
print(new_key)
print("\nAdd this to your .env file:")
print(f'SECRET_KEY="{new_key}"')
