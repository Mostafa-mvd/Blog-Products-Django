from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'blog'  # this our namespace

# Routing
router = DefaultRouter()
router.register(r"posts", views.PostsViewSet, basename="posts")

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.ViewPost.as_view(), name="post_detail"),
    path("created/", views.create_post, name="created_form"),
    path("like/<int:id>/", views.increment_like_of_posts, name="like_of_post"),
    path("dislike/<int:id>/", views.increment_dislike_of_posts, name="dislike_of_post"),
    path("edit/<int:pk>/", views.edit_post, name="edit_post"),
    path("create_category/", views.CreateCategory.as_view(), name="create_category"),
    path("update_category/<int:pk>/", views.UpdateCategory.as_view(), name='update-category'),
    path("category/<slug:category_slug>/", views.FilterPostByCategory.as_view(), name='post_by_category'),
    path("api/post/<int:pk>/", views.PostViewSet.as_view(), name="user_posts"),
    path("api/all_post/", views.PostViewSet.as_view(), name="posts"),
    path("api/posts/", include(router.urls)),
    # path("<int:id>/", views.category_posts, name="category"),
    # path("like/", views.increment_like_post, name="like_post"),
    # path("create_category/", views.create_categories, name="create_category"),
]
