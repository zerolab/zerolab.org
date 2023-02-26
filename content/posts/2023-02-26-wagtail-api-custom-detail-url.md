---
title: "Wagtail API - how to customize the detail URL"
date: 2023-02-26T22:48:54Z
tags: ["wagtail", "tutorial"]
---

Note: originally posted on 13 December 2019 at https://wagtail.org/blog/wagtail-api-how-customize-detail-url/

A while ago, a member of the Wagtail community wanted to customize the `PagesAPIEndpoint` to access the specific page detail view via its slug
(`/api/v2/pages/the-page-slug`, rather than id (`/api/v2/pages/123`)

The [Wagtail API](https://docs.wagtail.org/en/latest/advanced_topics/api/v2/configuration.html) builds on the [Django REST Framework](https://www.django-rest-framework.org/) (DRF), so the natural place to check was the DRF docs. The [generic views documentation page](https://www.django-rest-framework.org/api-guide/generic-views/#get_objectself)
points to changing `lookup_field`, however that does not work because `BaseAPIEndpoint.get_object_detail_urlpath` from which `PagesAPIEndpoint`
is derived uses `pk` explicitly. The next logical place was to override the detail_url method for the model serializer (ref: [BaseSerializer](https://github.com/wagtail/wagtail/blob/v4.2/wagtail/api/v2/serializers.py#L285)
and [DetailUrlField](https://github.com/wagtail/wagtail/blob/v4.2/wagtail/api/v2/serializers.py#L31), with no success.

Digging further into the Wagtail API implementation internals reveals that the API router gets the URL information from each endpoint
via `BaseAPIViewSet.get_urlpatterns` which defines them as:


```python
# https://github.com/wagtail/wagtail/blob/v4.2/wagtail/api/v2/views.py#L386-L393

class BaseAPIViewSet(GenericViewSet):
    ...

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path("", cls.as_view({"get": "listing_view"}), name="listing"),
            path("<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]
```


With that in hand, we can then define our own endpoint that can handle both id and slug as parameters for the detail view.

```python
# api.py
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter


class MyPagesAPIViewSet(PagesAPIViewSet):
    """
    Our custom Pages API endpoint that allows finding pages by pk or slug
    """

    def detail_view(self, request, pk=None, slug=None):
        param = pk
        if slug is not None:
            self.lookup_field = "slug"
            param = slug
        return super().detail_view(request, param)

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path("", cls.as_view({"get": "listing_view"}), name="listing"),
            path("<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("<slug:slug>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]

# Create the router. “wagtailapi” is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")

api_router.register_endpoint("pages", MyPagesAPIViewSet)
```

While the above works, slugs are only unique within a parent in Wagtail. It is, therefore, possible to have multiple pages with the same slug,
but in different sections of the site (e.g. `our-team` in `/about/our-team` and `/blog/our-team`). This would lead to a `MultipleObjectsReturned`
exception. To account for that, you need to do some defensive programming:

```python
# api.py
from django.core.exceptions import MultipleObjectsReturned
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter


class MyPagesAPIViewSet(PagesAPIViewSet):
    """
    Our custom Pages API endpoint that allows finding pages by pk or slug
    """

    def detail_view(self, request, pk=None, slug=None):
        param = pk
        if slug is not None:
            self.lookup_field = "slug"
            param = slug

        try:
            return super().detail_view(request, param)
        except MultipleObjectsReturned:
            # Redirect to the listing view, filtered by the relevant slug
            # The router is registered with the `wagtailapi` namespace,
            # `pages` is our endpoint namespace and `listing` is the listing view url name.
            return redirect(
                reverse('wagtailapi:pages:listing') + f"?{self.lookup_field}={param}"
            )

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            path("", cls.as_view({"get": "listing_view"}), name="listing"),
            path("<int:pk>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("<slug:slug>/", cls.as_view({"get": "detail_view"}), name="detail"),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]

# Create the router. “wagtailapi” is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")
api_router.register_endpoint("pages", MyPagesAPIViewSet)
```

Using this technique we can provide additional endpoint URL patterns and make the Wagtail API cater for even more project specific requirements.

Happy coding!