from django.shortcuts import redirect


# функция главной страницы:
def redirect_site(request):
    return redirect('persons_list_url', permanent=True)