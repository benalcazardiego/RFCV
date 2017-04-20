from CommandExecutor import CommandExecutor

class MockExecutor(CommandExecutor):
    def __init__(self, ip, port=2049, expect_reply=False):
        print "U R in MockExecutor - __init__" # Flag 4 debug
        
        pass

    def execute_command(self, command):
        print command
