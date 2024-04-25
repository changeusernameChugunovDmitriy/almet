from django.urls import path

from .views import home_page, registration_view, login_view, logout_view, shop_view, shop_add_view, add_money

from django.conf.urls.static import static


urlpatterns = [
    path('home', home_page, name='home'),
    path('registration', registration_view, name='register'),
    path('login', login_view, name='login'),
    path('logout', logout_view),
    path('shop', shop_view, name='shop'),
    path('skin/<int:id>', shop_add_view),
    path("money/<int:ball>", add_money)
]
