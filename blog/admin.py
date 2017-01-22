from datetime import datetime
from django.conf.urls import url
from django.contrib import admin
from django.http import Http404, HttpResponseRedirect
from .models import Post

class PostAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'posted', 'body')
    list_display = ('title', 'posted', 'status', 'slug')
    readonly_fields = ('posted',)
    change_form_template = 'blog/post_change_form.jhtml'
    
    # Publish/Unpublish links:
    def get_urls(self):
        return [
            url(r'^(?P<post_id>\d+)/publish/$', self.admin_site.admin_view(self.publish_view)),
            url(r'^(?P<post_id>\d+)/unpublish/$', self.admin_site.admin_view(self.unpublish_view)),
        ] + super(PostAdmin, self).get_urls()
    def publish_view(self, request, post_id):
        return self.publish_or_unpublish_view(post_id, True)
    def unpublish_view(self, request, post_id):
        return self.publish_or_unpublish_view(post_id, False)
    def publish_or_unpublish_view(self, post_id, publish):
        try:
            post = Post.objects.get(pk=int(post_id))
        except Post.DoesNotExist:
            raise Http404
        if publish and not post.posted:
            post.posted = datetime.now()
        elif not publish:
            post.posted = None
        post.save()
        return HttpResponseRedirect("../")
    def status(self, obj):
        return "Published" if obj.posted else '<span style="font-weight: bold; color: red; background-color: yellow; padding: 3px; border-radius: 3px;">Draft</span>'
    status.allow_tags = True

admin.site.register(Post, PostAdmin)
