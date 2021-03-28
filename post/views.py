import math
import requests
from accounts import mixins
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http.response import Http404
from django.views.generic import DetailView, FormView, View
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from . import forms, models


def title_crawling(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrom e/73.0.3683.86 Safari/537.36"
    }
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")
    if soup.find("meta", {"property": "og:title"}):
        title = soup.find("meta", {"property": "og:title"}).get("content")
        img = soup.find("meta", {"property": "og:image"}).get("content")
    else:
        title = "제목이 없습니다."
        img = "이미지를 찾을 수 없습니다."
    return title, img


def img_download(url):
    r = requests.get(url)
    file = open("{{post.title}}.jpg", "wb")
    file.write(r.content)
    file.close()


def posts(request):
    post_list = models.Post.objects.all()
    paginator = Paginator(post_list, 12)
    page_number = request.GET.get("page", 1)
    post_list = paginator.get_page(page_number)
    count = 5
    end_page = paginator.count / 5

    if int(page_number) % count == 0:
        start = (int(int(page_number) / count) * count + 1) - count
        end = int(page_number)
    elif page_number == end_page:
        start = (int(int(page_number) / count) * count) + 1
        end = int(end_page)
    else:
        start = int(int(page_number) / count) * count
        end = (math.ceil(int(page_number) / count) * count) - 1

    print(type(start), type(end))
    page_obj = paginator.page_range[start:end]
    return render(
        request, "post/home.html", {"post_list": post_list, "page_obj": page_obj}
    )


def posts_politics(request):
    post_list = models.Post.objects.filter(category__name="정치")
    return render(request, "post/home.html", {"post_list": post_list})


def posts_economy(request):
    post_list = models.Post.objects.filter(category__name="경제")
    return render(request, "post/home.html", {"post_list": post_list})


def posts_it(request):
    post_list = models.Post.objects.filter(category__name="IT")
    return render(request, "post/home.html", {"post_list": post_list})


def posts_company(request):
    post_list = models.Post.objects.filter(category__name="기업")
    return render(request, "post/home.html", {"post_list": post_list})


def posts_science(request):
    post_list = models.Post.objects.filter(category__name="과학")
    return render(request, "post/home.html", {"post_list": post_list})


def posts_society(request):
    post_list = models.Post.objects.filter(category__name="사회/문화")
    return render(request, "post/home.html", {"post_list": post_list})


def posts_bookreview(request):
    post_list = models.Post.objects.filter(category__name="책 리뷰")
    return render(request, "post/home.html", {"post_list": post_list})


class CreatePosts(mixins.LoggedInOnlyView, FormView):

    form_class = forms.CreatePostsForm
    template_name = "post/write.html"

    def form_valid(self, form):
        post = form.save()
        post.user = self.request.user
        url = form.cleaned_data.get("post_url")
        post.title = title_crawling(url)[0]
        post.image = title_crawling(url)[1]
        post.save()
        form.save_m2m()
        messages.success(self.request, "작성 완료!")
        return redirect(reverse("post:detail", kwargs={"pk": post.pk}))


# @login_required
# def post_write(request):
#     if request.method == "POST":
#         form = forms.PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user
#             url = form.cleaned_data.get("post_url")
#             post.title = title_crawling(url)[0]
#             post.save()
#             form.save_m2m()
#             return redirect("post:home")
#     else:
#         form = forms.PostForm()

#     return render(request, "post/post_write.html", {'forms':form})


class PostDetail(DetailView):
    model = models.Post
    template_name = "post/detail.html"
    context_object_name = "forms"


@login_required
def post_edit(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.method == "POST":
        form = forms.PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid:
            post = form.save(commit=False)
            if post.user == request.user:
                url = form.cleaned_data.get("post_url")
                post.title = title_crawling(url)[0]
                post.save()
                form.save_m2m()
                return redirect("post:detail", pk=pk)
            else:
                raise Http404
    else:
        if post.user == request.user:
            form = forms.PostForm(instance=post)
        else:
            raise Http404

    return render(request, "post/edit.html", {"forms": form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if post.user == request.user:
        post.delete()
        return redirect("post:home")
    else:
        Http404


class SearchView(View):
    def get(self, request):
        form = forms.SearchForm(request.GET)
        print(form)
        if form.is_valid():
            search = form.cleaned_data.get("search_content")
            title_post = models.Post.objects.filter(Q (title__icontains=search) | Q (content__icontains=search))
            return render(request, "post/search.html", {"form":form, "post_list":title_post})

        return render(request, "post/search.html", {"form":form})
    

def error(request):
    return render(request, "post/error.html")