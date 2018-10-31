class Context(object):
    def __init__(self, **kwargs):
        self.item_id = kwargs.get("item_id")
        self.user_id = kwargs.get("user_id")
