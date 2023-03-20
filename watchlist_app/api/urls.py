from django.urls import path,include
from watchlist_app.api.views import WatchListAv,WatchDetailAV,Streamplatform,ReviewList,ReviewDetail,ReviewCreate,Watchlist
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('platform',Streamplatform,basename='streamplatform')

urlpatterns = [
    path('list/',WatchListAv.as_view(),name='movie_list'),
    path('<int:pk>',WatchDetailAV.as_view(),name='movie_detail'),
    path('',include(router.urls)),
    path('platform/<int:pk>/review',ReviewList.as_view(),name='review_list'),
    path('platform/review/<int:pk>',ReviewDetail.as_view(),name='review_detail'),
    path('platform/<int:pk>/review-create',ReviewCreate.as_view(),name='review_create'),

    path('watchlist/',Watchlist.as_view(),name='watchlist'),

    # path('review',ReviewList.as_view(),name='review_list'),
    # path('review/<int:pk>',ReviewDetail.as_view(),name='review_detail'),
    ]
