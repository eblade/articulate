Feature: Variable substitution and parenthesis matching

  Scenario: Double parenthesis
      Given a VM
        And an expression (x+1) + (x-1)
        And a resolver that returns "1"
       When the expression is substituted
       Then the resolver was called with "x+1"
        And the resolver was called with "x-1"
        And the expression should be 1 + 1

  Scenario: Double nested parenthesis
      Given a VM
        And an expression (x+1 - (x+2)) + ((x * 4))
        And a resolver that returns "1"
       When the expression is substituted
       Then the resolver was called with "x+1"
        And the resolver was called with "x-1"
        And the expression should be 1 + 1

  Scenario: Comlex expression using recursive substitution
      Given a VM
        And the current scope has some variable x = 42
        And an expression (x+1 - (x+3)*(x+2)) + ((x * 4))
        And the normal resolver is used
       When the expression is substituted
       Then the expression should be x+1 - 45*44 + 168
