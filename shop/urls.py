from django.urls import path

from . import auth_views, views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),
    path("register/", auth_views.register, name="register"),
    path("login/", auth_views.UserLoginView.as_view(), name="login"),
    path("logout/", auth_views.UserLogoutView.as_view(), name="logout"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("cart/update/<int:product_id>/", views.cart_update, name="cart_update"),
    path("cart/clear/", views.cart_clear, name="cart_clear"),
]
