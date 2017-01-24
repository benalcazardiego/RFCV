#Current_and_voltage_random_ID_generator
from CurrentVoltage import CurrentVoltage
import random
import string

def random_id(current_voltage):
#Returns something like V-y65N if current_voltage equals 1 and like I-ij15 if current_voltage equals 0
        idf = ''.join(random.choice(string.lowercase + string.uppercase + "1234567890") for i in range(4))
        if current_voltage == CurrentVoltage.VOLTAGE:
            return "V-" + idf

        if current_voltage == CurrentVoltage.CURRENT:
            return "I-" + idf
