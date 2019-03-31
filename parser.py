import pyparsing as pp
import string

class DiceParser:

    def __init__(self):
        self.parser = self.get_parser()
        self.filter = self.get_filter()

    def get_parser(self):
        return Parser()

    def get_filter(self):
        return Filter()

    def handle(self, string):
        print('--- Input String : {}'.format(string))
        alphanum = self.filter.filter_symbols(string)
        filtered = self.filter.filter_words(alphanum)
        for string in filtered:
            self.parser.parse_string(string)

class Parser:

    def __init__(self):
        self.Parser = self.__generate_parser()

    def __generate_parser(self):
        D = pp.Word('Dd')
        ZeroDigit = pp.Word(str('0'))
        NonZeroDigit = pp.Word(str('123456789'))
        Digit = pp.Or([ZeroDigit, NonZeroDigit])
        NonZeroInteger = pp.OneOrMore(pp.Combine(NonZeroDigit + pp.ZeroOrMore(Digit)))
        Die = pp.Group(pp.Optional(NonZeroInteger) + D + NonZeroInteger)
        Operator = pp.Word(r'+-*/')
        Parser = pp.Or([Die, pp.OneOrMore(pp.Or([Die, NonZeroInteger]) + Operator) + pp.Or([Die, NonZeroInteger])])

        return Parser

    def parse_string(self, string):
        print('    Parsing String : {}'.format(string))
        try:
            result = self.Parser.parseString(string)
            print('        Match : {}'.format(result))
            return result
        except pp.ParseException as parse_exception:
            print('        No Match')
            #print$('        No Match : {}\n'.format(str(parse_exception)))

class Filter:

    def __init__(self):
        self.translation_table = self.__generate_table()

    def __generate_table(self):
        return str.maketrans('', '', '!"£$%^&()_={}[]:;\'\\@#~<>,.?|')

    def filter_symbols(self, string):
        return string.translate(self.translation_table)

    def filter_words(self, string):
        #print('    Checking for words')
        filtered = list()
        for string in string.split():
            if string.isalpha():
                #print('        Ignored : {}'.format(string))
                continue
            else:
                filtered.append(string)
        return filtered

if __name__ == '__main__':
    dice_parser = DiceParser()

    test_rolls = [
        #Fail
        'd', '1d6+d', 'd0', '0d', '1d', '0d6', '1d06', '1d6+0',
        #Pass
        '5+5', 'd6', '1d6', 'd1000/10', 'd6*4', 'd6-d6', 'd6+5', 'd6+d6', 'd6+1d6', '1d6+1', '1d6+d6', '1d6+1d6', '3d12+2/1d2', '2d6+3d6-4d6/5d6*6d6'
    ]
    for roll in test_rolls:
        dice_parser.handle(roll)

    test_string = 'This is a test of the parsers ability to seperate rolls from strings of text, for example 1d6 should be parsed and 0d5 should not.'
    dice_parser.handle(test_string)
