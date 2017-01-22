from collections import OrderedDict
from django.utils.timezone import now as tznow
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .models import Post

def index(request):
    posts = Post.objects.exclude(posted=None).values('title', 'slug', 'posted')

    by_year = OrderedDict()
    for p in posts:
        year = p['posted'].year
        if year not in by_year:
            by_year[year] = []
        p['get_absolute_url'] = reverse('blog_post', kwargs={'year': p['posted'].year, 'slug': p['slug']})
        by_year[year].append(p)

    return render(request, 'blog/index.html', {
        'title': 'Blog archive',
        'posts': posts,
        'posts_by_year': by_year,
    })


def post(request, slug, year=None, allow_unpublished=False):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404
    if year and int(year) != post.posted.year:
        return HttpResponseRedirect(post.get_absolute_url())

    if not post.posted:
        # This post has not yet been published
        if allow_unpublished:
            post.posted = tznow()  # Add a fake date so the template can display something
        else:
            raise Http404

    prev_posts = list(Post.objects.filter(posted__lt=post.posted).order_by("-posted")[:1])
    prev_post = prev_posts[0] if prev_posts else None
    next_posts = list(Post.objects.filter(posted__gt=post.posted).order_by("posted")[:1])
    next_post = next_posts[0] if next_posts else None

    return render(request, 'blog/post.html', {
        'title': post.title,
        'post_date': post.posted,
        'post_body': mark_safe(post.body),
        'prev_post': prev_post,
        'next_post': next_post,
        'post_id': post.id,  # Used by Disqus comments box
        'year': post.posted.year,  # Used by Disqus comments box
        'slug': slug,  # Used by Disqus comments box
    })

