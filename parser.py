import pyparsing as pp
import string

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

class Translator:

    def __init__(self):
        self.translation_Table = self.__generate_table()

    def __generate_table(self):
        return str.maketrans('', '', '!"£$%^&()_={}[]:;\'\\@#~<>,.?|')

    def remove_symbols(self, string):
        return string.translate(self.translation_Table)

    def filter(self, string):
        #print('    Checking for words')
        filtered = list()
        for string in string.split():
            if string.isalpha():
                #print('        Ignored : {}'.format(string))
                continue
            else:
                filtered.append(string)
        return filtered

def test(string):
    print('--  Input String : {}'.format(string))
    alphanum = Translator.remove_symbols(string)
    filtered = Translator.filter(alphanum)
    for string in filtered:
        Parser.parse_string(string)

if __name__ == '__main__':
    Parser = Parser()
    Translator = Translator()

    test_rolls = [
        #Fail
        'd', '1d6+d', 'd0', '0d', '1d', '0d6', '1d06', '1d6+0',
        #Pass
        '5+5', 'd6', '1d6', 'd1000/10', 'd6*4', 'd6-d6', 'd6+5', 'd6+d6', 'd6+1d6', '1d6+1', '1d6+d6', '1d6+1d6', '3d12+2/1d2', '2d6+3d6-4d6/5d6*6d6'
    ]
    for roll in test_rolls:
        test(roll)

    test_string = 'This is a test of the parsers ability to seperate rolls from strings of text, for example 1d6 should be parsed and 0d5 should not.'
    test(test_string)
