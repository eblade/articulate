Feature: Scoping
  
  Scoping is indentation-based. Variables should be available to
  lower scopes but not the opposite.

  Background: A VM is set up
      Given a VM
  
  Scenario: Integer assignment on three levels
      Given a specific sequence of instructions
         | directive | indentation | target | expression |
         | set       | 0           | level1 | 1          |
         | set       | 1           | level2 | 2          |
         | set       | 2           | level3 | 3          |
         | print     | 2           |        | level1     |
         | print     | 2           |        | level2     |
         | print     | 2           |        | level3     |
         | nop       | 0           |        |            |
       When the instructions are converted to a tree
        And the tree is fed to the VM
       Then the variable "level1" should have the value 1
        And the variable "level2" should be undefined
        And the variable "level3" should be undefined
        And the output from the VM should be 
         """
         1
         2
         3
         """

  Scenario: Local assignement should not remain when leaving scope
      Given a specific sequence of instructions
         | directive | indentation | target | expression |
         | set       | 0           | x      | "outer"    |
         | print     | 0           |        | x          |
         | set       | 1           | x      | "inner"    |
         | print     | 1           |        | x          |
         | print     | 0           |        | x          |
       When the instructions are converted to a tree
        And the tree is fed to the VM
       Then the output from the VM should be 
         """
         outer
         inner
         outer
         """

