---
title: "Small Wagtail editor enhancements"
date: "2025-12-11 18:13:00"
tags: ['Wagtail', 'js']
---

## Pinned rich text editor toolbar

Out of the box, the Wagtail rich text editor's toolbar is hidden. Users can pin it, and that choice 
is saved in their browser's local storage. I prefer the pinned toolbar from start. You can achieve that 
with a bit of JavaScript. For example. create `wagtail-editor-customisations.js` in your chosen Wagtail app in a `static/js/` folder


```js
// myapp/static/js/wagtail-editor-customisations.js
function setInitialRichtextToolbarStickyByDefault() {
  if (localStorage.getItem('wagtail:draftail-toolbar') === null) {
    localStorage.setItem('wagtail:draftail-toolbar', 'sticky');
  }
}

setInitialRichtextToolbarStickyByDefault();
```

Then use the [`insert_editor_js`](https://docs.wagtail.org/en/stable/reference/hooks.html#insert-editor-js) hook to add it

```python
# myapp/wagtail_hooks.py
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks


@hooks.register("insert_editor_js")
def editor_js() -> str:
    """Modify the default behavior of the Wagtail admin editor."""
    return format_html('<script src="{}"></script>', static("js/wagtail-editor-customisations.js"))
```


## Expand the minimap

If you or your users prefer to have the minimap open by default, add the following to your `wagtail-editor-customisations.js`

```js
// myapp/static/js/wagtail-editor-customisations.js
function setInitialMinimapExpandedByDefault() {
  if (localStorage.getItem('wagtail:minimap-expanded') === null) {
    localStorage.setItem('wagtail:minimap-expanded', true);
  }
}

setInitialMinimapExpandedByDefault();
```


## Other

If you want to interact with the editor panels, Wagtail 7.1 added [a client-side Panels API](https://docs.wagtail.org/en/stable/extending/client_side_panels.html).


May you tweak the editor experience in ways that bring you joy!
