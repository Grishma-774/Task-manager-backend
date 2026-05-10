from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import AllowAny,IsAuthenticated

from task_manager.serializer import RegisterSerializer,Task_Serializer,Notification_Serializer

from task_manager.models import Task,Notification

from rest_framework import status

from task_manager.pagination import TaskPagination

from django.db.models import Q

from django.contrib.auth.models import User


# Create your views here.

class Register_view(APIView):
    
    permission_classes = [AllowAny]


    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            }, status=201)

        return Response(serializer.errors, status=400)




class Create_view(APIView):

    permission_classes=[IsAuthenticated]

    pagination_class=TaskPagination

    def get(self,request):

        all_tasks= Task.objects.filter(user=request.user)

        search=request.query_params.get("search")
        status=request.query_params.get("status")
        priority=request.query_params.get("priority")

        filtered_task=all_tasks

        if(search):
            filtered_task=filtered_task.filter(Q(description__icontains=search) | Q(title__icontains=search) )

        if(status):
            filtered_task=filtered_task.filter(status__iexact=status)

        if(priority):
            filtered_task=filtered_task.filter(priority__iexact=priority)

        total = all_tasks.count()
        completed = all_tasks.filter(status="completed").count()
        pending = all_tasks.filter(status="pending").count()
        in_progress=all_tasks.filter(status="in_progress").count()

        paginator=self.pagination_class()

        paginated_tasks=paginator.paginate_queryset(filtered_task,request)
        serializer=Task_Serializer(paginated_tasks,many=True)

        response=paginator.get_paginated_response(serializer.data)

        response.data["stats"]= {
            "total": total,
            "completed": completed,
            "pending": pending,
            "in_progress":in_progress
        }

        return response


    def post(self,request):

        serializer = Task_Serializer( data=request.data)

        if(serializer.is_valid()):

            serializer.save(user=request.user)

            return Response(
                {
                    "message": "Task created successfully",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Get_View(APIView):

        permission_classes=[IsAuthenticated]

        def get(self,request,pk):

            try:
                task = Task.objects.get(pk=pk,user=request.user)

                serializer=Task_Serializer(task)

                return Response({
                    "message": "Successfully fetched the task",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            except Task.DoesNotExist:

                return  Response({"error": "Task not found"},status=status.HTTP_404_NOT_FOUND)

        
        def put(self,request,pk):

            try:

                task = Task.objects.get(pk=pk, user=request.user)

            except Task.DoesNotExist:

                return Response({
                    "error": "Task not found"
                    },status=status.HTTP_404_NOT_FOUND
                )

            serializer = Task_Serializer(task, data=request.data)

            if serializer.is_valid():

                serializer.save()

                return Response({
                    "message": "Task updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        def patch(self,request,pk):

            try:

                task = Task.objects.get(pk=pk, user=request.user)

            except Task.DoesNotExist:

                return Response({
                    "error": "Task not found"},status=status.HTTP_404_NOT_FOUND
                )

            serializer = Task_Serializer(task, data=request.data, partial=True)

            if serializer.is_valid():

                serializer.save()

                return Response({
                    "message": "Task updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        def delete(self,request,pk):

            try:
                
                task=Task.objects.get(pk=pk,user=request.user)

            except Task.DoesNotExist:

                return Response(
                    {"error": "Task not found"},
                    status=status.HTTP_404_NOT_FOUND
                 )


            task.delete()

            return Response(
                {"message": "Task deleted successfully"},
                status=status.HTTP_200_OK
            )



class Profile_View(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        user=request.user

        all_tasks= Task.objects.filter(user=request.user)

        recent_tasks = Task.objects.filter(user=request.user).order_by("-updated_at")[:5]

        recent_serializer = Task_Serializer(recent_tasks, many=True)

        total = all_tasks.count()
        completed = all_tasks.filter(status="completed").count()
        pending = all_tasks.filter(status="pending").count()
        in_progress=all_tasks.filter(status="in_progress").count()

        return Response({
            "username":user.username,
            "email":user.email,
            "stats":{
                "total":total,
                "completed":completed,
                "pending":pending,
                "in_progress":in_progress
            },
            "recent_tasks":recent_serializer.data
        })


class Notification_view(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
        unread_count=Notification.objects.filter(user=request.user,is_read=False).count()

        serializer=Notification_Serializer(notifications,many=True)

        return Response({
            "count":unread_count,
            "notifications":serializer.data
        })

class Notification_read(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)

        return Response(
            {
            "message": "Notifications marked as read"
        }
        )






        



    

            