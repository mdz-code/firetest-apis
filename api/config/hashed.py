import bcrypt

class Hash:

    def get_hashed_password(self, plain_text_password):
        # Hashear a senha pela primeira vez
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

    def check_password(self, plain_text_password, hashed_password):
        # Checkar se a senha heashead é igual a informada hashed password.
        return bcrypt.checkpw(plain_text_password, hashed_password)