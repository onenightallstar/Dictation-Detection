from django.contrib import admin
from .models import dictation_task_teacher,content,dictation_task_student
from django.contrib.auth.models import Group,User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin





class dictation_task_teacherAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,               {'fields': ['task_name']}),
        ('内容', {'fields': ['contents']}),
        ('班级和学生', {'fields': ['groups','users']}),
        ('时间', {'fields': ['task_pub_time','task_start_time','task_end_time']}),
    ]
    filter_horizontal = ('contents','groups','users') 
    list_display = ('task_name','status','task_pub_time','task_start_time','task_end_time','remain_time','get_contents')
    list_filter = ["task_pub_time","status"]
    search_fields = ["task_name"]

class dictation_task_studentAdmin(admin.ModelAdmin):
    list_display = ('task_name','status','task_start_time','task_end_time','remain_time')
    list_filter = ['task_start_time',"status"]
    search_fields = ["task_name"]

class UserAdmin(DefaultUserAdmin):
    list_display = ('username','first_name','get_groups')
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = '班级'
    list_filter = ["groups"]
    search_fields = ["username","first_name"]


admin.site.register(dictation_task_teacher,dictation_task_teacherAdmin)

admin.site.register(dictation_task_student,dictation_task_studentAdmin)

admin.site.register(content)

if admin.site.is_registered(User):
    admin.site.unregister(User)

admin.site.register(User, UserAdmin)


