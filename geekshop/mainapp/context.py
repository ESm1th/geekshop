from django.utils.translation import ugettext_lazy as _

main_menu = [{'get_url': 'mainapp:main', 'title': _('Home')},
             {'get_url': 'mainapp:products', 'title': _('Catalogue')},
             # {'get_url': 'mainapp:contacts', 'title': _('Contacts')},
             {'get_url': 'accounts:registration', 'title': _('Sign up')},
             {'get_url': 'accounts:login', 'title': _('Sign in')},
             {'get_url': 'admin:index', 'title': _('Admin panel')}, ]


def menu(request):
    return {'main_menu': main_menu}


def basket(request):
    basket = None

    if request.user.is_authenticated:
        basket = request.user.get_card

    return {'basket': basket}
