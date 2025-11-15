from django.contrib.auth.hashers import check_password, make_password
from django.db import models

# FLAW 3: store passwords in plaintext
#   True  = vulnerable (plaintext, direct compare)
#   False = fixed (hashed passwords)
FLAW_3_PLAINTEXT_PASSWORDS = True


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)  # enough for hashes too
    role = models.CharField(max_length=20, default="user")  # admin / user

    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)

    def set_password(self, raw_password):
        if FLAW_3_PLAINTEXT_PASSWORDS:
            self.password = raw_password
        else:
            self.password = make_password(raw_password)

    def check_password(self, raw_password):
        if FLAW_3_PLAINTEXT_PASSWORDS:
            return self.password == raw_password
        else:
            return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
