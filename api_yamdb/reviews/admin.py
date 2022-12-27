from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'pub_date',)
    list_editable = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug', 'pub_date',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'pub_date',)
    list_editable = ('name', 'slug',)
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug', 'pub_date',)
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'genre', 'title', 'pub_date',)
    list_editable = ('genre', 'title',)
    search_fields = ('genre', 'title',)
    list_filter = ('genre', 'title', 'pub_date',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category', 'pub_date',)
    list_editable = ('name', 'year', 'category')
    search_fields = ('name', 'year', 'category', 'genre',)
    list_filter = ('name', 'year', 'category', 'genre', 'pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Review)
