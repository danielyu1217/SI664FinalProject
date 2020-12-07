from django.urls import path, reverse_lazy
from . import views

app_name='restaurants'
urlpatterns = [
    path('', views.ResListView.as_view(), name='all'), # All restaurants as a list view
    path('category/<category>', views.CatListView.as_view(), name="res_category"),
    # CRUD
    path('res/<int:pk>', views.ResDetailView.as_view(), name='res_detail'),
    path('res/create',
        views.ResCreateView.as_view(success_url=reverse_lazy('restaurants:all')), name='res_create'),
    path('res/<int:pk>/update',
        views.ResUpdateView.as_view(success_url=reverse_lazy('restaurants:all')), name='res_update'),
    path('res/<int:pk>/delete',
        views.ResDeleteView.as_view(success_url=reverse_lazy('restaurants:all')), name='res_delete'),
    # comment
    path('res/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='res_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('restaurants:all')), name='res_comment_delete'),
    # favorites
    path('res/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='res_favorite'),
    path('res/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='res_unfavorite'),
    path('myfav', views.FavListView.as_view(), name="my_fav"),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined