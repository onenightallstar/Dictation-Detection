from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create random users'

    def handle(self, *args, **kwargs):
        usernames = []
        for i in range(10000001,10000010):
            usernames.append(str(i))

        for username in usernames:
            # 检查用户名是否已经存在
            if User.objects.filter(username=username).exists():
                print(f'Username {username} already exists.')
                continue

            # 生成一个随机密码
            group_name = '3班'   
            group, created = Group.objects.get_or_create(name=group_name)

            password = User.objects.make_random_password()

            # 创建用户
            user = User.objects.create_user(username=username, password=password)

            #指定组
            user.groups.add(group)

            # 打印用户名和密码
            print(f'Created user {username} with password {password}')