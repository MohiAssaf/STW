from django.contrib import admin
from ShareTheWorld.MAIN.models import Post, Comment, Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
