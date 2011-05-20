# python imports
import datetime
import re
import uuid

# django import
from django import template
from django.shortcuts import render_to_response
from django.template import RequestContext

# feedparser imports
import feedparser

register = template.Library()


@register.inclusion_tag('lfc_rss_tags/rss.html', takes_context=True)
def rss(context, url, limit=5):
    """An inclusion tag which displays an rss feed.
    """
    feed = feedparser.parse(url)

    try:
        name = feed["feed"]["link"].split("/")[-1]
    except (KeyError, IndexError, AttributeError):
        return {
            "entries": [],
            "link": "",
            "LANGUAGE_CODE": "",
        }

    entries = []
    for entry in feed.entries[0:limit]:
        summary = entry.summary.replace("%s: " % name, "")

        entries.append({
            "title": entry.title,
            "summary": summary,
            "date": datetime.datetime(*entry["updated_parsed"][0:6])
        })

    return {
        "entries": entries,
        "LANGUAGE_CODE": context.get("LANGUAGE_CODE"),
        "link": feed["feed"]["link"],
    }


@register.inclusion_tag('lfc_rss_tags/rss_ajax.html', takes_context=True)
def rss_ajax(context, url, limit=5):
    """An inclusion tag which displays an rss feed.
    """
    return {
        "url": url,
        "limit": limit,
        "id": uuid.uuid1(),
    }


def get_rss_entries(request, limit=5, template_name="lfc_rss_tags/rss_ajax_entries.html"):
    """Loads the entries for rss_ajax tag.
    """
    url = request.GET.get("url")
    feed = feedparser.parse(url)
    try:
        name = feed["feed"]["link"].split("/")[-1]
    except (KeyError, IndexError, AttributeError):
        return {
            "entries": [],
            "link": "",
            "LANGUAGE_CODE": "",
        }

    entries = []
    for entry in feed.entries[0:limit]:
        summary = entry.summary.replace("%s: " % name, "")
        summary = re.subn("#\S+", "", summary)[0]
        summary = re.subn("(http://\S+)", "<a href='\g<1>'>\g<1></a>", summary)[0]

        entries.append({
            "summary": summary,
            "date": datetime.datetime(*entry["updated_parsed"][0:6])
        })

    return render_to_response(template_name, RequestContext(request, {
        "entries": entries,
        "link": feed["feed"]["link"],
    }))