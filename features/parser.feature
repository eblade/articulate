Feature: parser

  Scenario: Parsing a "require" line
      Given the line require test
       When the line is parsed
       Then there should be an instruction
        And the directive should be "require"
        And "module" should be test

  Scenario: Parsing a simple "using" line
      Given the line using test
       When the line is parsed
       Then there should be an instruction
        And the directive should be "using"
        And "using" should be test

  Scenario: Parsing a more realistic "using" line
      Given the line using "cool" parametrized scope
       When the line is parsed
       Then there should be an instruction
        And the directive should be "using"
        And "using" should be "cool" parametrized scope

  Scenario: Parsing a simple "define" line
      Given the line define test
       When the line is parsed
       Then there should be an instruction
        And the directive should be "define"
        And "function" should be test

  Scenario: Parsing a more realistic "define" line
      Given the line define epic function (parameter)
       When the line is parsed
       Then there should be an instruction
        And the directive should be "define"
        And "function" should be epic function (parameter)

  Scenario: Parsing a "given" line
      Given the line given
       When the line is parsed
       Then there should be an instruction
        And the directive should be "given"

  Scenario: Parsing a simple "for-in" line
      Given the line for entry in entries
       When the line is parsed
       Then there should be an instruction
        And the directive should be "for-in"
        And "entry" should be entry
        And "list" should be entries

  Scenario: Parsing a "for-in" line with a dot
      Given the line for entry in feed.entries
       When the line is parsed
       Then there should be an instruction
        And the directive should be "for-in"
        And "entry" should be entry
        And "list" should be feed.entries

  Scenario: Parsing a simple "setting" line
      Given the line x = 5
       When the line is parsed
       Then there should be an instruction
        And the directive should be "set"
        And "target" should be x
        And "expression" should be 5

  Scenario: Parsing a complex "setting" line
      Given the line x.y = (5 + (3 - y))/32+2*y
       When the line is parsed
       Then there should be an instruction
        And the directive should be "set"
        And "target" should be x.y
        And "expression" should be (5 + (3 - y))/32+2*y
