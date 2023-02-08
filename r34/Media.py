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

from typing import Final
from os import popen, system

from requests import get, Response

ffmpegIsInstalled: Final[bool] = "gcc" in popen("ffmpeg -version").read()

def raiseEW() -> None:
    print("If you are trying to change the media extension, install ffmpeg (https://ffmpeg.org/download.html) and set the \"use_ffmpeg\" argument to True")
    return

def save(url: str, fileName: str = None, use_ffmpeg: bool = False) -> None:
    _file: Response = get(url)
    ext: str = _file.url.split('/')[-1].split('.')[1]

    fileName: str = fileName or _file.url.split("/")[-1]

    if len(fileName.split(".")) != 1:
        if ext.lower() != fileName.split(".")[-1].lower():
            if use_ffmpeg:
                if not ffmpegIsInstalled:
                    raiseEW()
                    fileName: str = _file.url.split("/")[-1]
                else:
                    system(f"ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i \"{url}\" {fileName}")
                return
            else:
                raiseEW()
                fileName: str = _file.url.split("/")[-1]

    with open(fileName, mode="wb") as file:
        file.write(_file.content)
        file.close()

    return