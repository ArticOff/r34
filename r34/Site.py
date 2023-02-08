# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2023-today Artic

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from typing import Union

from innerhtml import Page, Tag
from requests import post, Response

from .Gateway import getURL, Route
from .Constants import URL
from .Types import Post, User
from .Errors import VoidError

def search(tags: Union[tuple[str, ...], str] = None, blacklist: Union[tuple[str, ...], str] = None, page: int = 0, limit: int = -1) -> list[Post]:
    """
    from https://rule34.us/index.php?r=help/search

    ## Basic Usage Documentation
    The following code if entered into the search box will match any categories with tags that start with ab and end with d.
    >>> ab*d

    You are able to remove potential results by simply adding a - in front of what you wish to negate. This will search for anything that does not have cat_ears as a tag.
    >>> -cat_ears

    This will search the site contents with a title of ab*. The asterisk is a wildcard and will match anything that starts with ab.
    >>> title:ab*

    Will search for any category with a rating of explicit. Supports explicit, questionable, and safe. Most content is rated explicit, so this metasearch is almost never needed.
    >>> rating:explicit

    You are able to search for posts by a certain user as well.
    >>> user:anonymous

    You can search as well by the post's id. This will find post ID number 1.
    >>> id:1

    ## Advanced Usage Documentation

    Slightly more advanced is OR searching. This search allows you to search for tags that have one tag OR another tag. This query will show posts with cat_ears that have a car, what, or absolutely_everyone in them.
    >>> cat_ears {car ~ what ~ absolutely_everyone}

    You can combine everything above to make a larger query to bring your results down to a managable result count. The idea is that the more specific you are in searching, the less you will get in associated results.
    >>> glasses green_eyes -skirt -title:sa* {car ~ what ~ absolutely_everyone}
    """
    enable_limit: bool = True if limit > 0 else False
    count: int = 0
    if tags:
        if blacklist:
            if isinstance(tags, str):
                page: Page = getURL(f"/index.php?r=posts/index&q={tags.replace(' ', '+')}+-{blacklist.replace(' ', '+-') if isinstance(blacklist, str) else '+-'.join(blacklist)}&page={page}")
            else:
                page: Page = getURL(f"/index.php?r=posts/index&q={'+'.join(tags)}+-{blacklist.replace(' ', '+-') if isinstance(blacklist, str) else '+-'.join(blacklist)}&page={page}")
        else:
            if isinstance(tags, str):
                page: Page = getURL(f"/index.php?r=posts/index&q={tags.replace(' ', '+')}&page={page}")
            else:
                page: Page = getURL(f"/index.php?r=posts/index&q={'+'.join(tags)}&page={page}")
    else:
        if blacklist:
            if isinstance(tags, str):
                page: Page = getURL(f"/index.php?r=posts/index&q=-{blacklist.replace(' ', '+-') if isinstance(blacklist, str) else '+-'.join(blacklist)}&page={page}")
            else:
                page: Page = getURL(f"/index.php?r=posts/index&q=-{blacklist.replace(' ', '+-') if isinstance(blacklist, str) else '+-'.join(blacklist)}&page={page}")
        else:
            page: Page = getURL(f"/index.php?r=posts/index&page={page}")
    pages: list[str] = []
    for element in page._html:
        if "<a id=\"" in element:
            count += 1
            tag: Tag = Tag(element)
            url: str = [i for i in tag.tag.split(" ") if "href" in i][0].split("\"")[1]
            post: Post = Post(getURL(url.replace("amp;", "").removeprefix(f"{URL}/")))
            pages.append(post)
            if enable_limit:
                if count == limit:
                    return pages
    if len(pages) == 0:
        raise VoidError("There's nothing on this page.")
    return pages

def fetchPost(_id: int, page: int = 0) -> Post:
    return Post(getURL(f"/index.php?r=posts/view&id={_id}&page={page}"))

def fetchUser(_id: int) -> User:
    return User(getURL(f"/index.php?r=account/profile&id={_id}"))

def fetchPosts(_ids: tuple[int, ...]) -> list[Post]:
    posts: list[Post] = []
    for _id in _ids:
        post: Post = fetchPost(_id)
        posts.append(post)
    return posts

def fetchUsers(_ids: tuple[int, ...]) -> list[User]:
    users: list[Post] = []
    for _id in _ids:
        user: User = fetchUser(_id)
        users.append(user)
    return users

def ranking() -> dict[str, int]:
    page: Page = getURL("/index.php?r=statistics/ranking")
    rank: dict[str, int] = {}
    for element in page._html:
        if "top-list" in element:
            for count, tag in enumerate(element.split("><")):
                if "index.php?r=posts/index&q=" in tag:
                    name: str = Tag(f"<{tag}>").content
                    points: int = int(Tag(f"<{element.split('><')[count + 2]}>").content)
                    rank[name] = points
            else:
                return rank
            
def maxPosts() -> int:
    lastPost: Post = search(limit=1)[0]
    return lastPost.url.split("=")[-1]