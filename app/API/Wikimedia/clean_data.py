import re

class CleanData:

    @classmethod
    def clean(cls, data):
        return  " ".join(data.split())
