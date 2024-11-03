from .views import *
from django.urls import path
from rest_framework import routers
from .views import *
from django.urls import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.SimpleRouter()
router.register(r'employee-creation', Employeecreation, basename='emp-creation')
router.register(r'employee-profile',EmployeeProfile,basename='EmployeeProfile')
router.register(r'employee-custome-add',EmployeeCustomField,basename='EmployeeCustomField')


urlpatterns = [
    path('', include(router.urls)),
    path('employee-login/',view=employeelogin,name='employeelogin'),
    path('employee-password-change/',view=passwordChange,name='passwordChange'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  

]