"""
URL configuration for aoiPOS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from aoiPosApp import views as aoiView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', aoiView.login, name="login"),
    path('register/', aoiView.register, name="register"),
    path('pos/', aoiView.pos, name="pos"),
    path('summary/', aoiView.summary, name="summary"),
    path('catalogue/', aoiView.catalogue, name="catalogue"),
    path('catalogue/<int:id>/', aoiView.view, name="product-view"),
    path('catalogue/<int:id>/edit', aoiView.view, name="product-edit"),
    path('catalogue/create/', aoiView.view, name="product-create"),
    path('catalogue/delete/', aoiView.deleteProduct, name='product-delete'),
    path('logout/', aoiView.logout, name="logout"),    

    # api routes
    path('api/get-product-list', aoiView.getProductList),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
