class Result(object):
    title = ""
    description = ""
    image_url = ""
    image_text = ""
    keywords = ""
    date = ""
    last_modified = ""
    content = ""
    url = ""

    def __init__(self, fill_with_dict):
        for k, v in fill_with_dict.items():
            setattr(self, k, v)