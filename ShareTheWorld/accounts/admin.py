from django.contrib import admin
from ShareTheWorld.accounts.models import STWUser

@admin.register(STWUser)
class STWUserAdmin(admin.ModelAdmin):

    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)

    group.short_description = 'Groups'

    list_display = ('username', 'is_superuser', 'is_staff', 'group')