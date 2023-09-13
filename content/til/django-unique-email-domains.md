---
title: "Get unique domains for an email field on a model"
date: "2023-05-31 10:53:07.7977 +0100 BST"
tags: [Django]
source:
---

```python
from django.db.models import F, Value
from django.db.models.functions import StrIndex, Substr
from myapp.models import MyModel

MyModel.objects.annotate(
    at_pos=StrIndex('email', Value('@')) + 1, 
    domain=Substr('email', F('at_pos'))
).distinct('domain').values_list('domain', flat=True)
```