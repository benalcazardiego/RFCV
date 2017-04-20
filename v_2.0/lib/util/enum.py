#Class_creator
def enum(**enums):
    return type('Enum', (), enums)
