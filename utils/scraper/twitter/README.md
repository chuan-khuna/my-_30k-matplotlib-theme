# How to use twitter scraper

```py
scraper = TwitterScraper('path/to/header.yml')
scraper.n_lazy_load = 20

# list of tweets (dict)
data = scraper.scrape('Sawano Hiroyuki')
```

A YAML file that contains **request header** params
it should contain (log in search) `['authorization', 'cookie', 'x-csrf-token']` (nov 2022)
for incognito search it also need `'x-guest-token'`