from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from markdown2 import Markdown, markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    """
    Render html page based off of the title url.
    """
    if request.method == "POST":
        query = request.POST.get("q")
        if query in util.list_entries():
            page = util.get_entry(title)
            converter = Markdown()
            html_page = converter.convert(page)

            return HttpResponseRedirect(reverse("page"), {
                "title": query,
                "page": html_page
            })
        else:
            matches = []
            for entry in util.list_entries():
                if query.lower() in entry.lower():
                    matches.append(entry)

            return HttpResponseRedirect(reverse("index"), {
                "entries": matches
            })
    else:
        page = util.get_entry(title)

        if not page:
            return render(request, "encyclopedia/404.html")

        converter = Markdown()
        html_page = converter.convert(page)
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "page": html_page
        })


