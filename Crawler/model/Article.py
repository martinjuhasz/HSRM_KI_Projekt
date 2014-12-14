class Article(object):

    def __init__(self):
        self.title = ""
        self.description = ""
        self.keywords = ""
        self.date = ""
        self.last_modified = ""
        self.content = ""
        self.images = []
        self.url = ""

    def __repr__(self):
        representation = "Article[" \
                         "title=\"{title:.30}...\" " \
                         "description=\"{description:.30}...\" " \
                         "keywords=\"{keywords:.30}...\" " \
                         "date=\"{date}\" " \
                         "last_modified=\"{last_modified}\" " \
                         "content=\"{content:.30}...\" " \
                         "images=\"{images}\" " \
                        "]".format(**self.__dict__)
        return representation
