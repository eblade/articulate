Feature: Defining and calling functions
  
  A function is defined using the define keyword. That process registers a
  pattern to the scope which can be called. A function has in it's scope
  only access to what's passed into it, e.g. scope is not copied from the
  context where it was created.

  # Function syntax
  #
  # Defining a function:
  # define PATTERN
  # 
  # Calling a function:
  # result = EXPRESSION

  Background: A VM is set up
      Given a VM
  
  Scenario: Defining a simple function
      Given a specific sequence of instructions
         | directive | indentation | function                        | expression |
         | define    | 0           | <x:int> to the power of <y:int> |            |
         | return    | 1           |                                 | x ** y     |
       When the instructions are converted to a tree
        And the tree is fed to the VM
       Then there should be a function called <x:int> to the power of <y:int>

  Scenario: Defining a simple function and calling it with numbers
      Given a specific sequence of instructions
         | directive | indentation | function                        | expression          | target |
         | define    | 0           | <x:int> to the power of <y:int> |                     |        |
         | return    | 1           |                                 | x ** y              |        |
         | set       | 0           |                                 | 2 to the power of 3 | z      |
       When the instructions are converted to a tree
        And the tree is fed to the VM
       Then the variable "z" should have the value 8
        And the variable "x" should be undefined
        And the variable "y" should be undefined

  Scenario: Defining a simple function and calling it with variables
      Given a specific sequence of instructions
         | directive | indentation | function                        | expression              | target |
         | define    | 0           | <x:int> to the power of <y:int> |                         |        |
         | return    | 1           |                                 | x ** y                  |        |
         | set       | 0           |                                 | 4                       | a      |
         | set       | 0           |                                 | 2                       | b      |
         | set       | 0           |                                 | :a to the power of :b   | z      |
       When the instructions are converted to a tree
        And the tree is fed to the VM
       Then the variable "a" should have the value 4
        And the variable "b" should have the value 2
        And the variable "z" should have the value 16
        And the variable "x" should be undefined
        And the variable "y" should be undefined

  Scenario: A recursive fibonacci function
      Given the following code
        """
        define fibonacci number <x:int>
            if x in (1, 2)
                return 1
            return (fibonacci number (x-2)) + (fibonacci number (x-1))

        f1 = fibonacci number 1
        f2 = fibonacci number 2
        f3 = fibonacci number 3
        f4 = fibonacci number 4
        f5 = fibonacci number 5
        """
       When the code is parsed
        And the instructions are converted to a tree
        And the tree is fed to the VM
       Then the variable "f1" should have the value 1
        And the variable "f2" should have the value 1
        And the variable "f3" should have the value 2
        And the variable "f4" should have the value 3
        And the variable "f5" should have the value 5
