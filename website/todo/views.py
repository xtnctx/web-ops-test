from django.shortcuts import render
from rest_framework.views import View, APIView
from .models import ToDoModel
from rest_framework.response import Response
from .serializers import ToDoSerializer
from rest_framework import status
from rest_framework import generics
from .serializers import (UserSerializer,
    RegisterSerializer, LoginSerializer)
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken


class ToDoListView(generics.ListAPIView):
    queryset = ToDoModel.objects.all()
    serializer_class = ToDoSerializer

    def get(self, request):
        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        data = {
            "user": request.user.id,
            'todo': request.data.get('todo')
        }
        serializer = ToDoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReadView(APIView):

    def get(self, request, pk):
        todo = ToDoModel.objects.filter(pk=pk)
        serializer = ToDoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UpdateView(APIView):
     def put(self, request):
        todo_id = request.data.get('todo_id')
        todo = request.data.get('todo')

        ToDoModel.objects.filter(id=todo_id).update(todo=todo)
        return Response({"success": True}, status=status.HTTP_201_CREATED)


class DeleteView(View):
    def post(self, request):
        ...


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })



class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token
        })


class UserAPI(generics.RetrieveAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = UserSerializer

  def get_object(self):
    return self.request.user