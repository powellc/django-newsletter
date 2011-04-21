from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings

from newsletter.models import Edition
from newsletter.views import ExcelView, NewsletterDetailView, DefaultNewsletterView

admin.autodiscover()

urlpatterns = patterns('',

    url (r'^admin/newsletter/subscription/download/csv/$', 
        view=ExcelView.as_view(),
        name='download_csv',
    ),
    
    #url (r'subscribe/$', view=views.subscribe_detail, name='subscribe_detail', ),
    url (r'(?P<slug>[-\w]+)/$', view=NewsletterDetailView.as_view(), name='nw-newsletter-detail', ),
    url (r'^$', view=DefaultNewsletterView.as_view(), name='nw-index', ),
)
