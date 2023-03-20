from rest_framework.response import Response
#from rest_framework.decorators import api_view
from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.api.serializers import WatchListSerializer,StramPlatformSerializer,ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from watchlist_app.api.permissions import IsAdminOrReadOnly,IsReviewUserReadOnly
from .pagination import WatchListPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import mixins

class ReviewList(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Review.objects.filter(watchlist=self.kwargs['pk'])
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserReadOnly]

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): 
        return Review.objects.all()

    def perform_create(self,serializer):
        pk= self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review = Review.objects.filter(watchlist=movie,review_user=self.request.user)
        if review.exists():
            raise ValidationError("You have already reviewed this movie")
        if movie.avg_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating+serializer.validated_data['rating'])/2

        movie.number_rating = movie.number_rating + 1
        movie.save()
        serializer.save(watchlist=movie,review_user=self.request.user)

    
# class ReviewDetail(mixins.RetrieveModelMixin ,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self,request, *args,**kwargs):
#         return self.retrieve(request, *args, **kwargs)
    

# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class WatchListAv(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#----------------------------------------------------------------
class Watchlist(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']
    pagination_class = WatchListPagination

#----------------------------------------------------------------

class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk) 
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def put(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.Http_400_BAD_REQUEST)

class Streamplatform(viewsets.ViewSet):
    permission_classes = [IsAdminOrReadOnly]
    def list(self,request):
        queryset = StreamPlatform.objects.all()
        serializer = StramPlatformSerializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        platform = get_object_or_404(queryset, pk=pk)
        serializer = StramPlatformSerializer(platform)
        return Response(serializer.data)
    def create(self, request):
        serializer = StramPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# class StreamPlatformAV(APIView):
#     def get(self,request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StramPlatformSerializer(platforms,many=True)
#         return Response(serializer.data)

#     def post(self,request):
#         serializer = StramPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class StreamPlatformDetailAV(APIView):
#     def get(self,request,pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StramPlatformSerializer(platform)
#         return Response(serializer.data)
#     def delete(self,request,pk):
#         platform = StreamPlatform.objects.get(pk=pk) 
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT) 
#     def put(self,request,pk):
#         movie=StreamPlatform.objects.get(pk=pk)
#         serializer = StramPlatformSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.Http_400_BAD_REQUEST)


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies,many=True)
#         return Response(serializer.data) 
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request,pk):
#     if request.method == 'GET':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
