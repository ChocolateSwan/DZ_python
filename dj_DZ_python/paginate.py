from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(objects_list, request, perPage):
    page = request.GET.get('page', 1)

    paginator = Paginator(objects_list, perPage)
    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        objects_page = paginator.page(paginator.num_pages)

    low = objects_page.number - 3
    high = objects_page.number + 3
    if low < 1:
        low = 1
    if high > paginator.num_pages:
        high = paginator.num_pages
    return objects_page, range(low, high + 1)

