import re

class CleanData:

    @classmethod
    def clean(cls, html):
        clean = re.compile('<.*?>')
        clean_result = re.sub(clean, '', html)
        return  " ".join(clean_result.split())
