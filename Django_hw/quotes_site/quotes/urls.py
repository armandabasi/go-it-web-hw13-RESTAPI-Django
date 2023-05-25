from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.home, name="home"),
    path("quotes/", views.show_quotes, name="quotes"),
    path('quotes/<int:page>', views.show_quotes, name="quotes_paginate"),
    path("quotes/add_author/", views.add_author, name="add_author"),
    path("quotes/add_quote/", views.add_quote, name="add_quote"),
    path("quotes/show_author/<int:aut_id>/", views.show_author, name="show_author"),
    path("quotes/show_author/all_quotes_autor/<int:aut_id><int:page>", views.all_quotes_autor, name="all_quotes_autor"),
    path("quotes/all_quotes_one_tag/<int:tag_id><int:page>", views.all_quotes_one_tag, name="all_quotes_one_tag"),
    path("quotes/random_quote/", views.random_quote, name="random_quote"),
]
