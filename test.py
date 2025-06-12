import unittest
from interpreter import run, global_environment, Function, Primitive, Environment


class TestInterpreter(unittest.TestCase):
  def test_builtin_sum(self):
    self.assertEqual(run("(+ 5 6)"), 11)
  def test_builtin_dif(self):
    self.assertEqual(run("(- 5 6)"), -1)
  def test_builtin_mult(self):
    self.assertEqual(run("(* 5 6)"), 30)
  def test_builtin_quot(self):
    self.assertAlmostEqual(run("(/ 5 2)"), 2.5)
  def test_builtin_comparison(self):
    self.assertFalse(run("(= 5 6)"))
    self.assertTrue(run("(= 6 6)"))
  def test_assignment_and_primitive_lookup(self):
    run("(set a 17)")
    self.assertEqual(global_environment.lookup('a'), 17)
  def test_string_lookup(self):
    global_environment.add('key', 59)
    self.assertEqual(run("key"), 59)
  def test_procedure_definition(self):
    run("(def cube (num) (* num (* num num)))")
    cube_func = global_environment.lookup("cube")   
    self.assertTrue(isinstance(cube_func, Function))
    self.assertEqual(cube_func.body, ['*', "num", ["*", "num", "num"]])
    self.assertEqual(cube_func.param_list, ["num"])
    self.assertEqual(cube_func.environment, global_environment)

  def test_procedure_call(self):
    run("(def cube (num) (* num (* num num)))")
    self.assertEqual(run("(cube 4)"), 64)

  def test_compound_expressions(self):
    self.assertTrue(run("(begin (set x 6) (set x (+ 57 x)) x)"), 63)

  def test_class_definition(self):
    run("(begin(class Test None (def init (self name) (set (attr self name) name))))")
    self.assertTrue(isinstance(global_environment.lookup("Test"), Primitive) )

  def test_object_instantiation(self):
    run("(begin(class Test None (def init (self name) (set (attr self name) name))) (set a (Test)) ((attr a init)  66) )")
    self.assertTrue(isinstance(global_environment.lookup("a"), Environment))
    self.assertEqual(global_environment.lookup("a").lookup("name"), 66)


if __name__ == '__main__':
    unittest.main()
