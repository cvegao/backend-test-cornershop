from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.staff_home, name="staff_home"),
    path('login/', views.login_method, name="login"),
    path('logout/', views.logout_method, name="logout"),
    path('menus/', views.staff_menus, name="staff_menus"),
    path('menus/edit/<str:pk>/', views.edit_menu, name="edit_menu"),
    path('menus/delete/<str:pk>/', views.delete_menu, name="delete_menu"),
    path('orders/', views.show_orders, name="orders"),
    path('slack/', views.slack_notification, name="slack"),
]
