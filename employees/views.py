from rest_framework.response import Response
from .models import CustomeField, User
from .serializers import CustomTokenObtainPairSerializer, EmployeeCreationSerializer, EmployeeCustomSerializer
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from .Authhandle import IsAdminUser, IsEmployee,Auth
from rest_framework_simplejwt.views import TokenObtainPairView



# Create your views here.


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class Employeecreation(viewsets.ModelViewSet):
    serializer_class = EmployeeCreationSerializer
    queryset=User.objects.all().order_by('-created_at')
    # pagination_class =SinglePagination
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        user = User.objects.create_user(
            name=validated_data.get('name'),
            email=validated_data.get('email'),
            position=validated_data.get('position'),
            password=validated_data.get('password'),  
        )
        
        response_data = self.get_serializer(user).data
        return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def employeelogin(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:  
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response({'error': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)  

    token = CustomTokenObtainPairSerializer.get_token(user)

    access_token = str(token.access_token)
    refresh_token = str(token)

    response_data = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def passwordChange(request):
    try:
        old = request.data['old password']
        new = request.data['new password']
    except KeyError:
        return Response({'error': 'old and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user=User.objects.get(id=Auth.get_id(request=request))
    if not old or not new:
        return Response({'error': 'Old and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not user.check_password(old):
        return Response({'error': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new)
    user.save()
    return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
    
    





class EmployeeProfile(viewsets.ReadOnlyModelViewSet):
    serializer_class = EmployeeCreationSerializer
    queryset=User.objects.all().order_by('-created_at')
    permission_classes = [IsEmployee]



    def get_queryset(self):
        queryset=super().get_queryset()
        id=Auth.get_id(request=self.request)
        queryset=queryset.filter(id=id)
        return queryset
        


class EmployeeCustomField(viewsets.ModelViewSet):
    serializer_class=EmployeeCustomSerializer
    queryset=CustomeField.objects.all()
    permission_classes = [IsAdminUser]

    
