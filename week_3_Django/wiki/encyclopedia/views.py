from django.shortcuts import render
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

    page = util.get_entry(title)

    if not page:
        return render(request, "encyclopedia/404.html")

    converter = Markdown()
    html_page = converter.convert(page)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "page": html_page
    })


