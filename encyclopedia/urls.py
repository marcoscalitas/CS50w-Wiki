from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new_entry, name="new"),
    path("edit/<str:title>", views.edit_entry, name="edit"),
    path("random", views.random_entry, name="random"),
]
