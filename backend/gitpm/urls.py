from django.urls import path

from . import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', include(router.urls)),
  path('', TemplateView.as_view(template_name='index.html')),
]