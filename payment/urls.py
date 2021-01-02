from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.process_payment, name='process'),
    path('successful/', views.payment_successful, name='successful'),
    path('failed/', views.payment_failed, name='failed')
]
