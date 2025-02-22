from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    # path('cars/add/', views.add_car, name='add_car'),
    # path('cars/<int:car_id>/edit/', views.edit_car, name='edit_car'),
    path('cars/', views.car_list, name='car_list'),
    path('cart/', views.cart, name='cart_list'),
    path('add-to-cart/<int:car_id>/',views.add_to_cart,name='add'),


    
    path('login/',views.LoginView,name='login'),
    path('register/',views.register_view,name='register'),

    path('logout/',views.logout_view,name='logout'),
    path('update-cart-item/<int:cart_item_id>/', views.update_cart_item, name='update_cart_item'),  # New URL for updating
    path('update_days/', views.update_days, name='update_days'),  # Add this line
    path('remove/<int:cart_item_id>/',views.remove_from_cart,name='remove'),
    path('feedremove/<int:feedback_id>/',views.remove_from_feedback,name='delete_feedback'),
    path('cancel/<int:order_item_id>/',views.cancel,name='cancelled'),
    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_view, name='profile'),

    path('address/', views.address,name="address"),
    path('start_order/', views.start_order,name='start_order'),
    path('checkout', views.checkout,name='checkout'),
    path('wishlist/', views.wishlist,name='wishlist'),
    path('view_order', views.vieworder,name="view_order"),
    # path('feedback/', views.feedback_view, name='feedback'),

    path('admin-consumer', views.adminconsumer,name='admin_consumer'),
    path('admin-order', views.adminorder,name='admin_order'),
    path('admin-product', views.adminproduct,name='admin_product'),
    path('admin-feedback', views.deletefeedback,name='admin_feedback'),
    path('about', views.about,name='about'),
    path('contact-us', views.contacts,name='contact'),
    path('products/', views.product, name='product'),
]
