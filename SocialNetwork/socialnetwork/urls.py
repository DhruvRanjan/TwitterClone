from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from socialnetwork import views as social_net_views
from django.conf import settings
from django.conf.urls.static import static

"""urlpatterns = [
    url(r'^$', auth_views.login, {'template_name': 'login.html'},name='Login'),
    url(r'^register-user$', social_net_views.register_user, name='Register'),
    url(r'^login$', auth_views.login, {'template_name': 'login.html'},name='Login'),
    url(r'^global-stream$', social_net_views.global_stream, name='GlobalStream'),
    url(r'^profile$', social_net_views.profile, name='Profile'),
]
"""
urlpatterns = [
    url(r'^$', auth_views.login,{'template_name': 'login.html'},name='login'),
    url(r'^register-user$', social_net_views.register_user, name='register'),
    url(r'^login$', auth_views.login,{'template_name': 'login.html'},name='login'),
    url(r'^global-stream$', social_net_views.global_stream, name='globalStream'),
    #url(r'^profile/(?P<username>[-\w.]+)/$', social_net_views.profile, name='profile'),
    url(r'^profile$', social_net_views.profile, name='profile'),
    url(r'^profileview/(?P<username>[-\w.]+)/$', social_net_views.profile_view, name='profileView'),
    url(r'^edit-profile$', social_net_views.edit_profile, name='editProfile'),
    url(r'^follower-stream$', social_net_views.follower_stream, name='followerStream'),
    url(r'^logout$', auth_views.logout,{'next_page': 'login'},name='logout'),
    #url(r'^pictures/(?P<username>[-\w.]+)$', social_net_views.get_profile_picture, name='profile_picture'),
    #url(r'^pictures/' + settings.MEDIA_URL, social_net_views.get_profile_picture, name='profile_picture'),
    #url(r'^pictures/' + settings.MEDIA_URL, social_net_views.get_profile_picture, name='profile_picture'),
    url(r'^get-posts-json$', social_net_views.get_posts_json),
    url(r'^get-posts-xml$', social_net_views.get_posts_xml),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
