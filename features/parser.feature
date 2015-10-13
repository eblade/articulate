Feature: Parsing standard lines
  
  The parser parses "articulate" code into a set of instructions. Each 
  intruction has a directive, which can be seen as the identifier of
  the instruction. Instruction are fairly high-level units and only
  one instruction may come out of one line.

  # These first tests the parser's ability to parse a single line into
  # an instruction.

  Scenario: Parsing an empty line
      Given an empty line
       When the line is parsed
       Then there should not be an instruction

  Scenario: Parsing a "require" line
      Given the line require test
       When the line is parsed
       Then there should be an instruction
        And the directive should be "require"
        And "module" should be test
        And the indentation should be 0

  Scenario: Parsing a simple "using" line
      Given the line using test
       When the line is parsed
       Then there should be an instruction
        And the directive should be "using"
        And "function" should be test
        And the indentation should be 0

  Scenario: Parsing a more realistic "using" line
      Given the line using "cool" parametrized scope
       When the line is parsed
       Then there should be an instruction
        And the directive should be "using"
        And "function" should be "cool" parametrized scope
        And the indentation should be 0

  Scenario: Parsing a simple "define" line
      Given the line define test
       When the line is parsed
       Then there should be an instruction
        And the directive should be "define"
        And "function" should be test
        And the indentation should be 0

  Scenario: Parsing a more realistic "define" line
      Given the line define epic function {parameter}
       When the line is parsed
       Then there should be an instruction
        And the directive should be "define"
        And "function" should be epic function {parameter}
        And the indentation should be 0

  Scenario: Parsing a more realistic "define" line with integer input
      Given the line define epic function {parameter:d}
       When the line is parsed
       Then there should be an instruction
        And the directive should be "define"
        And "function" should be epic function {parameter:d}
        And the indentation should be 0

  Scenario: Parsing a "given" line
      Given the line given
       When the line is parsed
       Then there should be an instruction
        And the directive should be "given"
        And the indentation should be 0

  Scenario: Parsing a simple "for-in" line
      Given the line for entry in entries
       When the line is parsed
       Then there should be an instruction
        And the directive should be "for-in"
        And "entry" should be entry
        And "list" should be entries
        And the indentation should be 0

  Scenario: Parsing a "for-in" line with a dot
      Given the line for entry in feed.entries
       When the line is parsed
       Then there should be an instruction
        And the directive should be "for-in"
        And "entry" should be entry
        And "list" should be feed.entries
        And the indentation should be 0

  Scenario: Parsing a simple "set" line
      Given the line x = 5
       When the line is parsed
       Then there should be an instruction
        And the directive should be "set"
        And "target" should be x
        And "expression" should be 5
        And the indentation should be 0

  Scenario: Parsing a complex "setting" line
      Given the line x.y = (5 + (3 - y))/32+2*y
       When the line is parsed
       Then there should be an instruction
        And the directive should be "set"
        And "target" should be x.y
        And "expression" should be (5 + (3 - y))/32+2*y
        And the indentation should be 0

  Scenario: Parsing a simple "print" line
      Given the line print test
       When the line is parsed
       Then there should be an instruction
        And the directive should be "print"
        And "expression" should be test
        And the indentation should be 0

  Scenario: Parsing a more realistic "print" line
      Given the line print epic expression == 4
       When the line is parsed
       Then there should be an instruction
        And the directive should be "print"
        And "expression" should be epic expression == 4
        And the indentation should be 0

  Scenario: Parsing a simple "if" line
      Given the line if test
       When the line is parsed
       Then there should be an instruction
        And the directive should be "if"
        And "expression" should be test
        And the indentation should be 0

  Scenario: Parsing a more realistic "if" line
      Given the line if (x + 4) > 3
       When the line is parsed
       Then there should be an instruction
        And the directive should be "if"
        And "expression" should be (x + 4) > 3
        And the indentation should be 0

  Scenario Outline: Parsing a line indented with <spaces> spaces
      Given the line <line>
        And <spaces> spaces are prepended
       When the line is parsed
       Then the indentation should be <indentation>
        And the directive should be "<directive>"

       Examples: Well indented lines
           | line                   | spaces | indentation | directive |
           | require test           | 0      | 0           | require   |
           | print "hej"            | 4      | 1           | print     |
           | require http           | 4      | 1           | require   |
           | using a thing with "q" | 8      | 2           | using     |

  Scenario Outline: Parsing a line indented with <spaces> spaces and <tabs> tabs.
      Given the line <line>
        And <tabs> tabs are prepended
        And <spaces> spaces are prepended
       When the line is parsed (expecting trouble)
       Then it raises a SyntaxError with message "<message>"

       Examples: Badly indented lines
           | line                   | spaces | tabs | message                                   |
           | require test           | 1      | 0    | Indentation must be a factor of 4 (was 1).|
           | print "hej"            | 3      | 0    | Indentation must be a factor of 4 (was 3).|
           | require http           | 7      | 0    | Indentation must be a factor of 4 (was 7).|
           | using a thing with "q" | 9      | 0    | Indentation must be a factor of 4 (was 9).|
           | require http           | 0      | 1    | Indentation must only consist of spaces.  |
           | define function <test> | 1      | 1    | Indentation must only consist of spaces.  |
           | define function <test> | 4      | 2    | Indentation must only consist of spaces.  |

  Scenario: A line with scrambled symbols
      Given the line $^*^"%
       When the line is parsed
       Then the directive should be "void"

