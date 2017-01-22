from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .models import BasicPage, ProjectGroup

def page(request, path):
    if path.endswith('/'):
        path = path.rstrip('/')
        return HttpResponseRedirect(u'/' + path)

    try:
        page = BasicPage.objects.get(path=path)
    except BasicPage.DoesNotExist:
        raise Http404

    context = {
        'title': page.title,
        'content': mark_safe(page.content),
    }
    if page.description:
        context['meta_description'] = page.description

    return render(request, page.template, context)

def projects(request):
    if request.path.endswith('/'):
        path = request.path.rstrip('/')
        return HttpResponseRedirect(path)

    return render(request, "projects.html", {
        'title': "Projects",
        'groups': ProjectGroup.objects.all(),
    })
