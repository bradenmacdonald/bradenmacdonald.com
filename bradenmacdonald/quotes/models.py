#coding: utf-8
import re
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.safestring import mark_safe

class Author(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(blank=True, max_length=512)
    wikipedia_bio = models.CharField(max_length=128)

    def __unicode__(self):
        return u"{}".format(self.name)

    @property
    def wikipedia_url(self):
        if self.wikipedia_bio:
            return u"http://en.wikipedia.org/wiki/{}".format(self.wikipedia_bio)
        return u""

    class Meta:
        ordering = ("name", )

class Quote(models.Model):
    quote = models.TextField(blank=False)
    original = models.TextField(blank=True, help_text="If the quotation is translated, put the original here.")
    note = models.CharField(max_length=512, blank=True)
    author = models.ForeignKey(Author, null=True, blank=True)
    source = models.CharField(max_length=128, blank=True, help_text="String specifying the work in which the quote was published. Surround text with stars for italics or use HTML.")
    rating = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    added = models.DateField(null=False, blank=False, auto_now_add=True)
    confirmed = models.BooleanField(null=False, default=False, help_text="I personally confirmed the attribution/source.")

    @property
    def short_quote(self):
        short = self.quote
        if len(short) > 80:
            pos = short.rfind(' ', 55, 80)
            short = short[0:pos] + u'…'
        return short

    def source_html(self):
        """ HTML-ify the 'source' field, using Markdown-like stars to indicate italics """
        html = self.source
        html = re.sub(r'(?<!\w)\*(?P<text>.+?)\*(?!\w)', r'<em>\g<text></em>', html)
        return mark_safe(html)

    def __unicode__(self):
        return self.short_quote

    class Meta:
        ordering = ("-added", )