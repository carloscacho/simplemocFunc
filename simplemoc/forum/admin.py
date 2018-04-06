from django.contrib import admin

from .models import Thread, Replay


class ReplayAdmin(admin.ModelAdmin):
    list_display=['thread', 'author', 'created','correct','replay_up',  'replay_down', 'modified']
    fields=['thread', 'author','replay', 'correct',('replay_up',  'replay_down')]
    search_fields=['thread__title', 'author__email', 'replay']
    list_filter = ['thread__title', 'author__email', 'created', 'modified' ]  

class ReplayInline(admin.TabularInline):
    model = Replay

class ThreadAdmin(admin.ModelAdmin):
    list_display=['title', 'author', 'created', 'modified']
    search_fields=['title', 'author__email', 'body']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ReplayInline]

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Replay, ReplayAdmin)