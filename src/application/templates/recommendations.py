class Recommendations(object):
    def __init__(self):
        self.engine_name = ""
        self.ids = []
        self.scores = []

    def to_dict(self):
        return {
            "engine_name": self.engine_name,
            "ids": self.ids,
            "scores": self.scores
        }

    def to_string(self):
        return "{1} recommendations for {0}".format(self.engine_name,
                                                    len(self.ids))
