class Result(object):
    title = ""
    description = ""
    image_url = ""

    def __init__(self, title, description, image_url):
        self.title = title
        self.description = description
        self.image_url = image_url