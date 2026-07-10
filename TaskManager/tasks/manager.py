# here we have to write the code for the CustomUser model manager, 
# which decides how the record or the data should be stored as we have written our own customized User Model
# with own properties
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, password = None, **extras):

        if not phone_number:
            raise ValueError("phone_number was not given")
        user = self.model(
            phone_number,
            **extras
        )
        user.set_password(password)
        user.save(using = self._db)

        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            extra_fields.setdefault("is_active", True)

            if extra_fields.get("is_staff") is not True:
                raise ValueError("Superuser must have is_staff=True.")

            if extra_fields.get("is_superuser") is not True:
                raise ValueError("Superuser must have is_superuser=True.")

            return self.create_user(
                phone_number=phone_number,
                password=password,
                **extra_fields
            )