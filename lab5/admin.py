from django.contrib import admin
from .models import Poll, PollOption, Vote

class PollOptionInline(admin.TabularInline):
    model = PollOption
    extra = 2  # количество пустых вариантов при добавлении нового опроса

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'max_choices')
    inlines = [PollOptionInline]

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'poll')
    list_filter = ('poll',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'option', 'ip_address', 'timestamp')
    list_filter = ('poll', 'timestamp')
    search_fields = ('ip_address',)
