Feature: The using directive

  Background: A VM is set up
      Given a VM

  Scenario: Using and scopes
      Given the following code
        """
        x = 3

        define a place where x is ten times <x:int>
            x = x * 10
            y = x * 1000
            expose x, y

        x = 10

        using a place where x is ten times 5
            print x
            print y

        print x
        """
       When the code is parsed
        And the instructions are converted to a tree
        And the tree is fed to the VM
       Then the output from the VM should be 
        """
        50
        50000
        10
        """
