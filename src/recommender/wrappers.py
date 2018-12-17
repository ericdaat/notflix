class Context(object):
    def __init__(self, **kwargs):
        self.item = kwargs.get("item")
        self.user = kwargs.get("user")
        self.page_type = kwargs.get("page_type")


class Recommendations(object):
    def __init__(self):
        self.type = ""
        self.products = None
        self.display_name = ""
        self.priority = 0

    def to_dict(self):
        self.products = [r.as_dict() for r in self.products]

        return vars(self)

    def to_string(self):
        return "{1} recommendations for {0}".format(self.type,
                                                    len(self.products))
