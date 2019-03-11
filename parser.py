import pyparsing as pp

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
        print('---- Parsing String : {}'.format(string))
        try:
            result = self.Parser.parseString(string)
            print('     Match : {}'.format(result))
            return result
        except pp.ParseException as parse_exception:
            print('     No Match')
            #print$('     No Match : {}\n'.format(str(parse_exception)))

if __name__ == '__main__':
    Parser = Parser()

    test_rolls = [
        #Fail
        'd', '1d6+d', 'd0', '0d', '1d', '0d6', '1d06', '1d6+0',
        #Pass
        '5+5', 'd6', '1d6', 'd1000/10', 'd6*4', 'd6-d6', 'd6+5', 'd6+d6', 'd6+1d6', '1d6+1', '1d6+d6', '1d6+1d6', '3d12+2/1d2', '2d6+3d6-4d6/5d6*6d6'
    ]

    for roll in test_rolls:
        Parser.parse_string(roll)
