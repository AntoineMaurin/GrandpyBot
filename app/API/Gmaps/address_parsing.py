class AddressParsing:

    @classmethod
    def parse(cls, text):
        address = text.split(",")[0]
        result = "".join([i for i in address if not i.isdigit()])
        print(result)

        return result
