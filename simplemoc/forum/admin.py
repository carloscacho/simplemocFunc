from django.contrib import admin

from .models import Thread, Replay

class ThreadAdmin(admin.ModelAdmin):
    list_display=['title', 'author', 'created', 'modified']
    search_fields=['title', 'author__email', 'body']
    prepopulated_fields = {'slug': ('title',)}

class ReplayAdmin(admin.ModelAdmin):
    list_display=['thread', 'author', 'created','correct', 'replay_up', 'modified']
    search_fields=['thread__title', 'author__email', 'replay']    

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Replay, ReplayAdmin)