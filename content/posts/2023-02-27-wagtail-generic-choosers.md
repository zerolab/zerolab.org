---
title: "Custom choosers in Wagtail"
date: 2023-02-27T17:32:35Z
tags: ["Wagtail", "tutorial"]
---

Wagtail 4.0 introduced the concept of [generic viewset](https://docs.wagtail.org/en/stable/extending/generic_views.html)
which allows a bundle of views to be defined collectively, and their URLs to be registered in a single operation.

This is most useful for choosers, but is not limited to it. Consider the following use case:


```python
# myapp/models.py

from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page


class Organisation(models.Model):
    name = models.CharField(max_length=255)


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    organisation = models.ForeignKey(
        Organisation, blank=True, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MyPage(Page):
    author = models.ForeignKey(Person, blank=True, null=True, on_delete=models.SET_NULL)

    content_panels = Page.content_panels + [FieldPanel("author")]
```

We have a basic `Person` with the expected first and last name, and a link to an `Organisation`.
The Wagtail interface will use a regular HTML select for the author field on `MyPage`, which may be OK for a few entries, but certainly does not scale.

This is where the generic viewsets come in handy. To create a custom chooser we need to define our viewset:

```python
# myapp/views.py
from wagtail.admin.viewsets.chooser import ChooserViewSet

from .models import Person


class PersonChooserViewSet(ChooserViewSet):
    model = Person
    icon = "user"
    choose_one_text = "Choose a person"
    choose_another_text = "Choose another person"
    edit_item_text = "Edit this person"


person_chooser_viewset = PersonChooserViewSet("person_chooser")
```

This defines a simple chooser which shows a list of people's names. If you want to add a "Create" tab, and thus allow creating `Person` instances
from the chooser, define the `form_fields` attribute.


```python
# myapp/views.py
from wagtail.admin.viewsets.chooser import ChooserViewSet

from .models import Person


class PersonChooserViewSet(ChooserViewSet):
    ...
    form_fields = ["first_name", "last_name"]

...
```

Then you need to register the new viewset:

```python
from wagtail import hooks

from .views import person_chooser_viewset



@hooks.register("register_admin_viewset")
def register_viewset():
    return person_chooser_viewset
```

Et voilà!

But wait, what if you want to display the organisation name in a separate column? The [Viewsets reference page](https://docs.wagtail.org/en/stable/reference/viewsets.html)
has all the information you need.

```python
# myapp/views.py
from wagtail.admin.ui.tables import Column
from wagtail.admin.views.generic.chooser import ChooseView
from wagtail.admin.viewsets.chooser import ChooserViewSet

from .models import Person


class PersonChooseView(ChooseView):
    def get_object_list(self):
        return Person.objects.select_related("organisation").only(
            "first_name", "last_name", "organisation__name"
        )

    @property
    def columns(self):
        return super().columns + [
            Column("organisation", label="Organisation", accessor="organisation"),
        ]


class PersonChooserViewSet(ChooserViewSet):
    model = Person
    icon = "user"
    choose_view_class = PersonChooseView
    choose_one_text = "Choose a person"
    choose_another_text = "Choose another person"
    edit_item_text = "Edit this person"


    person_chooser_viewset = PersonChooserViewSet("person_chooser")
```

Should you need to customise the `Organisation` column, you can define a `Column` class and use that instead.


```python
# myapp/views.py
...
class OrganisationColumn(Column):
    def get_value(self, instance):
        return instance.organisation.name if instance.organisation else "No company"


class ChooseView(ChooseView):
    @property
    def columns(self):
        return super().columns + [
            OrganisationColumn("organisation", label="Organisation"),
        ]

...
```

If you want to enable search in the chooser, then either your model needs to inherit from `wagtail.search.index.Indexed` and have a `search_fields` definition
as per [documentation](https://docs.wagtail.org/en/stable/topics/search/indexing.html#indexing-custom-models) or define a `filter_form_class` attribute.

Your code could looks something like:


```python
# myapp/models.python
...
from wagtail.search import index
...

class Person(index.Indexed, models.Model):
    ...
    search_fields = [
        index.SearchField("first_name", partial_match=True),
        index.SearchField("last_name", partial_match=True),
        index.RelatedFields(
            "organisation",
            [
                index.SearchField("name", partial_match=True),
            ],
        )
    ]


# myapp/views.py
from wagtail.admin.ui.tables import Column
from wagtail.admin.views.generic.chooser import ChooseResultsView, ChooseView, ChosenView
from wagtail.admin.viewsets.chooser import ChooserViewSet

from .models import Person


class PersonChooserMixin:
    # Note: Using a mixin to apply both to the chooser view and the chooser
    # search results view.
    def get_object_list(self):
        # We override this method to fetch the related organisation field
        # to avoid additional queries when evaluating the queryset.
        return Person.objects.select_related("organisation").only(
            "first_name", "last_name", "organisation__name"
        )

    @property
    def columns(self):
    return super().columns + [
        Column("organisation", label="Organisation", accessor="organisation")
    ]


class PersonChooseView(PersonChooserMixin, ChooseView):
    pass


class PersonChooseResultsView(PersonChooserMixin, ChooseResultsView):
    pass


class PersonChosenView(ChosenView):
    # Note: while not stricly necessary, https://github.com/Tijani-Dia/dj-tracker
    # highlights another optimisation.
    def get_object(self, pk):
        return Person.objects.only("first_name", "last_name").get(pk=pk)


class PersonChooserViewSet(ChooserViewSet):
    model = Person
    icon = "user"
    choose_view_class = PersonChooseView
    chosen_view_class = PersonChosenView
    choose_results_view_class = PersonChooseResultsView
    choose_one_text = "Choose a person"
    choose_another_text = "Choose another person"
    edit_item_text = "Edit this person"


person_chooser_viewset = PersonChooserViewSet("person_chooser")
```

Kudos to Tidine Dia for inquiring on how to add new columns in custom choosers, as
well as his great [dj-tracker](https://github.com/Tijani-Dia/dj-tracker) package which
comes in handy to identify query optimisation opportunities.
