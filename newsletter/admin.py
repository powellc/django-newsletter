from django.contrib import admin
from newsletter.models import Subscription, Newsletter, Edition
from newsletter.forms import SubscriptionForm

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('name', 'org', 'editor',)
    search_fields= ('about',)
    prepopulate_fields={"slug":('name')}

admin.site.register(Newsletter, NewsletterAdmin)

class EditionAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'edition', 'published',)
    search_fields=('preview','edition',)
    list_filter=('newsletter',)
    prepopulate_fields={"slug":('edition')}

admin.site.register(Edition, EditionAdmin)

class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ('email', 'subscribed', 'created_on', )
    search_fields = ('email',)
    list_filter = ('subscribed',)

admin.site.register(Subscription, SubscriptionAdmin)

