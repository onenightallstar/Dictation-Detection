from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
from django.contrib.auth.models import Group,User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
class content(models.Model):

    id              = models.AutoField(primary_key=True)
    content_name    = models.CharField('古诗词名称',max_length=200,null=False)
    content_age     = models.CharField('古诗词朝代',max_length=200,default='未知')
    content_author  = models.CharField('古诗词作者',max_length=200,default='未知')
    content_txt     = models.TextField('古诗词内容',max_length=20000,null=False)

    class Meta:
        verbose_name = "古诗词库"
        verbose_name_plural = "古诗词库"

    def __str__(self):
        return self.content_name

def get_default_end_time(days=0, hours=0, minutes=0):
    return timezone.now() + datetime.timedelta(days=days, hours=hours, minutes=minutes)

class task_teacher(models.Model):

    id              = models.AutoField(primary_key=True)
    task_name       = models.CharField('默写任务名称',max_length=200,default='默写任务')
    task_pub_time   = models.DateTimeField('任务发布时间',default=get_default_end_time())# task_pub_time 无需输入 auto_now_add 自动添加
    contents        = models.ManyToManyField(content, verbose_name='古诗词库')
    task_start_time = models.DateTimeField('任务开始时间',default=get_default_end_time())
    task_end_time   = models.DateTimeField('任务结束时间',default=get_default_end_time(hours=1))
    status          = models.CharField('状态',max_length=200,default='未开始')
    classes         = models.ManyToManyField('Class',verbose_name='指定班级',blank=True)
    students        = models.ManyToManyField('student',verbose_name='指定学生',blank=True)
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

    def get_contents(self):
        return ", ".join([content.content_name for content in self.contents.all()])
    get_contents.short_description = '默写内容'

    def get_classes(self):
        return ", ".join([Class.name for Class in self.classes.all()])
    get_classes.short_description = '班级'

    def get_students(self):
        return ", ".join([student.name for student in self.students.all()])
    get_students.short_description = '学生'

class task_student(models.Model):

    id              = models.AutoField(primary_key=True)
    task_teacher    = models.ForeignKey(task_teacher,verbose_name='任务ID',on_delete=models.CASCADE,to_field='id',default=1)
    task_name       = models.CharField('默写任务名称',max_length=200,default='默写任务')
    contents        = models.ManyToManyField(content, verbose_name='古诗词库')
    task_start_time = models.DateTimeField('任务开始时间',default=get_default_end_time())
    task_end_time   = models.DateTimeField('任务结束时间',default=get_default_end_time(hours=1))
    status          = models.CharField('状态',max_length=200,default='未开始')
    score           = models.IntegerField('得分',default=0)
    student         = models.ForeignKey('student',verbose_name='学生ID',on_delete=models.CASCADE,to_field='id',default=1)
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

class Class(models.Model):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField('班级名称',max_length=200,default='未知')
    class Meta:
        verbose_name = "班级"
        verbose_name_plural = "班级"

    def __str__(self):
        return self.name
    
class student(models.Model):
    id              = models.AutoField(primary_key=True)
    name            = models.CharField('学生姓名',max_length=200)
    Class           = models.ForeignKey(Class,verbose_name='班级ID',on_delete=models.CASCADE,to_field='id',default=1)
    class Meta:
        verbose_name = "学生"
        verbose_name_plural = "学生"

    def __str__(self):
        return self.name
    

@receiver(m2m_changed, sender=task_teacher.contents.through)
@receiver(m2m_changed, sender=task_teacher.students.through)
@receiver(m2m_changed, sender=task_teacher.classes.through)
def add_task_student(sender, instance, **kwargs):
    print("正在改变task_student")
    print(instance.task_name)
    print(instance.contents.all())
    print(instance.students.all())
    print(instance.classes.all()) 
    #统计所给班级的所有学生
    students = set()
    if sender == task_teacher.classes.through:
        for Class in instance.classes.all():
            for student in Class.student_set.all():
                students.add(student)
    elif sender == task_teacher.students.through:
        for student in instance.students.all():
            students.add(student)

    for student in students:
        #如果task_teacher已经分发给该学生了，就不再分发
        if task_student.objects.filter(task_teacher=instance,student=student).exists():
            continue
        task = task_student.objects.create(
            task_teacher=instance,
            task_name=instance.task_name,
            task_start_time=instance.task_start_time,
            task_end_time=instance.task_end_time,
            student=student,
        )
        task.save()
        task.contents.set(instance.contents.all())



