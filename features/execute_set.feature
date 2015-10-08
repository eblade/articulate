Feature: Executing the set directive

  The set directive should calculate an expression based on the
  current scope and store the result in the target variable.

  Background: A VM is set up
      Given a VM
  
  # Integer

  Scenario: Integer assignment
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42
       When the instruction is fed to the VM
       Then the variable "x" should have the value 42

  Scenario: Integer addition
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42 + 100
       When the instruction is fed to the VM
       Then the variable "x" should have the value 142

  Scenario: Integer subtraction
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42 - 100
       When the instruction is fed to the VM
       Then the variable "x" should have the value -58

  Scenario: Integer multiplication
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42 * 100
       When the instruction is fed to the VM
       Then the variable "x" should have the value 4200

  Scenario: Integer division
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42 / 7
       When the instruction is fed to the VM
       Then the variable "x" should have the value 6

  Scenario: Integer complex expression
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = (44 + 4) * 11 ** 2
       When the instruction is fed to the VM
       Then the variable "x" should have the value 5808

  # Float

  Scenario: Float assignment
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42.5
       When the instruction is fed to the VM
       Then the variable "x" should have the value 42.5

  Scenario: Float addition
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42.3 + 100
       When the instruction is fed to the VM
       Then the variable "x" should have the value 142.3

  Scenario: Float subtraction
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42.5 - 100
       When the instruction is fed to the VM
       Then the variable "x" should have the value -57.5

  Scenario: Float multiplication
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 45.2 * 100
       When the instruction is fed to the VM
       Then the variable "x" should have the value 4520.0

  Scenario: Float division
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 42.0 / 7
       When the instruction is fed to the VM
       Then the variable "x" should have the value 6.0

  Scenario: Float complex expression
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = (44. + 4.) * 11. ** 2.
       When the instruction is fed to the VM
       Then the variable "x" should have the value 5808.0

  # Strings

  Scenario: String assignment
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = "my string"
       When the instruction is fed to the VM
       Then the variable "x" should have the value "my string"

  Scenario: String concatenation
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = "a" + "b" + "c"
       When the instruction is fed to the VM
       Then the variable "x" should have the value "abc"
  
  # Using variables from the scope

  Scenario: Adding a variable and an integer
      Given the current scope has some variable x = 5
        And a "set" instruction
        And the instruction has an argument target = y
        And the instruction has an argument expression = x + 10
       When the instruction is fed to the VM
       Then the variable "x" should have the value 5
        And the variable "y" should have the value 15

  Scenario: Chained addition using the current scope
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = 1
       When the instruction is fed to the VM
       Then the variable "x" should have the value 1
      Given a "set" instruction
        And the instruction has an argument target = x
        And the instruction has an argument expression = x + 2
       When the instruction is fed to the VM
       Then the variable "x" should have the value 3
