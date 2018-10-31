class Recommendations(object):
    def __init__(self):
        self.type = ""
        self.items = None
        self.display_name = ""
        self.priority = 0

    def to_dict(self):
        return vars(self)

    def to_string(self):
        return "{1} recommendations for {0}".format(self.type,
                                                    len(self.items))
