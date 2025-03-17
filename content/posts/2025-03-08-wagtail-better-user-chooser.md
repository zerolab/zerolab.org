---
title: "Better user choosers in Wagtail"
date: "2025-03-08 18:36:29"
tags: [Wagtail, recipes]
---

The Wagtail core choosers (page, images, documents, snippet and generic choosers) are pretty cool way of selecting a relation via a modal that 
can be searchable and filterable.

However, if you have a `ForeignKey` to model not covered by core, the default "chooser" interface is a select box. And if you 
have thousands of instances, that is not a nice setup to work with. 

This is where [generic choosers](https://docs.wagtail.org/en/stable/extending/generic_views.html#chooserviewset) come in handy as they allow you to customise the modal chooser interface and adapt it to your specific needs. I [wrote about them previously]({{% ref "2023-02-27-wagtail-generic-choosers.md" %}}).

I recently needed to make a nicer `User` model chooser, which had a couple of extra tidbits:

```python
# viewsets.py

from typing import TYPE_CHECKING

from django.contrib.admin.utils import quote
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.functional import cached_property
from wagtail.admin.forms.choosers import BaseFilterForm, SearchFilterMixin
from wagtail.admin.ui.tables import Column, StatusTagColumn
from wagtail.admin.utils import get_user_display_name
from wagtail.admin.views.generic.chooser import ChooseResultsView, ChooseView
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.users.views.users import UserColumn, get_users_filter_query


# if you have a custom user model, you could import it directly from the app that provides it
User = get_user_model()


if TYPE_CHECKING:
    from django.db.models import QuerySet


# note: the filter form is needed to enable the search in the modal.
# The generic chooser make this work automatically if the target model is searchable 
# (that is, it inherits from the search index.Indexed), which the User model isn't.
# While you can technically make it indexable if you use a custom User model, it is probably better not to.
class UserFilterForm(SearchFilterMixin, BaseFilterForm):
    @cached_property
    def model_fields(self) -> set[str]:
        return {field.name for field in User._meta.get_fields()}

    def filter(self, objects: "QuerySet[User]") -> "QuerySet[User]":
        """The User model doesn't have search_fields.

        So we take the same approach as the core UserViewSet when it comes to searching
        """
        if search_query := self.cleaned_data.get("q"):
            conditions = get_users_filter_query(search_query, self.model_fields)
            return objects.filter(conditions)
        return objects


# Note: We use a mixin for both the "choose" view which is what one see when the chooser modal opens
# and the "choose results" view which is used when searching/filtering
class UserChooserMixin:
    filter_form_class = UserFilterForm

    @property
    def columns(self) -> list[Column]:
        return [
            UserColumn(
                "name",
                accessor=lambda u: get_user_display_name(u),
                label="Name",
                get_url=(
                    lambda obj: self.append_preserved_url_parameters(  # type: ignore[attr-defined]
                        reverse(self.chosen_url_name, args=(quote(obj.pk),))  # type: ignore[attr-defined]
                    )
                ),
                # this is part of the glue that makes the chooser understand that a user made a choice
                # when clicking on this column
                link_attrs={"data-chooser-modal-choice": True},
            ),
            Column(
                User.USERNAME_FIELD,
                accessor="get_username",
                label="Username",
                width="20%",
            ),
            StatusTagColumn(
                "is_active",
                accessor=lambda u: "Active" if u.is_active else "Inactive",
                primary=lambda u: u.is_active,
                label="Status",
                width="10%",
            ),
        ]

    def get_object_list(self) -> "QuerySet[User]":
        # UserColumn will try to show the user's avatar, which comes from the related UserProfile model.
        return User.objects.select_related("wagtail_userprofile")


class UserChooseView(UserChooserMixin, ChooseView): ...


class UserChooseResultsView(UserChooserMixin, ChooseResultsView): ...


class UserChooserViewSet(ChooserViewSet):
    model = User
    icon = "user"
    choose_view_class = UserChooseView
    choose_results_view_class = UserChooseResultsView
    choose_one_text = "Choose a user"
    choose_another_text = "Choose another user"
    edit_item_text = "Edit this user"


user_chooser_viewset = UserChooserViewSet("user_chooser")
```

and register the viewset with the `register_admin_viewset` hook:

```python
# wagtail_hooks.py.py

from typing import TYPE_CHECKING

from wagtail import hooks

from .viewsets import user_chooser_viewset

if TYPE_CHECKING:
    from .viewsets import UserChooserViewSet


@hooks.register("register_admin_viewset")
def register_viewset() -> "UserChooserViewSet":
    return user_chooser_viewset
```
