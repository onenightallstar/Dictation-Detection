from django.contrib import admin
from .models import task_teacher,content,task_student,Class,student


def fenfa(modeladmin, request, queryset):
    for obj in queryset:
        obj.fenfa()

fenfa.short_description = "分发任务"

class task_teacherAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,              {'fields': ['task_name']}),
        ('内容',            {'fields': ['contents']}),
        ('班级和学生',      {'fields': ['classes','students']}),
        ('时间',            {'fields': ['task_pub_time','task_start_time','task_end_time']}),
    ]
    filter_horizontal = ('contents','classes','students') 
    list_display = ('task_name','status','task_pub_time','task_start_time','task_end_time','remain_time','get_contents','get_classes','get_students')
    list_filter = ["task_pub_time","status"]
    search_fields = ["task_name"]

class task_studentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['task_name']}),
        ('内容',            {'fields': ['contents']}),
        ('时间',            {'fields': ['task_start_time','task_end_time']}),
    ]
    filter_horizontal = ('contents',)
    list_display = ('task_name','status','task_start_time','task_end_time','remain_time','student')
    list_filter = ['task_start_time',"status"]
    search_fields = ["task_name"]


admin.site.register(task_teacher,task_teacherAdmin)

admin.site.register(task_student,task_studentAdmin)

admin.site.register(content)

admin.site.register(Class)

admin.site.register(student)



