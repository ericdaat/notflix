class Context(object):
    """ A wrapper for context that will help engines make recommendations.
    """
    def __init__(self, **kwargs):
        self.item = kwargs.get("item")
        self.user = kwargs.get("user")
        self.page_type = kwargs.get("page_type")
        self.history = kwargs.get("history")


class Recommendations(object):
    """ A recommendation object that is returned by the engines
    """
    def __init__(self):
        self.type = ""
        self.recommended_items = None
        self.display_name = ""
        self.priority = 0

    def to_dict(self):
        """ Convert recommendation object to dict

        Returns:
            dict: the recommendations as a dictionary
        """
        self.recommended_items = [r.as_dict() for r in self.recommended_items]

        return vars(self)

    def to_string(self):
        """ Convert recommendation object to string for debug purpose

        Returns:
            str: the recommendations as string, stating the type \
                and number of items recommended.
        """

        string = "{1} recommendations for {0}"\
                 .format(self.type, len(self.recommended_items))

        return string
