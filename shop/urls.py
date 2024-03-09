
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [

    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # path('api/v1/', include("shop.urls")),

    # посмотрим какие django дает инструменты из коробки, для этого
    path('users/', include('new_user.urls')),
    path('api/v1/', include('api.urls'))

]
