from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime, date
import warnings

from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from markup_mixin.models import MarkupMixin

class Newsletter(models.Model):
    """
    A newsletter.
    
    Let's add some meat to this things bone's and actually allow it
    to do batch emailing of an uploaded (or typed in) newsletter.
    """
    name = models.CharField(_("name"), max_length=50)
    slug = models.SlugField(_("name slug"))
    org = models.CharField(_("organization"), max_length=100)
    about = models.TextField(_("about"), blank=True, null=True)
    editor = models.ForeignKey(User, related_name="editor")
    default= models.BooleanField(_('Default'), default=False, 
                    help_text='Your sites default newsletter')
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now_add=True, auto_now=True)
    
    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
    
    def __unicode__(self):
        return u'%s' % (self.name)


class Edition(MarkupMixin, TimeStampedModel):
    """
    An edition of a newsletter.

    Editions can be uploaded as media files (pdf, jpg, etc..)

    Along with the upload, the model also contains some optional
    fields that allow a basic summary of, and a photo from the newsletter
    to be presented.

    In the future, a full templating system and text-based newsletters
    would be nice, but complicated.
    """
    title=models.CharField(_('Title'), max_length=100, blank=True, help_text="Leave this blank and we'll set it to the published month and year.")
    newsletter=models.ForeignKey(Newsletter)
    published=models.DateField(_('published'), default=datetime.now())
    preview_image=models.ImageField(_('preview image'), upload_to="newsletter/previews/", blank=True, null=True)
    preview=models.TextField(_('Preview'), blank=True, null=True)
    content=models.TextField(_('Content'), blank=True, null=True, help_text='Add newsletter content here, using markup of your choice')
    rendered_content=models.TextField(_('Rendered content'), blank=True, null=True, editable=False)
    file=models.FileField(_('file'), upload_to="newsletter/newsletters/", blank=True, null=True)

    class Meta:
        verbose_name = 'Edition'
        verbose_name_plural = 'Editions'
        get_latest_by='published'

    class MarkupOptions:
        source_field = 'content'
        rendered_field = 'rendered_content'

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.published.strftime('%B %Y')
        super(Edition, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s - %s' % (self.newsletter.name, self.title)


class SubscriptionBase(models.Model):
    '''
    A newsletter subscription base.

    '''

    subscribed = models.BooleanField(_('subscribed'), default=True)
    email = models.EmailField(_('email'), unique=True)
    created_on = models.DateField(_("created on"), blank=True)
    updated_on = models.DateField(_("updated on"), blank=True)
    
    class Meta:
        abstract = True
    
    @classmethod
    def is_subscribed(cls, email):
        '''
        Concept inspired by Satchmo. Thanks guys!
        
        '''
        try:
            return cls.objects.get(email=email).subscribed
        except cls.DoestNotExist, e:
            return False
         
    
    def __unicode__(self):
        return u'%s' % (self.email)
        
    def save(self, *args, **kwargs):
        self.updated_on = date.today()
        if not self.created_on:
            self.created_on = date.today()
        super(SubscriptionBase,self).save(*args, **kwargs)

class Subscription(SubscriptionBase):
    '''
    Generic subscription
    
    '''
        
    def save(self, *args, **kwargs):
        super(Subscription,self).save()
