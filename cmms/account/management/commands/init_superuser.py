from django.core.management.base import BaseCommand
from account.models import User
import random
import string


class Command(BaseCommand):
    help = 'Create a superuser and put (random) password to stdout only when no user exists'

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = "root"
            email = "root@cmms"  # hard-coded now
            password = ''.join(random.SystemRandom().choice(string.digits +
                                                            string.ascii_letters) for _ in range(8))
            print('Creating account for superuser (username is root)')
            admin = User.objects.create_superuser(email=email, gid=username,
                                                  student_id=username, nick_name=username,
                                                  real_name=username, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
            print(f'Password is {password}. Please change your password immediately after login!')
        else:
            print('Superuser accounts can only be initialized if no Accounts exist')
