from django.shortcuts import render
from django.views.generic import ListView

from main_page.models import MainPageModel


class Home(ListView):
    model = MainPageModel
    template_name = 'main_page/main_page_temp.html'
    context_object_name = 'main_page_json'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        def date_for_main_page(json_obj):
            context_date = {}
            little_context_dict = {}
            for i in json_obj:
                context_date[i.title] = []
            for i in json_obj:
                for key, val in i.json_field.items():
                    little_context_dict.update({key: val})
                context_date[i.title].append(little_context_dict)
                little_context_dict = {}
            return context_date

        def show_home_page_post(json_obj):
            try:
                main_post = json_obj['block_for_main_post'][-1:][0]

                content = main_post['content']
                content = content.split('</p>', maxsplit=1)
                content.insert(1, f'</p><div class="img-cont"><img src="{main_post["image"]}"'
                                  f'style="width: 100%;" alt="{main_post["text"]}"></div>')
                content = "".join(content)
                main_post['content'] = content
                block_for_main_post = list()
                block_for_main_post.append(main_post)
                return {'block_for_main_post': block_for_main_post}
            except KeyError:
                return {'block_for_main_post': 'block_for_main_post'}

        context = date_for_main_page(context['object_list'].order_by('pk'))
        context.update(show_home_page_post(context))
        # print(context)
        return context
