import lexer, sys

# Global variables for state management
next = 0
symbols = {}
tokens = []


def match(expected):
  """
    Check if the next token matches what's expected
    """
  global next

  if len(tokens) == 0:
    print("Unexpected end of input")
    quit()

  if tokens[next].type != expected:
    print("Expected", expected, "got", tokens[next].type)
    quit()

  # Advance to the next token
  next += 1


def check(test):
  """
    Helper method to check the next token without advancing
    """
  return tokens[next].type == test


def expression():
  """
    Expression --> Term [('+' | '-') Expression]
    """
  result = term()

  while check('PLUS') or check('MINUS'):
    if check('PLUS'):
      match('PLUS')
      result += term()
    elif check('MINUS'):
      match('MINUS')
      result -= term()

  return result


def term():
  """
    Term --> Factor [('*' | '/') Term]
    """
  result = factor()

  while check('MULTIPLY') or check('DIVIDE'):
    if check('MULTIPLY'):
      match('MULTIPLY')
      result *= factor()
    elif check('DIVIDE'):
      match('DIVIDE')
      result /= factor()

  return result


def factor():
  """
    Factor --> '-' Factor | Atom
    """
  if check('MINUS'):
    match('MINUS')
    return -factor()
  else:
    return atom()


def atom():
  """
    Atom --> Name | Number | '(' Expression ')'
    """
  if check('NAME'):
    var_name = tokens[next].value
    if var_name in symbols:
      var = symbols[var_name]
    else:
      raise ValueError(f"Undefined variable: {var_name}")
    match('NAME')
    return var
  elif check('NUMBER'):
    num = int(tokens[next].value)
    match('NUMBER')
    return num
  elif check('LPAREN'):
    match('LPAREN')
    value = expression()
    match('RPAREN')
    return value
  else:
    raise SyntaxError("Invalid syntax")


def assign_statement():
  """
  AssignStatement --> Name ':=' Expression
  """
  name = tokens[next].value
  match('NAME')
  match('ASSIGN')
  expr_value = expression()
  symbols[name] = expr_value


def input_statement():
  """
    InputStatement --> 'input' Name
    """
  match('INPUT')
  name = tokens[next].value
  match('NAME')
  value = int(input(f"Enter a value for {name}: "))
  symbols[name] = value


def print_statement():
  """
    PrintStatement --> 'print' Expression
    """
  match('PRINT')
  value = expression()
  print(value)


def while_statement():
  """
    WhileStatement --> 'while' Condition ':' Block 'end'
  """ ""
  global next

  # Match the starting keyword
  match('WHILE')

  # Keep track of starting/end position in the token sequence
  startPos = next
  endPos = next

  # Call the condition function
  while (condition()):
    # Match the colon
    match('COLON')

    # Call the block() function to process the statement block
    block()

    endPos = next
    # Reset position back to the starting position
    next = startPos

  # If condition was false, go back to last position before
  next = endPos
  match('END')


def do_while_statement():
  """
    DoWhileStatement --> 'do' ':' Block 'end' 'while' Condition
  """ ""
  global next

  # Match the starting keyword
  match('DO')

  # Match ':' keyword
  match('COLON')

  # Keep track of starting/end position in the token sequence
  startPos = next

  # Loop at least once
  while True:
    block()

    # Match the end keyword
    match('END')

    # Match while
    match('WHILE')

    # Condition to check whether to continue or break the loop
    if not condition():
      break

    # Reset position back to the starting position
    next = startPos


def evaluate_condition(left, operator, right):
  """
  Evaluate the condition based on the operator
  """
  if operator == 'EQUAL':
    return left == right
  elif operator == 'NOT_EQUAL':
    return left != right
  elif operator == 'GREATER_THAN':
    return left > right
  elif operator == 'LESS_THAN':
    return left < right
  elif operator == 'GREATER_THAN_OR_EQUAL':
    return left >= right
  elif operator == 'LESS_THAN_OR_EQUAL':
    return left <= right
  else:
    raise ValueError("Invalid relational operator")


def rel_operator():
  """
  Determine the relational operator and return it
  """
  match(tokens[next].type)
  return tokens[next - 1].type


def condition():
  """
  Condition --> Expression RelOp Expression
  """
  left_value = expression()
  operator = rel_operator()
  right_value = expression()
  return evaluate_condition(left_value, operator, right_value)


def if_statement():
  """
  IfStatement --> 'if' Condition ':' Block [ElseClause] 'end'
  """

  # Match "if" keyword
  match('IF')

  if (condition()):
    # Match ':'
    match('COLON')

    # Call block statement
    block()

    global next
    depth = 0

    # Skip until you find end
    while next < len(tokens):
      if (check('IF') or check('FOR') or check('WHILE')):
        depth += 1
        next += 1
      elif (check('END') and depth == 0):
        break
      elif (check('END')):
        depth -= 1
        next += 1
      else:
        next += 1

  else:
    while next < len(tokens):
      if (check('END')):
        break
      elif (check('ELSE')):
        else_clause()
      else:
        next += 1

  # Match 'end' keyword
  match('END')


def else_clause():
  """
  ElseClause --> 'else' ':' Block
  """
  if check('ELSE'):
    match('ELSE')
    match('COLON')
    block()


def for_statement():
  """
  ForStatement --> 'for' '(' Name ':=' Expression 'to' Expression ')' Block 'end'
  """

  global next
  # Match the 'for' keyword
  match('FOR')

  # Match the opening parenthesis
  match('LPAREN')

  # Match the name
  name = tokens[next].value
  match('NAME')

  # Match the ':=' operator
  match('ASSIGN')

  # Match the starting expression
  start_value = expression()
  symbols[name] = start_value

  # Match the 'to' keyword
  match('TO')

  # Match the ending expression
  end_value = expression()

  # Match the closing parenthesis
  match('RPAREN')

  # Keep track of starting/end position in the token sequence
  startPos = next

  while (True):
    # Match the block
    block()

    # Increment the index variable
    symbols[name] += 1

    # Check if the index variable is greater than or equal to the ending value
    if symbols[name] > end_value:
      break

    # Reset position back to the starting position
    next = startPos

  # Match the 'end' keyword
  match('END')


def block():
  """
    block --> {Statement}
    """
  global next
  in_block = True

  while in_block and next < len(tokens):
    if check('INPUT'):
      input_statement()
    elif check('NAME'):
      assign_statement()
    elif check('PRINT'):
      print_statement()
    elif check('IF'):
      if_statement()
    elif check('WHILE'):
      while_statement()
    elif check('DO'):
      do_while_statement()
    elif check('FOR'):
      for_statement()
    else:
      in_block = False


def program():
  """
    program --> 'program' Name ':' Block 'end'
    """
  match('PROGRAM')
  match('NAME')
  match('COLON')
  block()
  match('END')


def interpret(source):
  """
    The interpreter main function
    """
  global tokens
  tokens = lexer.analyze(source)
  program()


if __name__ == '__main__':
  # The name of the test file is the first command line argument
  filename = sys.argv[1]

  # Open it and read its contents into a string
  source = open(filename).read()
  print(source)
  print()

  # Interpret the source code
  interpret(source)
