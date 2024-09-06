from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _

import uuid

from xuser.managers import MyUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(
        _("username"),
        max_length=254,
        help_text=_("The prefereed username"),
        unique=True,
        null=False,
        blank=False
    )
    username = None
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("date joined"), auto_now_add=True)


    objects = MyUserManager()

    USERNAME_FIELD = "user_name"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]

    def __unicode__(self):
        return f"{self.user_name}"

    def __str__(self):
        return f"{self.user_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True



class AdminUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(
        _("username"),
        max_length=254,
        help_text=_("The prefereed username"),
        unique=True,
        null=False,
        blank=False
    )
    username = None
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_at = models.DateTimeField(_("date joined"), auto_now_add=True)
    groups = models.ManyToManyField(
        Group,
        related_name="admin_users",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="admin_users",
        blank=True
    )


    objects = MyUserManager()

    USERNAME_FIELD = "user_name"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]

    def __unicode__(self):
        return f"{self.user_name}"

    def __str__(self):
        return f"{self.user_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True
