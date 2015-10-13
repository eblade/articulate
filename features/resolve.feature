Feature: Expression resolver of the VM

  Background: A VM is set up
      Given a VM

  Scenario: Resolving a simple python expression
      Given an expression 1 + 4 ** 3
       When the expression is resolved
       Then the result should have the value 65
        And the result should be an integer
       
  Scenario: Resolving a simple python boolean expression (True)
      Given an expression 1 == 5 - 4
       When the expression is resolved
       Then the result should have the value True
        And the result should be a boolean
       
  Scenario: Resolving a simple python boolean expression (False)
      Given an expression 1 == 5 - 5
       When the expression is resolved
       Then the result should have the value False
        And the result should be a boolean
       
  Scenario: Resolving a function with an explicit number
      Given the following code
        """
        define my function of <int:x>
            return 3 * x

        y = 7
        """
        And an expression my function of 5
       When the code is parsed
        And the instructions are converted to a tree
        And the tree is fed to the VM
        And the expression is resolved
       Then the result should have the value 15
        And the result should be an integer
       
  Scenario: Resolving a function with an implicit number
      Given the following code
        """
        define my function of <int:x>
            return 3 * x

        y = 7
        """
        And an expression my function of :y
       When the code is parsed
        And the instructions are converted to a tree
        And the tree is fed to the VM
        And the expression is resolved
       Then the result should have the value 21
        And the result should be an integer
       
  Scenario: Resolving a function with with a call to itself as argument
      Given the following code
        """
        define my function of <int:x>
            return 3 * x

        y = 7
        """
        And an expression my function of (my function of :y)
       When the code is parsed
        And the instructions are converted to a tree
        And the tree is fed to the VM
        And the expression is resolved
       Then the result should have the value 63
        And the result should be an integer
       
