# Common problems snippets

## Create folder if not exists

```py
# folder_path ...
if not os.path.exists(folder_path):
    os.makedirs(folder_path, exist_ok=True)
```
