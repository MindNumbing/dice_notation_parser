import pyparsing as pp
import string
import time


class DiceParser:

    def __init__(self):
        self.parser = Parser()
        self.filter = Filter()

    def handle(self, input_string):
        print('--- Input String : {}'.format(input_string))
        filtered = self.filter.filter(input_string)
        results = self.parser.parse_string(filtered)
        if results:
            return results
        return None


class Parser:

    def __init__(self):
        self.Parser = self._generate_parser()

    def _generate_parser(self):
        d = pp.Word('Dd')
        zero_digit = pp.Word(str('0'))
        non_zero_digit = pp.Word(str('123456789'))
        digit = pp.Or([zero_digit, non_zero_digit])
        non_zero_integer = pp.OneOrMore(pp.Combine(non_zero_digit + pp.ZeroOrMore(digit)))
        roll = pp.Group(pp.Optional(non_zero_integer) + d + non_zero_integer)
        term = pp.Or([non_zero_integer, roll])
        
        factor = pp.Forward()
        factor << pp.Group(term + pp.ZeroOrMore(pp.Or(['*', '/']) + factor))

        expr = pp.Forward()
        expr << pp.Group(factor + pp.ZeroOrMore(pp.Or(['+', '-']) + expr))

        return expr

    def parse_string(self, input_string):
        results = []
        for word in string_list:
            try:
                result = self.Parser.parseString(string, parseAll=True).asList()
                results.append(result[0])
            except pp.ParseException as parse_exception:
                print(parse_exception.line)
                print(' ' * (parse_exception.col - 1) + '^')
                print(parse_exception)
                pass
        return results


class Filter:

    def __init__(self):
        self.translation_table = self._generate_table()

    def filter(self, input_string):
        alphanum = self.filter_symbols(input_string)
        filtered = self.filter_words(alphanum)
        return filtered

    def _generate_table(self):
        return str.maketrans('', '', '!"£$%^&()_={}[]:;\'\\@#~<>,.?|')

    def filter_symbols(self, input_string):
        return input_string.translate(self.translation_table)

    def filter_words(self, input_string):
        # print('    Checking for words')
        filtered = list()
        for word in input_string.split():
            if word.isalpha():
                # print('        Ignored : {}'.format(word))
                continue
            else:
                filtered.append(word)
        return filtered


class TestHandler:

    def __init__(self, test_cases):
        if test_cases:
            self.test_cases = test_cases
        self.dice_parser = DiceParser()

    def run_tests(self):
        for test in self.test_cases:
            print('')
            print('Processing : {}'.format(test[0]))
            result = self.dice_parser.handle(test[0])

            if result == test[1]:
                print('ASSERT - PASS\nResult   : {}\nExpected : {}'.format(result, test[1]))
            else:
                print('ASSERT - FAIL\nResult   : {}\nExpected : {}'.format(result, test[1]))


if __name__ == '__main__':
    test_input = [
        # Fail
        ('d', None),
        ('1d6+d', None),
        ('d0', None),
        ('0d', None),
        ('1d', None),
        ('0d6', None),
        ('1d06', None),
        ('1d6+0', None),
        # Pass - Add extra list for result
        ('5+5', [[['5'], '+', [['5']]]]),
        ('5+5+5', [[['5'], '+', [['5'], '+', [['5']]]]]),
        ('d6', [[[['d', '6']]]]),
        ('1d6', [[[['1', 'd', '6']]]]),
        ('d1000/10', [[[['d', '1000'], '/', ['10']]]]),
        ('d6*4', [[[['d', '6'], '*', ['4']]]]),
        ('d6+5', [[[['d', '6']], '+', [['5']]]]),
        ('d6-d6', [[[['d', '6']], '-', [[['d', '6']]]]]),
        ('d6+d6', [[[['d', '6']], '+', [[['d', '6']]]]]),
        ('d6+1d6', [[[['d', '6']], '+', [[['1', 'd', '6']]]]]),
        ('1d6+1', [[[['1', 'd', '6']], '+', [['1']]]]),
        ('1d6+d6', [[[['1', 'd', '6']], '+', [[['d', '6']]]]]),
        ('1d6+1d6', [[[['1', 'd', '6']], '+', [[['1', 'd', '6']]]]]),
        ('1d6+1d6+1d6', [[[['1', 'd', '6']], '+', [[['1', 'd', '6']], '+', [[['1', 'd', '6']]]]]]),
        ('3d12+2/1d2', [[[['3', 'd', '12']], '+', [['2', '/', [['1', 'd', '2']]]]]]),
        ('2d6+3d6-4d6/5d6*6d6', [[[['2', 'd', '6']], '+', [[['3', 'd', '6']], '-', [[['4', 'd', '6'], '/', [['5', 'd', '6'], '*', [['6', 'd', '6']]]]]]]]),
        ('1d6*2d7', [[[['1', 'd', '6'], '*', [['2', 'd', '7']]]]]),
        ('2d7/9d18', [[[['2', 'd', '7'], '/', [['9', 'd', '18']]]]]),
        ('9d18+6', [[[['9', 'd', '18']], '+', [['6']]]]),
        ('6/4', [[['6', '/', ['4']]]]),
        ('4-20', [[['4'], '-', [['20']]]]),
        ('1d6*2d7', [[[['1', 'd', '6'], '*', [['2', 'd', '7']]]]]),
        ('1d6*2d7/9d18', [[[['1', 'd', '6'], '*', [['2', 'd', '7'], '/', [['9', 'd', '18']]]]]]),
        ('1d6*2d7/9d18+6', [[[['1', 'd', '6'], '*', [['2', 'd', '7'], '/', [['9', 'd', '18']]]], '+', [['6']]]]),
        ('1d6*2d7/9d18+6/4', [[[['1', 'd', '6'], '*', [['2', 'd', '7'], '/', [['9', 'd', '18']]]], '+', [['6', '/', ['4']]]]]),
        ('1d6*2d7/9d18+6/4-20', [[[['1', 'd', '6'], '*', [['2', 'd', '7'], '/', [['9', 'd', '18']]]], '+', [['6', '/', ['4']], '-', [['20']]]]])
    ]

    test_handler = TestHandler(test_input)
    test_handler.run_tests()

    # test_string = 'This is a test of the parsers ability to seperate rolls from strings of text, for example 1d6 should be parsed and 0d5 should not.'
    # results.append(dice_parser.handle(test_string))

    # for result in results:
    #    print(result)