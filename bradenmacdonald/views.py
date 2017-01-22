from django.shortcuts import render

from blog.models import Post

def home(request):
    context = {}

    feed = []

    for post in Post.objects.exclude(posted=None)[:3]:
        feed.append( (post.posted, {
            'type': 'blog',
            'title': post.title,
            'summary': post.summary(),
            'permalink': post.get_absolute_url(),
        }) )

    feed.sort(key=lambda story: story[0], reverse=True)
    context['feed'] = feed

    return render(request, 'index.html', context)
