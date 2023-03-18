---
title: "Watching <code>psql</code> queries"
date: "2023-03-18 12:59:45.276335 +0000 GMT"
tags: ["sql", "psql"]
---

You can use `psql`'s `\watch` meta-command,  which re-executes a query every `n` seconds. Example usage:

```sql
SELECT pid, (CURRENT_TIMESTAMP - query_start) as query_time, datname, usename, query
FROM pg_stat_activity
ORDER BY query_time DESC
\watch 1
```

so you get `tail -f`-like functionality within `psql`.

h/t Chris Shaw