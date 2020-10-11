from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.randompage, name="random"),
    path("wiki/search", views.search, name="search"),
    path("wiki/new", views.new, name="new"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry") # must go last

]
