class Recommendations(object):
    def __init__(self):
        self.type = ""
        self.ids = []
        self.scores = []
        self.display_name = ""
        self.priority = 0

    def to_dict(self):
        return {
            "type": self.type,
            "ids": self.ids,
            "scores": self.scores,
            "display_name": self.display_name,
            "priority": self.priority
        }

    def to_string(self):
        return "{1} recommendations for {0}".format(self.type,
                                                    len(self.ids))
