from django.contrib import admin
from .models import Author, Quote

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'quotes_count', 'wiki_link')

    def quotes_count(self, inst):
        return inst.quote_set.count()

    def wiki_link(self, inst):
        if inst.wikipedia_bio:
            return u"<a href=\"{}\">Wiki</a>".format(inst.wikipedia_url)
        return ""
    wiki_link.allow_tags = True

admin.site.register(Author, AuthorAdmin)

class QuoteAdmin(admin.ModelAdmin):
    list_display = ('short_quote', 'author', 'added', 'rating', 'source', 'confirmed')

admin.site.register(Quote, QuoteAdmin)
