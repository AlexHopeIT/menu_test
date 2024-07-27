from django import template
from menu.models import Menu, MenuItem
from django.urls import resolve


register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    menu = Menu.objects.get(name=menu_name)
    current_url = resolve(context['request'].path_info).url_name
    return {'menu': menu,
            'current_url': current_url}


def build_menu_tree(menu_items, current_url):
    tree = []
    for item in menu_items:
        tree_item = {
            'title': item.title,
            'url': item.get_url(),
            'children': build_menu_tree(item.children.all(),
                                        current_url),
            'active': item.get_url() == current_url or any(child['active'] for child in build_menu_tree(item.children.all(), current_url))
        }
        tree.append(tree_item)
    return tree


@register.inclusion_tag('menu/menu_tree.html')
def render_menu_tree(menu_items, current_url):
    return {'menu_items': build_menu_tree(menu_items, current_url)}
