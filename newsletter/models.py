from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User
import warnings
from datetime import datetime


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
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now_add=True, auto_now=True)
    
    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'
    
    def __unicode__(self):
        return u'%s' % (self.name)
    

class Edition(models.Model):
    """
    An edition of a newsletter.
    
    Editions can be uploaded as media files (pdf, jpg, etc..)
    
    Along with the upload, the model also contains some optional
    fields that allow a basic summary of, and a photo from the newsletter
    to be presented.
    
    In the future, a full templating system and text-based newsletters
    would be nice, but complicated.
    """
    edition=models.CharField(_('edition'), max_length=40)
    slug=models.SlugField(_('edition slug'))
    newsletter=models.ForeignKey(Newsletter)
    published=models.DateField(_('published'), default=datetime.now())
    preview=models.TextField(_('preview'), blank=True, null=True)
    preview_image=models.ImageField(_('preview image'), upload_to="newsletter/previews/", blank=True, null=True)
    file=models.FileField(_('file'), upload_to="newsletter/newsletters/", blank=True, null=True)
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now_add=True, auto_now=True)
    
    class Meta:
        verbose_name = 'Edition'
        verbose_name_plural = 'Editions'
        ordering=('-published',)
    
    def __unicode__(self):
        return u'%s - %s' % (self.newsletter.name, self.published)
    

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
        self.updated_on = datetime.date.today()
        if not self.created_on:
            self.created_on = datetime.date.today()
        super(SubscriptionBase,self).save(*args, **kwargs)

class Subscription(SubscriptionBase):
    '''
    Generic subscription
    
    '''
        
    def save(self, *args, **kwargs):
        super(Subscription,self).save()
