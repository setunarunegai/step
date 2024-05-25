#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_times(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def read_devide(line, index):
    token = {'type': 'DEVIDE'}
    return token, index + 1

def read_bracket_begin(line, index):
    token = {'type': 'BRACKET_BEGIN'}
    return token, index + 1

def read_bracket_end(line, index):
    token = {'type': 'BRACKET_END'}
    return token, index + 1

def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3

def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3

def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
        elif line[index] == '/':
            (token, index) = read_devide(line, index)
        elif line[index] == '(':
            (token, index) = read_bracket_begin(line, index)
        elif line[index] == ')':
            (token, index) = read_bracket_end(line, index)
        elif line[index] == 'a':
            (token, index) = read_abs(line, index)
        elif line[index] == 'i':
            (token, index) = read_int(line, index)
        elif line[index] == 'r':
            (token, index) = read_round(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def there_function(tokens, begin_index, ans):
    there_func = 0
    if begin_index - 1 >= 0:
        if tokens[begin_index - 1]['type'] == 'ABS':
            ans = abs(ans)
            there_func += 1
        elif tokens[begin_index - 1]['type'] == 'INT':
            ans = int(ans)
            there_func += 1
        elif tokens[begin_index - 1]['type'] == 'ROUND':
            ans = round(ans)
            there_func += 1
    return there_func, ans

def delparen(tokens):
    begin = [] # (がどのインデックスにあるか
    end = [] # 対応する(と同じインデックスに入れた
    begin_least = [] # (がどの順番で出たか
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'BRACKET_BEGIN':
            begin.append(index)
            end.append(0) #インデックスにアクセスするため枠を増やしておく
            begin_least.append(len(begin) - 1)
        elif tokens[index]['type'] == 'BRACKET_END':
            end[begin_least[len(begin_least) - 1]] = index
            begin_least.pop()
        index += 1
    index = len(begin) - 1
    while index >= 0: #右の(から計算していく
        if tokens[begin[index] + 1]=='-':
            ans = evaluate(tokens[begin[index] + 2 : end[index]])
            ans = (-1)*ans
        else:
            ans = evaluate(tokens[begin[index] + 1 : end[index]])
        (there_func, ans) = there_function(tokens, begin[index], ans)
        tokens[end[index]] = {'type': 'NUMBER', 'number': ans} # )をnumberに変える
        del tokens[begin[index] - there_func : end[index]] #abs(~)のうち、abs(~の部分を削除 )はnumberに変わっている
        for i in range(0, index): #消した分のindexをずらす
            if end[i] > end[index]:
                end[i] -= end[index] - begin[index] + there_func
        index -= 1
    return tokens

def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 0 
    while index + 1 < len(tokens): # *と/を先に計算する
        if tokens[index]['type'] == 'TIMES':
            tokens[index - 1]['number'] *= tokens[index + 1]['number']
            del tokens[index : (index + 2)]
        elif tokens[index]['type'] == 'DEVIDE':
            if tokens[index + 1]['number'] == 0: #0で割らないように
                print('divide by zero')
                exit(1)
            tokens[index - 1]['number'] /= tokens[index + 1]['number']
            del tokens[index : (index + 2)]
        else:
            index+=1
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print(tokens)
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    tokens = delparen(tokens)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1")
    test("0")
    test("3.0")
    test("3.1")
    test("3.10")

    test("1+2")
    test("1.1+2.0")
    test("1.0+4")
    test("0+4.0")
    test("4.1+0")
    test("1-2")
    test("1.1-2.0")
    test("1.0-4")
    test("0-4.0")
    test("4.1-0")
    test("1*2")
    test("1.1*2.0")
    test("1.0*4")
    test("0*4.0")
    test("4.1*0")
    test("10000000000*10000000000*10000000000*1000000000")
    test("100000000000000000000000000000000000000*1000000000")
    test("1/2")
    test("2/1")
    test("1.1/2.0")
    test("1.0/4")
    test("0/4.0")

    test("2.0+3.0-4.0")
    test("2.0+3.0*4.0")
    test("2.0+3.0/4.0")
    test("2.0-3.0*4.0")
    test("2.0-3.0/4.0")
    test("2.0*3.0/4.0")

    test("4+5*3/2-5+10*2*4/5+1")

    test("(3+2)")
    test("(3+2)*4")
    test("4*(3+2)")
    test("(3+2)/4")
    test("(3+4)/2")
    test("(3*(3+4))-10")
    test("(9+3)*(4+2)")
    test("(7*(3+1)-3)*(5+4)")
    test("(7*(3+1)-3)/(5+4)")

    test("abs(2.2)")
    test("abs(-2.3)")
    test("int(1.55)")
    test("int(3)")
    test("int(-1.9)")
    test("int(-4)")
    test("round(1.55)")
    test("round(3)")
    test("round(-1.4)")
    test("round(-3)")
    test("abs(int(round(-1.55)+abs(int(-2.3+4))))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    tokens = delparen(tokens) 
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
