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

from os import getcwd, chdir

from innerhtml import Page, Tag
from requests import get, Response

from .Constants import INDEX, URL
from .Media import save
from .Gateway import getURL

class User(object):
    def __init__(self, page: Page) -> None:
        self.data: dict[str, object] = {}
        for element in page._html:
            if "h2" in element and Tag(element).content != "":
                self.data["Name"] = Tag(element).content
            if "<tr class=\"account\">" in element:
                self.data[element.split("><")[1].split(">")[1].split("<")[0]] = int(element.split("><")[2].split(">")[1].split("<")[0]) if element.split("><")[2].split(">")[1].split("<")[0].isdigit() else element.split("><")[2].split(">")[1].split("<")[0]

        self.name: str = self.data["Name"],
        self.contact: str = self.data["Contact"]
        self.join_at: str = self.data["Join Date"]
        self.level: str = self.data["Level"],
        self.tags: str = self.data["Favorite Tags"]
        self.posts: int = self.data["Posts"]
        self.deleted_posts: int = self.data["Deleted Posts"]
        self.favorites: int = self.data["Favorites"]
        self.comments: int = self.data["Comments"]
        self.tag_edits: int = self.data["Tag Edits"]
        self.points: int = self.data["Points"]

        return

    def __str__(self) -> str:
        return f"<User {self.data}>"
    
    def __repr__(self) -> str:
        return f"<User {self.data}>"

class Comment(object):
    def __init__(self, user: User, comment: str, date: str) -> None:
        self.author: User = user
        self.content: str = comment
        self.date: str = date
    
    def __str__(self) -> str:
        return f"<Commment {self.content}>"
    
    def __repr__(self) -> str:
        return f"<Commment {self.content}>"
    
class Post(object):
    def __init__(self, page: Page) -> None:
        self.data: dict[str, object] = {}
        self.tag: dict[str, list] = {}
        self._tags: bool = False
        self.tags: list[str] = []
        self.metadatas: list[str] = []
        self.allTags: list[str] = []
        self.isactual: bool = False
        self.media: list[str] = []
        self.brek: bool = False
        self._id: int
        self.url: str
        self.size: tuple[int, int]
        self.added_by: tuple[str, str]
        self.created: str
        self.score: int
        self.comments: list[Comment] = []
        for element in page._html: 
            if self._tags:
                if "<div class=\"content_push\">" in element:
                    self._tags: bool = False
                    continue
                if "Id: " in element:
                    tag: Tag = Tag(element)
                    self._id: int = int(tag.content.split(" ")[1])
                    self.url: str = f"{INDEX}?r=posts/view&id={self._id}"
                if "Size: " in element:
                    tag: Tag = Tag(element)
                    self.size: tuple[int, int] = (int(tag.content.split(" ")[1].removesuffix("w")), int(tag.content.split(" ")[3].removesuffix("h")))
                if "Added by: " in element:
                    tag: Tag = Tag(element.split("Added by: ")[1].removesuffix("</li>"))
                    url: str = tag.tag.split('"')[1]
                    self.added_by: tuple[str, str] = (tag.content, f"{URL}/{url}")
                if "Created: " in element:
                    tag: Tag = Tag(element.split("Created: ")[1].removesuffix("</li>"))
                    self.created: str = tag.content
                if "Score: " in element:
                    tag: Tag = Tag(" ".join(element.split("Score: ")[1].removesuffix("</li>").split(" ")[:2]))
                    self.score: int = int(tag.content)
                self.tags.append(element)
                continue
            if "https://img2.rule34.us/images/" in element:
                tag: Tag = Tag(element)
                self.media.append(tag.getAttribute("src"))
            if "https://video.rule34.us/images/" in element and "source" in element:
                tag: Tag = Tag(element)
                self.media.append(tag.getAttribute("src"))
            if "commentBox" in element:
                user: User = User(getURL(" ".join(element.split("><")[1].split(" ")[7:-12]).split("\"")[1]))
                date: str = " ".join(" ".join(element.split("><")[1].split(" ")[7:]).split("<")[1].split(" ")[3:-1])
                comment: str = element.split("><")[4].removeprefix("/a>  ").replace("<br />", "")
                self.comments.append(Comment(user, comment, date))     
            if "tag-list" in element:
                self._tags: bool = True
                continue
        for element in self.tags:
            if self.brek:
                break
            if len([i.split(">")[1].split("<")[0] for i in element.split("><") if "b>" in i]) != 0:
                self.metadatas: list[str] = [i.split(">")[1].split("<")[0] for i in element.split("><") if "b>" in i]
            for __tag in element.split("><"):
                _tag: str = f"<{__tag}>"
                tag: Tag = Tag(_tag)
                if not tag.content.strip():
                    continue
                if tag.content == "Tools":
                    self.brek: bool = True
                    continue
                self.allTags.append(tag.content)
        for meta in self.metadatas:
            try:
                self.tag[self.allTags[self.allTags.index(meta):self.allTags.index(self.metadatas[self.metadatas.index(meta) + 1])][0]] = self.allTags[self.allTags.index(meta):self.allTags.index(self.metadatas[self.metadatas.index(meta) + 1])][1:]
            except IndexError:
                self.tag["-".join(self.allTags[self.allTags.index(meta):]).split("-")[0]] = "-".join(self.allTags[self.allTags.index(meta):]).split("-")[1:]
        self.data["tag"] = self.tag
        self.data["media"] = self.media
        self.data["id"] = self._id
        self.data["url"] = self.url
        self.data["size"] = self.size
        self.data["added_by"] = self.added_by
        self.data["created"] = self.created
        self.data["score"] = self.score
        self.data["comments"] = self.comments
        return

    def __str__(self) -> str:
        return f"<Post {self.data}>"
    
    def download(self, path: str = getcwd(), fileName: str = None, limit: bool = True, use_ffmpeg: bool = False) -> None:
        chdir(path)

        if limit:
            return save(self.media[0], fileName, use_ffmpeg)
        for media in self.media:
            save(media, fileName, use_ffmpeg)

        return

class Client(User):
    def __init__(self, page: Page) -> None:
        super().__init__(page)