from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
  def create_user(self, email, username, password, role):
    if not email:
      raise ValueError("Users must have an email address")
    email = self.normalize_email(email)
    user = self.model(email=email, username=username, role=role)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_super_user(self, email, password, username):
    user = self.create_user(email, password, username, role='admin')
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user


class User(AbstractUser, PermissionsMixin):
  roles = (
    ('student', 'Student'),
    ('teacher', 'Teacher')
  )
  email = models.EmailField(unique=True)
  username = models.CharField(max_length=150)
  role = models.CharField(max_length=10, choices=roles)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'role']

class Course(models.Model):
  title = models.CharField(max_length=100)
  teacher = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
  student = models.ManyToManyField(User, related_name='courses', limit_choices_to={'role': 'student'})
  
  def __str__(self):
    return self.title
  
class Record(models.Model):
  student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
  course = models.ForeignKey(Course, on_delete=models.CASCADE)

  # Grades
  mid = models.FloatField()
  assessment = models.FloatField()
  final = models.FloatField()
  #others
  attendance = models.IntegerField() 
  remarks = models.TextField(blank=True)
  
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.student.username} -- {self.course.title}"