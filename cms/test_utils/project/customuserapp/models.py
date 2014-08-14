# -*- coding: utf-8 -*-
from django.db import models
try:
    import re
    from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
        UserManager)
    from django.core import validators
    from django.core.mail import send_mail
    from django.utils.http import urlquote
    from django.utils.translation import ugettext_lazy as _

    class User(AbstractBaseUser, PermissionsMixin):
        """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.

        Username, password and email are required. Other fields are optional.
        """
        username = models.CharField(_('username'), max_length=30, unique=True,
            help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                        '@/./+/-/_ characters'),
            validators=[
                validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
            ])
        email = models.EmailField(_('email address'), blank=True)
        is_staff = models.BooleanField(_('staff status'), default=False,
            help_text=_('Designates whether the user can log into this admin '
                        'site.'))
        is_active = models.BooleanField(_('active'), default=True,
            help_text=_('Designates whether this user should be treated as '
                        'active. Unselect this instead of deleting accounts.'))
        my_new_field = models.IntegerField(null=True, blank=True, default=42)

        objects = UserManager()

        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['email']

        class Meta:
            verbose_name = _('user')
            verbose_name_plural = _('users')

        def get_absolute_url(self):
            return "/users/%s/" % urlquote(self.username)

        def get_full_name(self):
            """
            Returns the first_name plus the last_name, with a space in between.
            """
            return "A user called %s" % self.username

        def get_short_name(self):
            "Returns the short name for the user."
            return self.username

        def email_user(self, subject, message, from_email=None):
            """
            Sends an email to this User.
            """
            send_mail(subject, message, from_email, [self.email])
except ImportError:
    from django.contrib.auth.models import User  # nopyflakes
