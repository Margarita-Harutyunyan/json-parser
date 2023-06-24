import jsongenerator
import jsonparser
import random

class JSONtester:
    def __init__(self, file, keys):
        self.__parser = jsonparser.JSONparser(file)
        self.__keys = keys

    def runAllTests(self):
        self.loadTest()
        self.addFieldTest()
        self.updateFieldTest()
        self.deleteFieldTest()
        self.dumpTest()

    def loadTest(self):
        if self.__parser.load() == True:
            print('Test load passed')
        else:
            print('Test load failed')

    def dumpTest(self):
        if self.__parser.dump() == True:
            print('Test dump passed')
        else:
            print('Test dump failed')

    def addFieldTest(self):
        # Case 1 - True
        i = random.randint(0, len(self.__keys) - 1)
        newField = 'newField'
        fields = (self.__keys[i], newField)
        value = 'newValue'
        if self.__parser.addField(value, *fields) == True:
            print(f'Test addField for {self.__keys[i]}.{newField} = {value} passed')
        else:
            print(f'Test addField for {self.__keys[i]}.{newField} = {value} failed')

        # Case 2 - False
        wrongField = 'wrongField'
        fields = (wrongField, newField)
        if self.__parser.addField(value, *fields) == False:
            print(f'Test addField for {self.__keys[i]}.{wrongField} = {value} passed')
        else:
            print(f'Test addField for {self.__keys[i]}.{wrongField} = {value} failed')            

    def updateFieldTest(self):
        # Case 1 - True
        i = random.randint(0, len(self.__keys) - 1)
        field = self.__keys[i]
        value = 'newValue'
        if self.__parser.updateField(value, field) == True:
            print(f'Test updateField for {field} = {value} passed')
        else:
            print(f'Test updateField for {field} = {value} failed')

        #Case 2 - False
        field = 'wrongField'
        if self.__parser.updateField(value, field) == False:
            print(f'Test updateField for {field} = {value} passed')
        else:
            print(f'Test updateField for {field} = {value} failed')      

    def deleteFieldTest(self):
        # Case 1 - True
        i = random.randint(0, len(self.__keys) - 1)
        field = self.__keys[i]
        if self.__parser.deleteField(field) == True:
            print(f'Test deleteField for {field} passed')
        else:
            print(f'Test deleteField for {field} failed')

        # Case 2 - False
        field = 'wrongField'
        if self.__parser.deleteField(field) == False:
            print(f'Test deleteField for {field} passed')
        else:
            print(f'Test deleteField for {field} failed')


def run():
    fileName = input('Enter a random word: ').strip() + '.txt'
    keys = jsongenerator.generateRandomJsonFile(fileName)
    tester = JSONtester(fileName, keys)
    tester.runAllTests()

