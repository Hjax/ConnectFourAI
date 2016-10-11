
class book:
    def __init__(self):
        self.book = {
                    "" : "3",
                    "0": "3",
                    "1": "2",
                    "2": "3",
                    "3": "3",
                    "30":"3",
                    "31":"1",
                    "32":"5",
                    "33":"3",
                    "030": "3",
                    "031": "3",
                    "032": "3",
                    "033": "3",
                    "034": "3",
                    "035": "3",
                    "036": "2",
                    "120": "2",
                    "121": "1",
                    "122": "2",
                    "123": "3",
                    "124": "2",
                    "125": "2",
                    "126": "2",
                    "230": "3",
                    "231": "3",
                    "232": "2",
                    "233": "0",
                    "234": "3",
                    "235": "3",
                    "236": "3",
                    "330": "3",
                    "331": "2",
                    "332": "1",
                    "333": "3",
                    "3333": "3"
                    }
    def reverse(self, line):
        return "".join([str(6 - int(x)) for x in line])
    def inBook(self, line):
        return line in self.book.keys() or self.reverse(line) in self.book.keys()
    def getMove(self, line):
        if line in self.book.keys():
            return self.book[line]
        else:
            return self.reverse(self.book[self.reverse(line)])
