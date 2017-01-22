import datetime
from django.db import models
from django.utils.text import slugify

class BasicPage(models.Model):
    path = models.CharField(max_length=128, db_index=True, unique=True)
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    extra_js = models.TextField(blank=True)
    extra_css = models.TextField(blank=True)
    template = models.CharField(blank=False, default="layout.html", max_length=128)

    class Meta:
        ordering = ('path', )
        verbose_name = "Basic Page"
        verbose_name_plural = "Basic Pages"

    def clean(self):
        self.path = self.path.strip('/').replace('//', '')
        for f in ('title', 'description', 'content', 'extra_js', 'extra_css',):
            self.__dict__[f] = getattr(self, f).strip()

    def __unicode__(self):
        return u'/{} : {}'.format(self.path, self.title)

    def get_absolute_url(self):
        return u'/{}'.format(self.path)

# For the Projects page:

class ProjectGroup(models.Model):
    name = models.CharField(max_length=128)
    order = models.IntegerField(null=False, default=5)
    def __unicode__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=128)
    group = models.ForeignKey(ProjectGroup, related_name="projects")
    image = models.ImageField(blank=True, upload_to="proj-thumbs")
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    source_url = models.URLField(blank=True)
    source_desc = models.CharField(blank=True, max_length=128)
    role = models.CharField(blank=True, max_length=128)
    sortdate = models.DateField(blank=False)
    year = models.IntegerField(null=True, blank=True, help_text="Year, or '9999' for ongoing")
    year_began = models.IntegerField(null=True, blank=True)
    tags_str = models.CharField(blank=True, verbose_name="Tags", help_text="Tags, comma-separated", max_length=512)

    class Meta:
        ordering = ('group__order', '-sortdate', )

    def clean(self):
        self.tags_str = ','.join([s.strip() for s in self.tags_str.split(',')])

    def tags(self):
        if not self.tags_str:
            return []
        return [
            {"tag": t, "tag_slug": slugify(t.replace('+', 'p').replace('#', 's'))}  # The replace is for 'C++' -> 'cpp' and C# -> 'cs'
            for t in self.tags_str.split(',')
        ]

    def year_range_str(self):
        if not self.year:
            return None
        current_year = datetime.date.today().year
        year = self.year
        if year > current_year:
            year = current_year
        if self.year_began and self.year_began != year:
            return "{}-{}".format(self.year_began, year)
        return str(year)

    def source_url_is_github(self):
        return 'github.com' in self.source_url

    def __unicode__(self):
        return self.name
