class AddressParsing:

    def parse(text):
        address = text.split(",")[0]
        result = "".join([i for i in address if not i.isdigit()])
        return result
