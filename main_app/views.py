from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, TokenPairSerializer, CourseSerializer, RecordSerializer
from .models import Course, Record, User

class RegisterView(APIView):
  authentication_classes = []
  permission_classes = [AllowAny]
  def post(self, request):
    serializer = UserSerializer(data = request.data)
    if(serializer.is_valid()): 
      user = serializer.save()
      return Response({'Message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
  serializer_class = TokenPairSerializer

class LogoutView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"})
    except Exception:
        return Response({"error": "Invalid refresh token"}, status=400)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  @action(detail=False, methods=['get'])
  def students(self, request):
    students = self.get_queryset().filter(role ='student')
    serializer = self.get_serializer(students, many=True)
    return Response(serializer.data)
  
  @action(detail=False, methods=['get'])
  def teachers(self, request):
    teachers = self.get_queryset().filter(role ='teacher')
    serializer = self.get_serializer(teachers, many=True)
    return Response(serializer.data)
  

class CourseViewSet(viewsets.ModelViewSet):
  queryset = Course.objects.all()
  serializer_class = CourseSerializer
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    user = self.request.user
    if user.role != 'teacher':
      raise PermissionDenied("Only teachers can create courses.")
    serializer.save(teacher=user)

  @action(detail = True, methods=['post'])
  def enroll_student(self, request, pk=None):
    course = self.get_object()
    student_id = request.data.get('student_id')
    try:
      student = User.objects.get(id=student_id, role='student')
      course.students.add(student)
      return Response({'message': 'enrolled student successfully'}, status=status.HTTP_200_OK)
    except User.DoesntExist:
      return Response({'error': 'Invalid student ID'}, status=status.HTTP_400_BAD_REQUEST)
    
  @action(detail = True, methods=['post'])
  def enroll_students(self, request):
    course = self.get_object()
    for student in request.data.students:
      print(student.id)


class RecordViewSet(viewsets.ModelViewSet):
  queryset = Record.objects.all()
  serializer_class = RecordSerializer
  permission_classes = [IsAuthenticated]


  @action(detail=False, methods=['POST'])
  def add_record(self, request):
    user = self.request.user
    if user.role != 'teacher':
      raise PermissionDenied("Only teachers can add records.")
    
    student_name = request.data.get('student')
    course_name = request.data.get('course')
    print("-------------")
    print(request.data)
    print("-------------")
    student = User.objects.get(username=student_name)
    course = Course.objects.get(title=course_name)
    record = Record.objects.create(
    student=student,
    course=course,
    mid=request.data['mid'], 
    assessment=request.data['assessment'], 
    final=request.data['final'], 
    attendance=request.data['attendance'], 
    remarks=request.data['remarks'])
    return Response({'message': 'added record successfully'}, status=status.HTTP_200_OK)
  
  @action(detail=False, methods=['get'])
  def student_record(self, request):
    student = User.objects.get(username=request.data.get('student_name'))
    student_records = self.get_queryset().filter(student=student.id)
    serializer = self.get_serializer(student_records, many=True)
    return Response(serializer.data)