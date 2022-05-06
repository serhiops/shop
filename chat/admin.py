from django.contrib import admin
from .models import Messages, Room

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("id","message","author",)
    list_display_links = ('message',"id")
    search_fields = ('id','message')
    list_filter = ("author",)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id","name",'product')
    list_display_links = ("id","name",)
    search_fields = ("id","name",)
    list_filter = ("name", )
