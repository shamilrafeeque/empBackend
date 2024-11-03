from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password,name,position,is_staff=False,is_admin=False,is_active=True):
        if not (email and name and position ):
            raise ValueError("email,name and position are mandatory")
        email=self.normalize_email(email)
        user=self.model(email=email,name=name,position=position,is_admin=is_admin,is_active=is_active)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password,name,position):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            name=name,
            position=position,
            is_staff=True
        )
        user.is_active = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser):
    name=models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    position=models.CharField(max_length=255)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff=models.BooleanField(default=False)

    objects=UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'position']

    def has_perm(self,perm,obj=None):
        return self.is_staff

    def has_module_perms(self,add_label):
        return True


    # def __str__(self):
    #     return self.email
    

class CustomeField(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fields=models.JSONField(default=dict,blank=True)