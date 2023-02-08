
# r34

Library for retrieving posts and tags from rule34.us

## Authors

- [@ArticOff](https://www.github.com/ArticOff)


## Installation

Install info with pip

```bash
# Linux/macOS
python3 -m pip install -U r34

# Windows
py -3 -m pip install -U r34
```
    
## Usage/Examples

### These codes are pretty slow because it takes on the HTML

> search by tags
```py
import r34

posts = r34.search("1girls")

for post in posts:
    print(post.url)

return
```

> get posts by their id
```py
import r34

posts = [1, 2, 3, 4, 5]

new_posts = r34.fetchPosts(posts)

for post in new_posts:
    print(post.media)

return
```


## Feedback

If you have any feedback, please reach out to us on [our discord](https://articoff.github.io/discord)

## Links

- [Official discord server](https://articoff.github.io/discord)
- [Source](https://github.com/ArticOff/r34)