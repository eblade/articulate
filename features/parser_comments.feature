Feature: Parse comments

  Comments should be stripped away at an early stage. They consist of things
  including and to the right of hash signs not in strings.

  Scenario: A line starts with a hash
      Given the line # This whole line is a comment
       When the line is parsed
       Then there should not be an instruction
