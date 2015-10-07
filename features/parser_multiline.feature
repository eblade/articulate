Feature: Parsing multi-line code
  
  The parser should handle a multi-line string with various kinds of code-lines.
  It should be able to parse them one and one and create a sequence of 
  instructions out of that.

  Scenario: A set of require instructions
      Given the following code
        """
        require http
        require test
        require something
        """
       When the code is parsed
       Then the instruction should be the following
         | lineno | directive | indentation | module    |
         | 1      | require   | 0           | http      |
         | 2      | require   | 0           | test      |
         | 3      | require   | 0           | something |

  Scenario: A set of require instruction with empty lines in between
      Given the following code
        """
        
        require http

        require test



        require something
        """
       When the code is parsed
       Then the instruction should be the following
         | lineno | directive | indentation | module    |
         | 2      | require   | 0           | http      |
         | 4      | require   | 0           | test      |
         | 8      | require   | 0           | something |

  Scenario: Nested using instructions
      Given the following code
        """
        using a thing
            using another thing
                using a third thing
        """
       When the code is parsed
       Then the instruction should be the following
         | lineno | directive | indentation | using         |
         | 1      | using     | 0           | a thing       |
         | 2      | using     | 1           | another thing |
         | 3      | using     | 2           | a third thing |
