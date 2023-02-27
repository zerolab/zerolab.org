---
title: "Loading .env variables in Makefile"
date: 2023-02-27T20:37:00Z
source: https://lithic.tech/blog/2020-05/makefile-dot-env
---

If you're using a Makefile and need to make use of variables from a `.env` file, you can add

```Makefile
ifneq (,$(wildcard ./.env))
    include .env
    export
endif
```

to the top of the Makefile. Then you can use those like in any shell script. (e.g. `@echo "${HOST}"`)