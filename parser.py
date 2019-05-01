import pyparsing as pp
import string
import random
import numbers

class DiceParser(object):

    def __init__(self):
        self.parser = self.get_parser()
        self.filter = self.get_filter()
        self.builder = self.get_builder()

    def get_parser(self):
        return Parser()

    def get_filter(self):
        return Filter()

    def get_builder(self):
        return Builder()

    def handle(self, string):
        print('--- Input String : {}'.format(string))
        alphanum = self.filter.filter_symbols(string)
        filtered = self.filter.filter_words(alphanum)
        token_list = self.parser.parse_string(filtered)
        if token_list:
            print(token_list)
            self.builder.build_tree(token_list[0])

class Parser(object):

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

    def parse_string(self, string_list):
        results = []
        for string in string_list:
            print('    Parsing String : {}'.format(string))
            try:
                result = self.Parser.parseString(string).asList()
                print('        Match : {}'.format(result))
                results.append(result)
            except pp.ParseException as parse_exception:
                print('        No Match')
                #print$('        No Match : {}\n'.format(str(parse_exception)))
        return results

class Filter(object):

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

class Node(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right
    
    def print_chain(self, indentation=''):
        print(indentation + self.name)
        indentation = indentation + '  '

        if isinstance(self.left, Node):
            print('{}Left:'.format(indentation))
            self.left.print_chain(indentation)
        else:
            print('{}Left: {}'.format(indentation, self.left))

        if isinstance(self.right, Node):
            print('{}Right:'.format(indentation))
            self.right.print_chain(indentation)
        else:
            print('{}Right: {}'.format(indentation, self.right))

    def calculate_value(self):
        pass

    def calculate(self):
        try:
            self.left = self.left.calculate()
        except:
            pass

        try:
            self.right = self.right.calculate()
        except:
            pass

        return self.calculate_value(self.left, self.right)

class Tree(Node):

    def __init__(self, left=None, right=None):
        self.name = 'Tree'
        super().__init__(left, right)

class Add(Node):
    
    def __init__(self, left, right):
        self.name = 'Add'
        super().__init__(left, right)

    def calculate_value(self, a, b):
        return a + b

class Sub(Node):

    def __init__(self, left, right):
        self.name = 'Sub'
        super().__init__(left, right)
    
    def calculate_value(self, a, b):
        return a - b

class Mul(Node):

    def __init__(self, left, right):
        self.name = 'Mul'
        super().__init__(left, right)

    def calculate_value(self, a, b):
        return a * b

class Div(Node):

    def __init__(self, left, right):
        self.name = 'Div'
        super().__init__(left, right)
 
    def calculate_value(self, a, b):
        return a / b

class Dice(Node):

    def __init__(self, left, right):
        self.name = 'Dice'
        super().__init__(left, right)

    def calculate_value(self, rolls, max):
        result = 0
        for x in range(rolls):
            result = result + random.randint(0, max)
        return result

#def isnum(x):
#    try:
#        if int(x):
#            return True
#    except:
#        pass

class Builder(object):

    def parse(tokens):
        """parse: tokens_iter or generator -> Node
        From an infix stream of tokens, and the current index into the
        token stream, construct and return the tree, as a collection of Nodes,
        that represent the expression."""
    
        next_tok = next(tokens)
    
        if next_tok.isdigit():
            return ('literal', next_tok)
    
        elif next_tok == "+":
            return ('add', parse( tokens ), parse( tokens )) # first argument is the node.left, second is the node.right
        elif next_tok == "-":
            return ('sub', parse( tokens ), parse( tokens ))
        elif next_tok == "*":
            return ('mul', parse( tokens ), parse( tokens ))
        elif next_tok == "/":
            return ('div', parse( tokens ), parse( tokens ))
        elif isinstance(next_tok, list()):
            return ('dice', next_tok)
        else:
            return ('variable', next_tok )

        # And, example:
        print(parse(iter(['-', '//', 'y', '2', 'x'])))

    def build_tree(self, token_list: list):
        print(token_list)
        #token_list = token_list[::-1]
        #print(token_list)

        parse(token_list)
            



        """print('Size : {}'.format(len(token_list[0])))
        print('List : {}'.format(token_list[0]))
        print('Reversed List : {}'.format(token_list[0][::-1]))"""

        """list = ['6', 'd', '6'], '*', ['5', 'd', '6'], '/', ['4', 'd', '6'], '-', ['3', 'd', '6'], '+', ['2', 'd', '6']

        list = reversed(list)

        list = ['6', 'd', '6'], '*', ['5', 'd', '6'], '/', ['4', 'd', '6'], '-', ['3', 'd', '6'], '+', ['2', 'd', '6']
        current  = ['6', 'd', '6'], '*', ['5', 'd', '6']
        first    = mul(['6', 'd', '6'], ['5', 'd', '6'])
        
        list    = '/', ['4', 'd', '6'], '-', ['3', 'd', '6'], '+', ['2', 'd', '6']
        current = '/', ['4', 'd', '6']
        second  = div(first, ['4', 'd', '6'])

        list    = '-', ['3', 'd', '6'], '+', ['2', 'd', '6']
        current = '-', ['3', 'd', '6']
        third  = sub(second, ['3', 'd', '6'])

        list    = '+', ['2', 'd', '6']
        current = '+', ['2', 'd', '6']
        fourth  = add(third, ['2', 'd', '6'])"""

        """while len(token_list[0]) > 2:
                                    print('WHILE')
                                    current = token_list[:3]
                                    print(current)
                                else:
                                    print('ELSE')"""

        """for tokens in token_list:
            print('Tokens: {}'.format(tokens))
            for token in tokens:
                if token is '+':
                    print('ADD')
                    list.append('')
                elif token is '-':
                    print('SUB')
                elif token is '*':
                    print('MUL')
                elif token is '/':
                    print('DIV')
                elif isinstance(token, list):
                    print('DICE: {}'.format(token))
                elif isnum(token):
                    print('INT: {}'.format(token))"""


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
