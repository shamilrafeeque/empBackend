from rest_framework import permissions
from rest_framework_simplejwt.tokens import AccessToken
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff  
    
class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff  
    
    

class AuthHandler():
    def get_id(self, request):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split()[1]
            decoded_token = AccessToken(token)
            # Access the user ID from the decoded token payload
            user_id = decoded_token['user_id']
            return user_id
        except:
            return False
    def is_admin(self,request):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split()[1]
            payload = AccessToken(token)
        except:
            return False
        try:
            return payload['is_staff']
        except:
            return False
    
    
Auth=AuthHandler()
    
