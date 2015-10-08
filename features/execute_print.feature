Feature: Executing the print directive

  The print directive should print what it's given to stdout.
  
  Background: A VM is set up
      Given a VM

  Scenario: Hello World!
      Given a "print" instruction
        And the instruction has an argument expression = "Hello World!"
       When the instruction is fed to the VM
       Then the output from the VM should be 
        """
        Hello World!
        """

  Scenario: Hello World! Twice!
      Given a "print" instruction
        And the instruction has an argument expression = "Hello World!"
       When the instruction is fed to the VM
        And the instruction is fed to the VM
       Then the output from the VM should be 
        """
        Hello World!
        Hello World!
        """

  Scenario: Printing a concatenated string
      Given a "print" instruction
        And the instruction has an argument expression = "Hello " + "World!"
       When the instruction is fed to the VM
       Then the output from the VM should be 
        """
        Hello World!
        """

  Scenario: Printing a concatenated string on two lines
      Given a "print" instruction
        And the instruction has an argument expression = "Hello\n" + "World!"
       When the instruction is fed to the VM
       Then the output from the VM should be 
        """
        Hello
        World!
        """

