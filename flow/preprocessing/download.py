import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from queue import Queue
from threading import Lock
import requests

import assets.strings

# Globals
download_queue_lock = Lock()
download_queue = []


class DownloadRequest:
    def __init__(self, url: str, headers: dict = None, name: str = None, path: str = None):
        self.url = url
        self.headers = headers
        self.name = name
        self.path = path


class AsyncDownloader:
    __DEFAULT_THREAD_NUM = 3

    def __init__(self, thread_num=__DEFAULT_THREAD_NUM):
        self.__thread_pool = ThreadPoolExecutor(thread_num)

        if not os.path.isdir(assets.strings.SAVE_PATH):
            os.mkdir(assets.strings.SAVE_PATH)

    def __download(self, req: DownloadRequest):
        fname = req.name
        fpath = req.path
        parts = req.url.split(".")
        img_data = None
        if not req.headers:
            img_data = requests.get(req.url).content
        else:
            img_data = requests.get(req.url, headers=req.headers).content

        if not fname:
            fname = str(datetime.now()).replace(":", "").replace(".", "") + "." + parts[-1]
        if not fpath:
            fpath = assets.strings.SAVE_PATH

        with open(fpath + "\\" + fname, 'wb') as handler:
            handler.write(img_data)

        download_queue_lock.acquire()
        download_queue.remove(req)
        download_queue_lock.release()

    def submit_url(self, url, headers: dict = None, file_name: str = None, path: str = None):
        download_queue_lock.acquire()
        req = DownloadRequest(url, headers, file_name, path)
        download_queue.append(req)
        download_queue_lock.release()
        self.__thread_pool.submit(self.__download, req)
