from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home),
    path('about/',views.about),
    path('comingsoon/',views.coming,name="coming"),
    path('allproduct/',views.allproduct),
    path('testing/',views.testing),
    path('store/', views.store, name="store"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("Todays/<int:myid>", views.todayView, name="Todays"),
    path("Bests/<int:myid>", views.bestView, name="Bests"),
    path("covids/<int:myid>", views.covid, name="covids"),
    path('join/',views.join),
    path('upload/',views.upload),
    path('top/',views.top),
    path('specific/',views.specific),
    path('bestselling/',views.bestselling),
    path('account/',views.account),
    path('consult/',views.consult),
    path('tracker/',views.tracker),
    path('ayurvedhic/',views.ayurvedhic),

    path('cart/',views.cart, name='cart'),
    path('update_item/',views.updateItem, name='update_item'),
    path('process_order/',views.processOrder, name='process_order'),
    path('checkout/',views.checkout, name='checkout'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('bot/', views.bot, name='bot'),
    path('get/', views.get_bot_response, name='get'),
    path('customerservice/', views.customerservice, name='customerservice'),
    path('mailing/', views.email, name='email'),
    path('wallet/', views.wallet, name='wallet'),
    path('search/', views.search, name='search'),

]
