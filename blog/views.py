from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins

from blog.models import Post
from blog import models, forms
from itertools import chain

from blog.serializers import PostSerializer


def post_list(request):
    my_posts, other_posts = [], []

    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = "1"

    if request.user.is_authenticated:
        my_posts = models.Post.objects.filter(creator=request.user)
        other_posts = models.Post.objects.exclude(creator=request.user)
    else:
        other_posts = models.Post.objects.all()

    posts = list(chain(my_posts, other_posts))
    paginator = Paginator(posts, 9)

    # page_obj = paginator.get_page(page)

    try:
        page_obj = paginator.page(int(page))
    except ValueError:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request,
                  "home/home.html",
                  {
                      'object_list': page_obj.object_list,
                      'page_obj': page_obj,
                      'paginator': paginator
                   })


def category_posts(request, id):
    my_posts_category = models.Post.objects.filter(category__id=id)
    context = {
        "posts_category": my_posts_category
    }
    return render(request, template_name="blog/post/list_categories.html", context=context)


@login_required
def create_post(request):
    form_instance = forms.PostForm()

    if not request.user.has_perm("blog.add_post"):
        raise PermissionDenied

    if request.method == "POST":
        form_instance = forms.PostForm(data=request.POST, files=request.FILES)

        if form_instance.is_valid():
            form_instance.instance.creator = request.user
            form_instance.save()
            return redirect("blog:post_list")

    return render(request,
                  "blog/post/post_form.html",
                  {
                      "form": form_instance,
                      "page_title": "Create Your Post"
                  })


# @csrf_exempt
# def increment_like_post(request):
#    """
#    Increment number of post's likes
#    """

#    post_id = request.POST.get("post_id", None)

#    if post_id:
#        my_post = models.Post.objects.get(pk=post_id)
#        my_post.like += 1
#        my_post.save()
#        return JsonResponse(
#            {
#                "status": "ok"
#            }
#        )


@require_http_methods(["POST"])
@csrf_exempt
def increment_like_of_posts(request, id):
    """
        Increment number of post's likes
    """

    if request.user.is_authenticated:
        post = get_object_or_404(klass=models.Post, pk=id)

        if post:
            if (not post.like_btn_clicked) and (not post.dislike_btn_clicked):
                post.like += 1
                post.like_btn_clicked = True

            elif (not post.like_btn_clicked) and post.dislike_btn_clicked:
                post.like += 1
                post.dislike -= 1
                post.dislike_btn_clicked = False
                post.like_btn_clicked = True

            elif post.like_btn_clicked:
                post.like -= 1
                post.like_btn_clicked = False

            post.save()
            result = True

            # return redirect("blog:post_list")

            return JsonResponse(
                {
                    "result": result,
                    "number_of_likes": post.like,
                    "number_of_dislikes": post.dislike,
                    "like_btn_clicked": post.like_btn_clicked,
                    "dislike_btn_clicked": post.dislike_btn_clicked,
                }
            )
        else:
            pass
    else:
        result = False
        return JsonResponse(
            {
                "result": result,
            }
        )


@require_POST
@csrf_exempt
def increment_dislike_of_posts(request, id):
    """
        Increment number of post's dislikes
    """

    if request.user.is_authenticated:
        post = get_object_or_404(klass=models.Post, pk=id)

        if post:
            if (not post.dislike_btn_clicked) and (not post.like_btn_clicked):
                post.dislike += 1
                post.dislike_btn_clicked = True

            elif (not post.dislike_btn_clicked) and post.like_btn_clicked:
                post.dislike += 1
                post.like -= 1
                post.like_btn_clicked = False
                post.dislike_btn_clicked = True

            elif post.dislike_btn_clicked and post.dislike > 0:
                post.dislike -= 1
                post.dislike_btn_clicked = False

            post.save()
            result = True

            return JsonResponse(
                {
                    "result": result,
                    "number_of_likes": post.like,
                    "number_of_dislikes": post.dislike,
                    "like_btn_clicked": post.like_btn_clicked,
                    "dislike_btn_clicked": post.dislike_btn_clicked,
                }
            )
        else:
            pass
    else:
        result = False
        return JsonResponse(
            {
                "result": result,
            }
        )


def create_categories(request):
    return render(request, "blog/post/category_form.html")


def edit_post(request, pk):
    post = get_object_or_404(klass=models.Post, pk=pk)

    if not request.user.has_perm("blog.change_post"):
        raise PermissionDenied

    if not post.creator == request.user:
        return HttpResponseForbidden("Access Denied.")

    if request.method == "POST":
        form_instance = forms.PostForm(instance=post, data=request.POST, files=request.FILES)

        if form_instance.is_valid():
            form_instance.save()
            return redirect("blog:post_list")
    else:
        form = forms.PostForm(instance=post)
        return render(request,
                      "blog/post/post_form.html",
                      {
                          "form": form,
                          "page_title": "Edit #( {} )".format(form.instance.title)
                      })


class ViewPost(DetailView):  # model's name_detail
    model = Post
    template_name = "blog/post/post_details.html"


# LoginRequiredMixin
class CreateCategory(PermissionRequiredMixin, CreateView):
    model = models.Category

    fields = (
        'name', 'slug'
    )

    extra_context = {
        'page_title': 'Create a category'
    }

    permission_required = "blog.add_category"

    template_name = "blog/post/category_form.html"
    success_url = reverse_lazy('blog:post_list')


# LoginRequiredMixin
# UpdateView looks for forms
class UpdateCategory(PermissionRequiredMixin, UpdateView):
    model = models.Category
    fields = (
        'name', 'slug'
    )
    success_url = reverse_lazy('blog:post_list')

    template_name = "blog/post/category_form.html"
    permission_required = "blog.change_category"


class FilterPostByCategory(ListView):
    model = models.Post
    template_name = 'blog/post/list_categories.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug', None)
        # Get our object's query sets that we created before OR It determines the list of object's query sets
        qs = super().get_queryset()
        qs = qs.filter(category__slug=category_slug)
        return qs


"""
REST API View
"""


class PostViewSet(APIView):
    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(klass=get_user_model(), pk=pk)
            posts = Post.objects.filter(creator=user)
        else:
            posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


class PostsViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
