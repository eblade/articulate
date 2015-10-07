Feature: Parse comments

  Comments should be stripped away at an early stage. They consist of things
  including and to the right of hash signs not in strings.

  Scenario: A line starts with a hash
      Given the line # This whole line is a comment
       When the line is parsed
       Then there should not be an instruction

  Scenario: A line starts with a hash after some indentation
      Given the line # This whole line is a comment
        And 8 spaces are prepended
       When the line is parsed
       Then there should not be an instruction

  Scenario: A line has a comment at the end
      Given the line require http # This is a comment
       When the line is parsed
       Then there should be an instruction
        And the directive should be "require"
        And "module" should be http

  Scenario: A line has a comment with hashes in it
      Given the line require http # This ## is #a comment #with hashes
       When the line is parsed
       Then there should be an instruction
        And the directive should be "require"
        And "module" should be http

