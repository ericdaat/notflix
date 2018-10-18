class Context(object):
    def __init__(self, **kwargs):
        self.user_id = kwargs.get("user_id")
        self.item_id = kwargs.get("item_id")
