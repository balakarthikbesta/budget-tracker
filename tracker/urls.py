from django.urls import path
from .views import budget_view, reset_budget

urlpatterns = [
    path('', budget_view, name='budget'),
    path('reset/', reset_budget, name='reset'),  # Ensure this is defined correctly
]
