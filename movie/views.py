import math
from django.core import paginator
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View
from .models import Movie


def main(request):
    total_movie = Movie.objects.all()
    paginator = Paginator(total_movie, 20)
    page_number = request.GET.get("page", 1)
    movie_list = paginator.get_page(page_number)
    view_count = 10
    end_page = math.ceil(paginator.count/20)

    if int(page_number) % view_count == 0:
        start = (int(int(page_number) / view_count) * view_count + 1) - view_count
        end = int(page_number)
    else:
        start = int(int(page_number) / view_count) * view_count
        end = (math.ceil(int(page_number) / view_count) * view_count)

    page_obj = paginator.page_range[start:end]
    return render(
        request, "total_movie.html", {"movie_list": movie_list, "page_obj": page_obj, 
                                    "end_page":end_page}
    )


def search(request):
    search = request.GET.get("search")
    actors = request.GET.get("actors")
    director = request.GET.get("director")
    ganre = request.GET.get("ganre")
    country= request.GET.get("country")
    sort= request.GET.get("sort")
    rating_num= request.GET.get("rating_num")

    form = {
        'search':search,
        'actors':actors,
        'director':director,
        'ganre':ganre,
        'country':country,
        'sort':sort,
        'rating_num':rating_num
    }

    if sort == 'rating':
        movie_list = Movie.objects.filter(Q(title__icontains=search) & Q(actors__icontains=actors) & Q(director__icontains=director) & Q(rating_num__gte=rating_num)
         & Q(etc__icontains=ganre) & Q(etc__icontains=country)).order_by('-rating').exclude(rating__icontains="정보")
    else:
        movie_list = Movie.objects.filter(Q(title__icontains=search) & Q(actors__icontains=actors) & Q(director__icontains=director) & Q(rating_num__gte=rating_num)
        & Q(etc__icontains=ganre) & Q (etc__icontains=country)).order_by('title').exclude(rating__icontains="정보")

    print(rating_num)
    return render(
        request, "total_movie.html", {"movie_list": movie_list, "form":form})