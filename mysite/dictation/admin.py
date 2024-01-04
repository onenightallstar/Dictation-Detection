from django.contrib import admin
from .models import dication_task,content

class dication_taskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['task_name']}),
        ('内容', {'fields': ['contents']}),
        ('时间', {'fields': ['task_start_time','task_end_time']}),
    ]
    filter_horizontal = ('contents',)
    list_display = ('task_name','status','task_pub_time','task_start_time','task_end_time','remain_time')
    list_filter = ["task_pub_time","status"]
    search_fields = ["task_name"]
    


admin.site.register(dication_task,dication_taskAdmin)
admin.site.register(content)
# Register your models here.
