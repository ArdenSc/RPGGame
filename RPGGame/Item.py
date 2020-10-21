class Item:
    def __init__(self, name: str, **kwargs: str):
        self.name = name
        self.data = kwargs

    def __str__(self):
        return self.name
