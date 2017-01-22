from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from .models import Author, Quote

def index(request):

    # Preserve old pre-Django URLs used by the PHP version of the quotes collection:
    if 'by' in request.GET:
        author_id = int(request.GET['by'])
        return HttpResponseRedirect(reverse('quotes_author', kwargs={'author_id': author_id}))


    quotes = Quote.objects.select_related().all().order_by("-rating", "-added")

    return render(request, 'quotes/quotes_list.html', {
        'title': 'Quotations Collection | Curated by Braden MacDonald ',
        'header': 'Quotations Collection',
        'meta_desc': 'A collection of quotations, curated by Braden MacDonald.',
        'quotes': quotes,
    })

def author(request, author_id):
    try:
        author = Author.objects.get(pk=int(author_id))
    except Author.DoesNotExist:
        raise Http404
    quotes = Quote.objects.select_related().filter(author=author).order_by("-rating", "-added")

    title = u'Quotations by {}'.format(author.name)
    return render(request, 'quotes/quotes_list.html', {
        'title': title,
        'header': title,
        'meta_desc': 'A collection of quotations, curated by Braden MacDonald.',
        'quotes': quotes,
        'show_back_link': True,
    })
