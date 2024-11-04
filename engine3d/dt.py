class DataTable:
    def __init__(self, name: str, **kwargs):
        self.name = name

        for key, value in kwargs.items():
            setattr(self, key, value)
