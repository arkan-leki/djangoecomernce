from django_components import Component, register

@register("collection_card")
class Card(Component):
    # Templates inside `[your apps]/components` dir and `[project root]/components` dir
    # will be automatically found.
    #
    # `template_name` can be relative to dir where `calendar.py` is, or relative to STATICFILES_DIRS
    template_name = "template.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, title, items, image):
        return {
            "title": title,
            "items": items,
            "image": image,
            # ...
        }

    # Both `css` and `js` can be relative to dir where `calendar.py` is, or relative to STATICFILES_DIRS
    # class Media:
    #     css = "style.css"
    #     js = "script.js"
