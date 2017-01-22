_nav = [
    {'url':'/', 'desc': 'Home'},
    {'url':'/about', 'desc': 'About'},
    {'url':'/blog', 'desc': 'Blog',},
    {'url':'/projects', 'desc': 'Projects'},
]

# Or, from django.core.urlresolvers import reverse_lazy then reverse_lazy('home')

# The following is a template context processor that can be used
# via the TEMPLATE_CONTEXT_PROCESSORS settings to make navigation
# links available to every page template

def get_nav(request):
    # Set the "active" attribute of the entry that is currently active
    best_match = {'url': ''}
    for n in _nav:
        if request.path.startswith(n['url']) and len(n['url']) > len(best_match['url']):
            best_match = n
    if best_match['url'] == '/' and len(request.path) > 1:
        best_match = None
    return {"nav": [(n if n is not best_match else dict(active=True, **n)) for n in _nav]}
