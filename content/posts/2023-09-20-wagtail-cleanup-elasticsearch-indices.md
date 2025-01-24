---
title: "Wagtail and Elasticsearch: Clean up unused indexes"
date: 2023-09-20 20:15:36
tags: [Wagtail, search, Elasticsearch]
---

Wagtail deletes the search index and rebuilds it from scratch by default when using the Elasticsearch backend. <sup>[1]</sup>

This means users won't get any results until the re-index is finished. To prevent that one can set `ATOMIC_REBUILD` to `True` in the 
search backends configuration. This allows Wagtail to create new indices, index your content, alias them to the canonical indices and remove the old ones.

However, should the indexing process result in any error, you end up with stray indices. This could spell trouble if you're on limited 
hosting plans such as [Bonsai on Heroku](https://elements.heroku.com/addons/bonsai).

If you have access to the Elasticsearch console you could run the following checks:

`GET /_cat/indices` <sup>[2]</sup> - returns all indices, their status, number of primaries/replicas, documents in them and size

```
health status index                                     uuid     pri rep docs.count docs.deleted store.size pri.store.size
green  open   wagtail__wagtailimages_image_lcgak2e      <UUID>   1   1            0            0       416b           208b
green  open   wagtail__images_customimage_eatxk42       <UUID>   1   1          452            4    416.1kb        209.3kb
green  open   wagtail__wagtaildocs_document_ajkn4li     <UUID>   1   1            0            0       416b           208b
green  open   wagtail__documents_customdocument_xtwnqfk <UUID>   1   1           90            0     99.6kb         49.8kb
green  open   wagtail__wagtailcore_page_zqkorrt         <UUID>   1   1         3251            0      6.8mb          3.4mb
green  open   wagtail__wagtailcore_page_bqsaiep         <UUID>   1   1         3238            0      6.9mb          3.4mb
green  open   wagtail__wagtailcore_page_nm7irjb         <UUID>   1   1         6792           95     23.7mb         11.7mb
```

You can further tweak this by running `GET /_cat/indices?h=creation.date.string,index` which will return the indices by creation date (h/t Alex Morega)


`GET /_cat/aliases` <sup>[3]</sup> - gives you the list of aliases

```
alias                             index
wagtail__documents_customdocument wagtail__documents_customdocument_xtwnqfk - - - -
wagtail__images_customimage       wagtail__images_customimage_eatxk42       - - - -
wagtail__wagtaildocs_document     wagtail__wagtaildocs_document_ajkn4li     - - - -
wagtail__wagtailimages_image      wagtail__wagtailimages_image_lcgak2e      - - - -

wagtail__wagtailcore_page         wagtail__wagtailcore_page_nm7irjb         - - - -
```

Elasticsearch breaks an index into shards in order to distribute them and scale. 
It is recommended to run a cluster of notes so that you have primary and secondary nodes (replicas) for 
reliability. On services such as Bonsai, each node counts towards your total index limit.

`GET /_cat/shards` <sup>[4]</sup> - list all shards

```
index                                   shard  prirep    state    docs   store  ip   node
wagtail__images_customimage_eatxk42         0     p      STARTED   452 209.3kb  <ip> <node>
wagtail__images_customimage_eatxk42         0     r      STARTED   452 206.8kb  <ip> <node>
wagtail__documents_customdocument_xtwnqfk   0     r      STARTED    90  49.8kb  <ip> <node>
wagtail__documents_customdocument_xtwnqfk   0     p      STARTED    90  49.8kb  <ip> <node>
wagtail__wagtaildocs_document_ajkn4li       0     p      STARTED     0    208b  <ip> <node>
wagtail__wagtaildocs_document_ajkn4li       0     r      STARTED     0    208b  <ip> <node>
wagtail__wagtailimages_image_lcgak2e        0     r      STARTED     0    208b  <ip> <node>
wagtail__wagtailimages_image_lcgak2e        0     p      STARTED     0    208b  <ip> <node>

wagtail__wagtailcore_page_bqsaiep           0     p      STARTED  3238   3.4mb  <ip> <node>
wagtail__wagtailcore_page_bqsaiep           0     r      STARTED  3238   3.4mb  <ip> <node>
wagtail__wagtailcore_page_nm7irjb           0     p      STARTED  6792  11.7mb  <ip> <node>
wagtail__wagtailcore_page_nm7irjb           0     r      STARTED  6792    12mb  <ip> <node>
wagtail__wagtailcore_page_zqkorrt           0     r      STARTED  3251   3.4mb  <ip> <node>
wagtail__wagtailcore_page_zqkorrt           0     p      STARTED  3251   3.4mb  <ip> <node>
```

In the examples above, we know that `wagtail__wagtailcore_page` is an alias of `wagtail__wagtailcore_page_nm7irjb`,
thus `wagtail__wagtailcore_page_bqsaiep` and `wagtail__wagtailcore_page_zqkorrt` are old indices that need removing.

To remove it via the Elasticsearch console/API: `DELETE /index_name` <sup>[5]</sup> (for example, `DELETE /wagtail__wagtailcore_page_bqsaiep`)

## Wagtail

If you do not have access to the Elasticsearch console, you could make use of the tools Wagtail provides via the search backend.

```python
from wagtail.search.backends import get_search_backend
from wagtail.models import Page


# get the default backend, and find the current page index
backend = get_search_backend("default")
page_index = backend.get_index_for_model(Page)

# get the index name (it is 'wagtail__wagtailcore_page')
print(page_index.name)

# get the index the page index is aliased as. in our example `wagtail__wagtailcore_page_nm7irjb`
for alias in page_index.aliased_indices():
    print(alias.name)

# check that a given index exists
print(page_index.es.indices.exists(index_name)

# list all indices.
page_index.es.cat.indices()

indices_to_delete: list[str] = []  # provide a list of index names to remove
for index_name in indices_to_delete:
	page_index.es.indices.delete(index_name)
```

> **note**
>
> You can do this using a script or via the Django shell (`django-admin shell`)


[1]: <https://docs.wagtail.org/en/stable/topics/search/backends.html#wagtailsearch-backends-atomic-rebuild> (Wagtail docs on ATOMIC_REBUILD)
[2]: <https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cat-indices.html> (Elasticsearch docs on _cat/indices)
[3]: <https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cat-alias.html> (Elasticsearch docs on _cat/alias)
[4]: <https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cat-shards.html> (Elasticsearch docs on _cat/shards)
[5]: <https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-delete-index.html> (Elasticsearch docs on deleting an index)
