from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):

    # function handling creation of users (normal and superusers)
    def _create_users(
        self,
        user_name,
        password=None,
        **extra_fields
    ):
        if not user_name:
            raise ValueError("username field is required")
        user_name = user_name.lower()

        # create user
        user = self.model(
            user_name=user_name,
            **extra_fields
        )

        # set user password
        user.set_password(password)

        # save
        user.save(using=self._db)
        return user

    """
    create outward facing functions to handle creation of users and superusers
    """

    # function to create normal users
    def create_user(
        self,
        user_name,
        password=None,
        **extra_fields
    ):

        # set superuser privileges to default to false
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_users(
            user_name, password, **extra_fields
        )

    # function to create superusers
    def create_superuser(
        self,
        user_name,
        password=None,
        **extra_fields
    ):

        # set the superuser privileges to true
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # perform validation checks
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_users(
            user_name, password, **extra_fields
        )
