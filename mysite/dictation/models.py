from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
from django.contrib.auth.models import Group,User


class content(models.Model):
    content_name = models.CharField('古诗词名称',max_length=200,null=False)
    content_age = models.CharField('古诗词朝代',max_length=200,default='未知')
    content_author = models.CharField('古诗词作者',max_length=200,default='未知')
    content_txt = models.TextField('古诗词内容',max_length=20000,null=False)

    class Meta:
        verbose_name = "古诗词库"
        verbose_name_plural = "古诗词库"

    def __str__(self):
        return self.content_name

def get_default_end_time(days=0, hours=0, minutes=0):
    return timezone.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes)

class dictation_task_teacher(models.Model):
    
    task_name       = models.CharField('默写任务名称',max_length=200,default='默写任务')
    task_pub_time   = models.DateTimeField('任务发布时间',default=get_default_end_time())# task_pub_time 无需输入 auto_now_add 自动添加
    contents        = models.ManyToManyField(content, verbose_name='古诗词库')
    task_start_time = models.DateTimeField('任务开始时间',default=get_default_end_time())
    task_end_time   = models.DateTimeField('任务结束时间',default=get_default_end_time(hours=1))
    status          = models.CharField('状态',max_length=200,default='未开始')
    groups          = models.ManyToManyField(Group,verbose_name='指定班级',blank=True)
    users           = models.ManyToManyField(User,verbose_name='指定学生',blank=True)
    class Meta:
        verbose_name = "默写任务-教师端"
        verbose_name_plural = "默写任务-教师端"
    # Meta类作用：修改模型在admin中的显示方式
    # verbose_name：单数形式显示
    # verbose_name_plural：复数形式显示

    def __str__(self):
        return self.task_name

    STATUS_CHOICES = [
        ('进行中', '正在进行'),
        ('未开始', '未开始'),
        ('已结束', '已结束'),
    ]
    def save(self, *args, **kwargs):
        now = timezone.now()
        if now > self.task_start_time and now < self.task_end_time:
            self.status = '进行中'
        elif now < self.task_start_time:
            self.status = '未开始'
        else:
            self.status = '已结束'
        super().save(*args, **kwargs) #super()调用父类方法 .save()保存

        
        task = dictation_task_student(task_name=self.task_name)
        task.save()
        task.contents.set(self.contents.all())
        # 当ManytoManyField字段时，不可以直接赋值，要用set方法、
            

        # user_queryset1 = self.users.all()
        # user_queryset2 = self.groups.user.all()
        # combined_queryset = user_queryset1 | user_queryset2
        # unique_users = combined_queryset.distinct()

        # for content in self.contents.all():
        #     for user in self.users.all():
        #         print(f'Creating dictation_task_student {content} for user {user}')
        #         dictation_task_student.objects.create(
        #             task_name=self.task_name,
        #             contents=content,
        #             task_start_time=self.task_start_time,
        #             task_end_time=self.task_end_time,
        #             # user=user
        #         )

    def remain_time(self):
        now = timezone.now()
        if self.task_start_time > now:
            return self.task_start_time-now
        elif self.task_end_time > now:
            return self.task_end_time-now
        else:
            return "已结束"
    remain_time.short_description = '剩余时间'

    def get_contents(self):
        #将contents的内容以逗号分隔显示
        return ", ".join([content.content_name for content in self.contents.all()])
    get_contents.short_description = '默写内容'

class dictation_task_student(models.Model):
    task_name       = models.CharField('默写任务名称',max_length=200,default='默写任务')
    contents        = models.ManyToManyField(content, verbose_name='古诗词库')
    task_start_time = models.DateTimeField('任务开始时间',default=get_default_end_time())
    task_end_time   = models.DateTimeField('任务结束时间',default=get_default_end_time(hours=1))
    status          = models.CharField('状态',max_length=200,default='未开始')
    score           = models.IntegerField('得分',default=0)
    # user            = models.ForeignKey(User,verbose_name='学生',on_delete=models.CASCADE)
    class Meta:
        verbose_name = "默写任务-学生端"
        verbose_name_plural = "默写任务-学生端"

    def __str__(self):
        return self.task_name

    STATUS_CHOICES = [
        ('进行中', '正在进行'),
        ('未开始', '未开始'),
        ('已结束', '已结束'),
    ]
    def save(self, *args, **kwargs):
        now = timezone.now()
        if now > self.task_start_time and now < self.task_end_time:
            self.status = '进行中'
        elif now < self.task_start_time:
            self.status = '未开始'
        else:
            self.status = '已结束'
        super().save(*args, **kwargs)

    def remain_time(self):
        now = timezone.now()
        if self.task_start_time > now:
            return self.task_start_time-now
        elif self.task_end_time > now:
            return self.task_end_time-now
        else:
            return "已结束"
    remain_time.short_description = '剩余时间'

