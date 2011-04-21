import logging
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django import http
from django.views.generic.list import BaseListView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from django.conf import settings

from newsletter.models import Subscription, Edition, Newsletter
from newsletter.forms import SubscriptionForm
from newsletter.core import csv

import datetime
import re

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

class ExcelResponseMixin(object):
    def render_to_response(self, context):
        return self.get_csv_response(self.convert_context_to_xls(context))

    def get_csv_response(self, content, **httpresponse_kwargs):
        return http.HttpResponse(content['data'], 
                                 content_type=content['mimetype'],
                                 **httpresponse_kwargs)

    def convert_context_to_xls(self, context):
        return csv.generate_csv(context)

class ExcelView(ExcelResponseMixin, BaseListView):
    model = Subscription

class DefaultNewsletterView(DetailView, FormView):
    template_name = 'newsletter/newsletter_detail.html'
    form_class = SubscriptionForm
    success_url = '/'
    
    def get_object(self):
        return Newsletter.objects.get(default=True)

    def get_context_data(self, **kwargs):
        context = super(DefaultNewsletterView, self).get_context_data(**kwargs)
        context['form'] = SubscriptionForm
        return context

class NewsletterDetailView(DetailView, FormView):
    model = Newsletter
    form_class = SubscriptionForm

    def get_context_data(self):
        context['form'] = SubscriptionForm
        return context

    def post(request, *args, **kwargs):
        if form.is_valid():
            subscribed = form.cleaned_data["subscribed"]
            form.save()
            if subscribed:
                message = getattr(settings,
                    "NEWSLETTER_OPTIN_MESSAGE", "Success! You've been added.")
            else:
                message = getattr(settings,
                     "NEWSLETTER_OPTOUT_MESSAGE", 
                     "You've been removed. Sorry to see ya go.")

            extra = {
                'success': True,
                'message': message,
                'form': form_class(),
            }
            extra.update(extra_context)
            return render_to_response(success_template, extra, 
                 RequestContext(request))
