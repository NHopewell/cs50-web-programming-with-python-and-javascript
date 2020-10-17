from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from markdown2 import Markdown, markdown

from . import util

def index(request):
    if request.method == "POST":
        query = request.POST.get("q")
        if query in util.list_entries():

            page = util.get_entry(query)
            converter = Markdown()
            html_page = converter.convert(page)

            return render(request, "encyclopedia/page.html", {
                "title": query,
                "page": html_page
            })
        else:
            matches = []
            for entry in util.list_entries():
                if query.lower() in entry.lower():
                    matches.append(entry)

            return render(request, "encyclopedia/index.html", {
                "entries": matches
            })
    else:

        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def page(request, title):
    """
    Render html page based off of the title url.
    """
    page = util.get_entry(title)

    if not page:
        return render(request, "encyclopedia/404.html")

    converter = Markdown()
    html_page = converter.convert(page)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": html_page
    })

def new(request):
    return render(request, "encyclopedia/new.html")


