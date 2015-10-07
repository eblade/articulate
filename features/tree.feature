Feature: tree

  The syntax tree should be able to take a sequence of instructions
  and build structure based on scoping.

  Scenario: A set of 0-indented instruction should create a flat tree.
      Given a specific sequence of instructions
         | directive | indentation | module    |
         | require   | 0           | http      |
         | require   | 0           | test      |
         | require   | 0           | something |
       When the instructions are converted to a tree
       Then the tree should have 3 root instructions

  Scenario: A simple 2-instruction tree
      Given a specific sequence of instructions
         | directive | indentation | using     |
         | using     | 0           | test1     |
         | using     | 1           | test1.1   |
       When the instructions are converted to a tree
       Then the tree should have 1 root instruction

  Scenario: A more complex 5-instruction tree
      Given a specific sequence of instructions
         | directive | indentation | using     |
         | using     | 0           | test1     |
         | using     | 1           | test1.1   |
         | using     | 2           | test1.1.1 |
         | using     | 0           | test2     |
         | using     | 1           | test2.1   |
       When the instructions are converted to a tree
       Then the tree should have 2 root instructions
       Then the tree should look like this
       """
       <Instruction behave +1 using>
       .<Instruction behave +2 using>
       ..<Instruction behave +3 using>
       <Instruction behave +4 using>
       .<Instruction behave +5 using>
       """

  Scenario: A more complex 10-instruction tree
      Given a specific sequence of instructions
         | directive | indentation | using     |
         | using     | 0           | test1     |
         | using     | 1           | test1.1   |
         | using     | 2           | test1.1.1 |
         | using     | 2           | test1.1.2 |
         | using     | 2           | test1.1.3 |
         | using     | 0           | test2     |
         | using     | 1           | test2.1   |
         | using     | 2           | test2.1.1 |
         | using     | 1           | test2.2   |
         | using     | 1           | test2.3   |
       When the instructions are converted to a tree
       Then the tree should have 2 root instructions
       Then the tree should look like this
       """
       <Instruction behave +1 using>
       .<Instruction behave +2 using>
       ..<Instruction behave +3 using>
       ..<Instruction behave +4 using>
       ..<Instruction behave +5 using>
       <Instruction behave +6 using>
       .<Instruction behave +7 using>
       ..<Instruction behave +8 using>
       .<Instruction behave +9 using>
       .<Instruction behave +10 using>
       """

  Scenario: A badly indented instruction tree 1
      Given a specific sequence of instructions
         | directive | indentation | using     |
         | using     | 0           | test1     |
         | using     | 2           | test1.1.1 |
       When the instructions are converted to a tree (expecting trouble)
       Then it raises a SyntaxError with message "Bad indentation transition (0 -> 2)."

  Scenario: A badly indented instruction tree 2
      Given a specific sequence of instructions
         | directive | indentation | using       |
         | using     | 0           | test1       |
         | using     | 1           | test1.1     |
         | using     | 3           | test1.1.1.1 |
       When the instructions are converted to a tree (expecting trouble)
       Then it raises a SyntaxError with message "Bad indentation transition (1 -> 3)."
