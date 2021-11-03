class Entry:

    def __init__(self):
        self.image_path = ""
        self.image_small = ""
        self.image_full = ""
        self.source = ""
        self.tags = []
        self.score = -1
        self.headers = {}
        self.title = None

    def as_dict(self):
        return {'path': self.image_path,
                'url': self.image_full,
                'source': self.source,
                'tags': self.tags,
                'score': self.score,
                'headers': self.headers,
                'title' : self.title
                }

    def tags_as_string(self) -> str:
        tags = ""
        for tag in self.tags:
            tags = tags + tag + "\n"
        return tags
