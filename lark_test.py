from lark import Lark, Transformer, v_args


try:
    input = raw_input   # For Python2 compatibility
except NameError:
    pass


calc_grammar = """
    ?start: sum

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> number
         | "-" atom         -> neg
         | NAME             -> var
         | "(" sum ")"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)    # Affects the signatures of the methods
class CalculateTree(Transformer):
    # number = int

    def number(self, a: any) -> str:
        return f"const {str(a)}\n"

    def add(self, a: any, b: any) -> str:
        return a + b + "call Int:plus\n"

    def sub(self, a: any, b: any) -> str:
        return a + b + "call Int:minus\n"

    def mul(self, a: any, b: any) -> str:
        return a + b + "call Int:times\n"

    def div(self, a: any, b: any) -> str:
        return a + b + "call Int:divide\n"

    def __init__(self):
        self.vars = {}

    def assign_var(self, name, value):
        self.vars[name] = value

        return str(value) + f"store {name}"

    def var(self, name):
        # return self.vars[name]
        if name in self.vars.keys():
            return f"load {name}\n"
        else:
            raise Exception("Variable not found: %s" % name)



calc_parser = Lark(calc_grammar, parser='lalr', transformer=CalculateTree())
calc = calc_parser.parse


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(calc(s))


def test():
    print(calc("1 + 2 * 3"))


if __name__ == '__main__':
    # test()
    main()
