from django.conf.urls import url, include
app_name = 'backend'

urlpatterns = [
    url(r'user/', include('backend.libs.user.urls', namespace='user')),
]