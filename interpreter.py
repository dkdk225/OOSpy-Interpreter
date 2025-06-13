def tokenize(string):
  # if "(" create a new array and track the array
  # if ")" go to parent array
  # if " " add the current token to token list and continue
  # if anything else: add it to token string

  # if there's a token add it to given list
  # return value is to be the new value of a token
  # if there was a token: which means it's lengt is greater than 0 we would reset it
  # if there was no token it doesn't matter if we reset it or not
  def add_token(token, list):
    if len(token) > 0:
      list.append(format_token(token))
    return ""
  # Check if a token is a number
  def format_token(token):
    # check if the first character is a number.
    # if the first character is a digit the token must be a number otherwise it's illegal and I assume that the user doesn't make mistakes (lol)
    if token[0].isdigit():
      if "." in token: #if token is a number and if it contains a "." then it must be a floating point
        return float(token)
      else:
        return int(token)
    else:
      return token

  token_list = []
  parent_list = []
  token = ""
  current = token_list

  for char in string:
    if char == " ":
      token = add_token(token, current)
    elif char == "(":
      token = add_token(token, current)
      parent_list.append(current)
      current = []
    elif char == ")":
      token = add_token(token, current)
      parent = parent_list.pop()
      parent.append(current)
      current = parent
    else:
      token = token+char
  add_token(token, current)
  return token_list[0] #token list is a wrapper so it contains a single element which is the list of tokens

# print(tokenize("(+ 7 6)"))
# print(tokenize("(+ 7 (* 6 number))"))
# print(tokenize("(+ 7 (* 6 (/ number 6.9)))"))

class Environment:
  def __init__(self, binding,  parent):
    self.binding = binding
    self.parent = parent
  def add(self, key, value):
    self.binding[key] = value
  def lookup(self, key):
    if key in self.binding:
      return self.binding[key]
    elif not self.parent == None:
      return self.parent.lookup(key)
    else:
      raise NameError("Attribute " + key + " doesn't exist in environment chain")
  #This funciton allows Environment to be able to viewed via print() funcitons which are used for debugging the program
  #Later on it is planned to be used in order to view program environment at each step if it's required
  def __str__(self):
    return self.binding.__str__()
      

class Function:
  def __init__(self, param_list, body, environment):
    self.param_list = param_list
    self.body = body
    self.environment = environment

class Primitive():
  tags = []
  def __init__(self, tag, body):
    self.tags.append(tag)
    self.body = body

  
def lhsEval(lhs, env):
  if isinstance(lhs, list):
    (tag, obj_name, attr_name) = lhs
    return (spyEval(obj_name, env), attr_name)
  else:
    return (env, lhs)


#in spy function body and "if" statement branches are expected to be a single expression
def spyEval(form, env):
  if isinstance(form, int) or isinstance(form, float):
    return form
  elif isinstance(form ,str):
    return env.lookup(form)
  elif form[0] == "begin": #compound expression
    tag = form.pop(0)
    val = None
    for exp in form:
      val = spyEval(exp, env)
    return val
  elif form[0] == "set": #attribute assignment
    (tag, lhs, rhs) = form
    (target_env, name) = lhsEval (lhs, env)
    target_env.add(name, spyEval(rhs, env))
  elif form[0] == "def": #function declaration
    (tag, name, params, body) = form
    env.add(name, Function(params, body, env))
  elif form[0] == "if": #if statement
    (tag, condition, ifBody, elseBody) = form
    if spyEval(condition, env):
      return spyEval(ifBody, env)
    else:
      return spyEval(elseBody, env)
  elif form[0] == "attr":
    (tag, obj, attr) = form
    return spyEval(obj, env).lookup(attr)
  # (class [name] [super] ([class_body]))
  # Example:::
  # (class [name] [super] (def [name] ([param1], [param2], ...)(begin [expression list])))
  elif form[0] == "class":
    (tag, name, super, body) = form
    if super == "None":
      super = global_environment
    classEnv = Environment({}, super)
    env.add(name, Primitive(name, lambda: Environment({}, classEnv)))
    spyEval(body, classEnv)
  elif form[0] in Primitive.tags:
    tag = form.pop(0)
    f = spyEval(tag, env).body
    evaluated_args = []
    for arg in form:
      evaluated_args.append(spyEval(arg, env))
    return f(*evaluated_args)
  elif isinstance(form, list): #function call
    name = form.pop(0)
    param_list = form
    #----------Checks if the environment that the procedure was declared on is an instance-------------
    #------------if so adds the instance as first argument to parameter list
    if isinstance(name, list):
      param_list.insert(0, name[1])
    #----------------------


    f = spyEval(name, env) # f is the function that was saved in environment
    #evaluate function parameters at call environment then assign these parameters at function environment
    function_environment = Environment({}, f.environment)
    for i in range(0 ,len(param_list)):
      function_environment.add(f.param_list[i], spyEval(param_list[i], env))
    return spyEval(f.body, function_environment)
  else:
    raise SyntaxError("illegal expression: "+ str(form))

builtin_sum = Primitive("+", lambda x,y:x+y)
builtin_dif = Primitive("-", lambda x,y:x-y)
builtin_mult = Primitive("*", lambda x,y:x*y)
builtin_quot = Primitive("/", lambda x,y:x/y)
builtin_comparison = Primitive("=", lambda x,y:x==y)

global_environment = Environment({
  "+":builtin_sum,
  "-":builtin_dif,
  "*":builtin_mult,
  "/":builtin_quot,
  "=":builtin_comparison
  }, None)



def run(string):
  tokenized = tokenize(string)
  return spyEval(tokenized, global_environment)



# run("(set num 6)")
# print(run("(begin (set num 70) (+ 6 (- 80 (* num 2))))"))
# print(run("(begin (def add (x y) (+ x y)) (add 6 7))"))
# print("run: ", run("(begin(class Test None (def init (self name) (set (attr self name) name))) (set a (Test)) ((attr a init) a 66) (attr a name) )"))
# print("run: ", run("(begin(class Test None (def init (self name) (set (attr self name) name))) (set a (Test)) ((attr a init)  66) (attr a name) )"))


# print("+++++++++++++++++++++++++")
# print(global_environment)
# print("+++++++++++++++++++++++++")
# print(global_environment.binding['Test'])

def main():
  import sys

  def shell():
    while True:
      exp = input(">>>")
      if exp == "env":
        print(global_environment)
      elif exp == "exit":
        break
      else:
        print(run(exp))
    
  def file_program():
    path = sys.argv[1]
    with open(path, 'r') as file:
      content = file.read()
    print(run(content))
    
  if len(sys.argv) > 1:
    file_program()
  elif len(sys.argv) < 2:
    shell()
  else:
    raise TypeError("Wrong number of arguments")


  
if __name__ == '__main__':
  main()