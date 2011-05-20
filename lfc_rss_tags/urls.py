# django imports
from django.conf.urls.defaults import *


urlpatterns = patterns('lfc_rss_tags.templatetags.lfc_rss_tags',
    url(r"^get-entries", "get_rss_entries", name="lfc_rss_get_entries"),
)