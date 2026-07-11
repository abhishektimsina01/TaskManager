# here we have to write the code for the CustomUser model manager, 
# which decides how the record or the data should be stored as we have written our own customized User Model
# with own properties
from django.contrib.auth.models import BaseUserManager, UserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, password, **extras):

        # we have to ensure that the field that is compulsary and unique, given to us
        if not phone_number or not password:
            raise ValueError("full credentials was not given")
        
        # create user with the data we have like, phone_number and all the extra fields
        user = self.model(
            phone_number = phone_number,
            **extras
        )
        # at the end we need to hash the passwrod as string or raw password is dangerous for storing 
        user.set_password(password)
        # we then save it in the _db
        user.save(using = self._db)
        print(user)
        return user
    
    # this method is used to make the super user in our application and 
    # it uses the create_user as well we just have to set up some properties and check 
    # so that we can make sure that the user is a super user
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