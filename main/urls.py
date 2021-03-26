from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
path('',views.index,name="index"),
path('home/',views.home,name="home"),
path('signup/',views.signup,name="signup"),
path('email_verify/',views.email_verify,name="email_verify"),
path('login/',views.login,name="login"),
path('search/',views.search,name="search"),
path('notifications/',views.notifications,name="notifications"),
path('chat/',views.chat,name="chat"),
path('post_status/',views.post_status,name="post_status"),
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)