from django.core.urlresolvers import reverse
from django.db import models
from django.utils.safestring import mark_safe

class Post(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=100, unique=True)
    body = models.TextField(help_text="Leave a blank line to split the summary from the rest")
    posted = models.DateTimeField(db_index=True, verbose_name="Date posted", null=True) # null for drafts

    def clean(self):
        self.body = self.body.replace('\r', '').strip()

    def summary(self):
        return mark_safe(self.body.split("\n\n", 1)[0])

    def get_absolute_url(self):
        if self.posted:
            return reverse('blog_post', kwargs={'year': self.posted.year, 'slug': self.slug})
        return reverse('blog_preview', kwargs={'slug': self.slug})

    class Meta:
        ordering = ("-posted",)

    def __str__(self):
        return self.title if self.title else u"Untitled Entry"
