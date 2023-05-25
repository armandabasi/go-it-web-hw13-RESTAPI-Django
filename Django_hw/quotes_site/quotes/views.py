from random import choices

from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AuthorForm, QuoteForm
from .models import Quote, Author, Tag
from .utils import get_mongodb
from django.core.paginator import Paginator


def home(request):
    return render(request, "quotes/index.html", context={"title": "QuoteHive"})


def find_top_ten():
    tag_counts = Tag.objects.annotate(num_quotes=Count('quote')).order_by("-num_quotes")[:10]
    return tag_counts


def show_quotes(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/quotes.html",
                  context={"title": "QuoteHive", "quotes": quotes_on_page, "top_tags": find_top_ten()})


def show_author(request, aut_id):
    author = Author.objects.get(pk=aut_id)
    return render(request, "quotes/show_author.html", context={"title": "QuoteHive", "author": author})


def all_quotes_one_tag(request, tag_id, page=1):
    tag = Tag.objects.get(pk=tag_id)
    quotes = Quote.objects.filter(tags=tag_id).all()
    per_page = 3
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/all_quotes_one_tag.html",
                  context={"title": "QuoteHive", "quotes": quotes_on_page, "tag": tag, "top_tags": find_top_ten()})


def all_quotes_autor(request, aut_id, page=1):
    author = Author.objects.get(pk=aut_id)
    quotes = Quote.objects.filter(author=aut_id).all()
    per_page = 3
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/all_quotes_autor.html",
                  context={"title": "QuoteHive", "author": author, "quotes": quotes_on_page,
                           "top_tags": find_top_ten()})


def random_quote(request):
    quote = choices(Quote.objects.all())
    return render(request, "quotes/random_quote.html",
                  context={"title": "QuoteHive", "quote": quote[0], "top_tags": find_top_ten()})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:quotes")
        else:
            return render(request, "quotes/add_author.html",
                          context={"form": AuthorForm(), "title": "QuoteHive: new author"})
    return render(request, "quotes/add_author.html", context={"form": AuthorForm(), "title": "QuoteHive: new author"})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to="quotes:quotes")
        else:
            return render(request, "quotes/add_quote.html",
                          context={"form": QuoteForm(), "title": "QuoteHive: new quote"})
    return render(request, "quotes/add_quote.html", context={"form": QuoteForm(), "title": "QuoteHive: new quote"})
