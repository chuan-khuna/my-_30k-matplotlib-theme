# How to use twitter scraper

```py
scraper = TwitterScraper('path/to/header.yml')
scraper.n_lazy_load = 20

# list of tweets (dict)
data = scraper.scrape('Sawano Hiroyuki')
```
