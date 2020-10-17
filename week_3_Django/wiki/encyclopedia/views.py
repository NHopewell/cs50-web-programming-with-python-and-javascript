from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from markdown2 import Markdown, markdown
from random import choice

from . import util

def index(request):
    if request.method == "POST":
        query = request.POST.get("q")
        if query in util.list_entries():
            return redirect(page, title=query)
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
    if request.method == 'POST':
        entry_title = request.POST.get("entry_title")
        entry_content = request.POST.get("entry_content")

        for entry in util.list_entries():
            if entry_title.lower() == entry.lower():
                messages.error(request, 'Entry already exists. Try again.')
                return redirect('new')

        util.save_entry(entry_title, entry_content)
        
        return redirect(page, title=entry_title)
    else:
        return render(request, "encyclopedia/new.html")

    
def edit(request, title):
    if request.method == 'POST':

        entry_content = request.POST.get("entry_content")
        util.save_entry(title, entry_content)
        
        return redirect("page", title=title)
    else:
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "page": page
        })


def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return redirect("page", title=title)


