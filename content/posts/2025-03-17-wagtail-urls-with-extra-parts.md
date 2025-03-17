---
title: "Wagtail Page URLs with extra parts"
date: "2025-03-17 18:58:16"
tags: [Wagtail]
---


Wagtail organises its [pages in a tree](https://docs.wagtail.org/en/stable/reference/pages/theory.html). So the page URLs are based on the given page position and slug. Let's imagine that you run a podcast aggregation site, with podcast pages and podcast episode pages:

```
/
├─ about/
├─ the-podcast/  <-- PodcastPage
│  ├─ hello-world/ <-- PodcastEpisodePage
...
```


The path for the "Hello world" episode is `https://example.com/the-podcast/hello-world`. 

Your page models may look like:

```python
from wagtail.models import Page


class PodcastPage(Page):
    subpage_types = ["PodcastEpisodePage"]


class PodcastEpisodePage(Page):
    parent_page_types = ["PodcastPage"]
```

Now, you are asked to change the URL structure so that the episodes are prefixed with `/editions/`. So `https://example.com/the-podcast/hello-world` would become `https://example.com/the-podcast/editions/hello-world`. In a traditional Wagtail way, you could create a placeholder page model `PodcastEditionsPage` that sits under `PodcastPage` and the episode pages get created under it:

```python
class PodcastPage(Page):
    subpage_types = ["PodcastEditionsPage"]


class PodcastEditionsPage(Page):
    parent_page_types = ["PodcastEditionsPage"]
    subpage_types = ["PodcastEpisodePage"]
    max_count_per_parent = 1


class PodcastEpisodePage(Page):
    parent_page_types = ["PodcastEditionsPage"]
```

For whatever reasons, the site editors do not like this setup (e.g. it is too much work to start a new podcast section). 

To solve this, we can make use of [`RoutablePageMixin`](https://docs.wagtail.org/en/stable/reference/contrib/routablepage.html) which can help with serving content under defined paths. So `https://example.com/the-podcast/editions/` would be a sub-url for the podcast page (`https://example.com/the-podcast/`). But the episode pages would still use the old format. Looking through the Wagtail documentation 
[`Page.get_url_parts()`](https://docs.wagtail.org/en/stable/reference/models.html#wagtail.models.Page.get_url_parts) looks interesting. In short, it is used internally to generate the page URL:

```python
from typing import TYPE_CHECKING, Optional

from wagtail.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, path

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.template.response import TemplateResponse


class PodcastPage(RoutablePageMixin, Page):
    subpage_types = ["PodcastEpisodePage"]

    @path("edition/<str:slug>/")
    def edition(self, request: "HttpRequest", slug: str) -> "TemplateResponse":

        if not (edition := PodcastEpisodePage.objects.live().child_of(self).filter(slug=slug).first()):
            raise Http404

        response: "TemplateResponse" = edition.serve(request)
        return response


class PodcastEpisodePage(Page):
    parent_page_types = ["PodcastPage"]

    def get_url_parts(self, request: Optional["HttpRequest"] = None):
        site_id, root_url, page_path = super().get_url_parts(request=request)

        # inject the "edition" slug before the page slug in the path
        # works in conjunction with PodcastPage.edition()
        split = page_path.strip("/").split("/")
        split.insert(-1, "edition")
        page_path = "/".join(["", *split, ""])

        return (site_id, root_url, page_path)
```

This takes care of the requirement for episode page paths to be prefixed `/editions/` without the intermediate page type.
But the simple path is still available and if we want to prevent that, this can be extended to:


```python
from typing import TYPE_CHECKING, Optional

from django.shortcuts import redirect
from wagtail.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, path

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.template.response import TemplateResponse


class PodcastPage(RoutablePageMixin, Page):
    subpage_types = ["PodcastEpisodePage"]

    @path("edition/<str:slug>/")
    def edition(self, request: "HttpRequest", slug: str) -> "TemplateResponse":

        if not (edition := PodcastEpisodePage.objects.live().child_of(self).filter(slug=slug).first()):
            raise Http404

        response: "TemplateResponse" = edition.serve(request, serve_as_edition=True)
        return response


class PodcastEpisodePage(Page):
    parent_page_types = ["PodcastPage"]

    def get_url_parts(self, request: Optional["HttpRequest"] = None):
        site_id, root_url, page_path = super().get_url_parts(request=request)

        # inject the "edition" slug before the page slug in the path
        # works in conjunction with PodcastPage.edition()
        split = page_path.strip("/").split("/")
        split.insert(-1, "edition")
        page_path = "/".join(["", *split, ""])

        return (site_id, root_url, page_path)

    def serve(self, request: "HttpRequest", *args, **kwargs) -> "HttpResponse":
        if not kwargs.get("serve_as_edition"):
            # if for some reason we're getting the non-editioned path
            # redirect to the path with the /edition/ slug
            page_url = self.get_url(request=request)
            if page_url != request.path:
                return redirect(page_url)


        return super().serve(request, *args, **kwargs)
```

And that should do the trick. 

May your site handle odd path structures!
