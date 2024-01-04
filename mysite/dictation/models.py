from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin


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

class dication_task(models.Model):
    
    task_name = models.CharField('默写任务',max_length=200,default='默写任务')
    # task_pub_time 无需输入 auto_now_add 自动添加
    task_pub_time = models.DateTimeField('任务发布时间',auto_now_add=True)
    contents = models.ManyToManyField(content, verbose_name='古诗词库')
    task_start_time = models.DateTimeField('任务开始时间')
    task_end_time = models.DateTimeField('任务结束时间')
    status = models.CharField('状态',max_length=200,default='未开始')
    class Meta:
        verbose_name = "默写任务"
        verbose_name_plural = "默写任务"
    # Meta类作用：修改模型在admin中的显示方式
    # verbose_name：单数形式显示
    # verbose_name_plural：复数形式显示

    def __str__(self):
        return self.task_name
    
    # @admin.display(
    #     boolean=True,
    #     ordering="task_pub_time",
    #     description="最近发布？",
    # )

    STATUS_CHOICES = [
        ('进行中', '正在进行'),
        ('未开始', '未开始'),
        ('已结束', '已结束'),
    ]
    def save(self, *args, **kwargs):
        now = timezone.now()
        if now > self.task_pub_time and now < self.task_end_time:
            self.status = '进行中'
        elif now < self.task_pub_time:
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




