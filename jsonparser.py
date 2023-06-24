class JSONparser:
    def __init__(self, fileName):
        self.__file = fileName
        self.__str = None
        self.__pos = 0
        self.__obj = None
    
    #public methods
    def load(self):
        if self._dataAcquired():
            self._preprocess()
            self._parse()
            print(self.__obj)
            return True
        return False

    def dump(self):
        obj = self._format(self.__obj)
        try:
            with open(self.__file, 'w') as file:
                file.write(obj)
                return True
        except:
            return False

    def addField(self, value, *field):
        if self._isnumber(value):
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        if len(field) == 2:
            if field[0] in self.__obj.keys():
                # self.__obj[field[0]][field[1]] = value
                # return True
                if not isinstance(self.__obj[field[0]], dict):
                    self.__obj[field[0]] = {}
                self.__obj[field[0]][field[1]] = value
                return True
            else: return False
        elif len(field) == 1:
            self.__obj[field[0]] = value
            return True
        else:
            return False

    def updateField(self, value, *field):
        found = False
        if self._isnumber(value):
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        if len(field) == 2:
            if field[0] in self.__obj.keys() and field[1] in self.__obj[field[0]].keys():
                found = True
                self.__obj[field[0]][field[1]] = value
        if len(field) == 1:
            if field[0] in self.__obj.keys():
                found = True
                self.__obj[field[0]] = value
        if not found:
            return False
        return True

    def deleteField(self, *field):
        found = False
        if len(field) == 2:
            if field[0] in self.__obj.keys() and field[1] in self.__obj[field[0]].keys():
                found = True
                del self.__obj[field[0]][field[1]]
        if len(field) == 1:
            if field[0] in self.__obj.keys():
                found = True
                del self.__obj[field[0]]
        if not found:
            return False
        return True
    
    def displayObject(self):
        obj = self._format(self.__obj)
        print(obj)

    #protected helper mehtods
    #helper methods for load
    def _dataAcquired(self):
        try:
            with open(self.__file, 'r') as file:
                return True
        except:
            return False
        
    def _preprocess(self):
        with open(self.__file, 'r') as file:
            readf = file.read()
        readf = readf.replace(' ', '').replace('\n', '').replace('\t', '')
        self.__str = readf

    def _parse(self):
        self.__pos = 0
        if self.__str[0] == '{' and self.__str[-1] == '}':
            self.__obj = self._parseValue()


    def _parseValue(self):
        char = self.__str[self.__pos]
        if char == '{':
            return self._parseObject()
        if char == '"':
            return self._parseString()
        if char.isdigit() or char == '-':
            return self._parseNumber()
        else:
            return False
    
    def _parseObject(self):
        obj = {}
        self.__pos += 1

        while self.__pos < len(self.__str):
            char = self.__str[self.__pos]

            if char == '}':
                self.__pos += 1
                return obj
            elif char == ',':
                self.__pos += 1
            else:
                key = self._parseString()
                if self.__str[self.__pos] != ':':
                    return False
                self.__pos += 1 
                value = self._parseValue()
                obj[key] = value
        return obj

    def _parseString(self):
        self.__pos += 1
        start = end = self.__pos
        valid = False

        while end < len(self.__str) and self.__str[end] != '"':
            valid = True
            self.__pos += 1
            end += 1

        if not valid:
            return

        self.__pos = end + 1
        return self.__str[start:end]
        
    def _parseNumber(self):
        start = end = self.__pos
        valid = False

        while end < len(self.__str) and (self.__str[end].isdigit() or self.__str[end] in ['-', '.']):
            valid = True
            end += 1

        if not valid:
            return
        self.__pos = end
        num = self.__str[start:end]
        if '.' in num:
            return float(num)
        else:
            return int(num)
        
    #helper method for dump
    def _format(self, obj, indent = 0):
        res = '{\n'
        indent += 2

        for key, value in obj.items():
            res += " " * indent + f'"{key}": '
            if isinstance(value, dict):
                res += self._format(value, indent) + ",\n"
            elif isinstance(value, str):
                res += f'"{value}",\n'
            else:
                res += f'{value},\n'

        indent -= 2
        res = res.rstrip(",\n") + "\n"
        res += " " * indent + "}"

        return res

    def _isnumber(self, value):
        isnum = True
        for i in range(len(value)):
            if not (value[i].isdigit() or value[i] in ['-', '.']):
                isnum = False
                break
            return isnum


class JSONParserConsole:
    def __init__(self):
        self.__parser = None

    def getFile(self):
        fileName = input('Welcome! Enter the name of the JSON file you want to work with: ')
        self.__parser = JSONparser(fileName)
        parsed = self.__parser.load()
        if parsed:
            return True
        else:
            return False

    def displayObject(self):
        print('Displaying the contents of JSON object...')
        self.__parser.displayObject()

    def getCommand(self):
        print('\nAvailable commands:')
        print('1. Update a field (usage example -> upd school.name = Academy)')
        print('2. Add a new field (usage example -> add student.name = Anna)')
        print('3. Delete a field (usage example -> del student)')
        command = input('Enter a command from the list of available commands: ')
        validCommand = self.processCommand(command)
        return validCommand
    
    def saveChanges(self):
        saved = self.__parser.dump()
        if saved:
            return True
        else:
            return False

    def processCommand(self, command):
        command = command.strip()
        if command.startswith('upd'):
            parts = command[3:].strip().split('=')
            if len(parts) != 2:
                return False
            fields = parts[0].strip()
            field = []
            try:
                fields = fields.split('.')
                for f in fields:
                    field.append(f)
            except:
                field.append(fields)
            value = parts[1].strip()
            return self.__parser.updateField(value, *field)

        if command.startswith('del'):
            fields = command[3:].strip()
            field = []
            try:
                fields = fields.split('.')
                for f in fields:
                    field.append(f)
            except:
                field.append(fields)
            return self.__parser.deleteField(*field)

        if command.startswith('add'):
            parts = command[3:].strip().split('=')
            if len(parts) != 2:
                return False
            fields = parts[0].strip()
            value = parts[1].strip()
            field = []
            try:
                fields = fields.split('.')
                for f in fields:
                    field.append(f)
            except:
                field.append(fields)
            return self.__parser.addField(value, *field)
        
    def start(self):
        parsed = self.getFile()
        if parsed:
            print('JSON document parsed successfully!')
        else:
            print('Invalid JSON file :(')
            print('Exiting the program')
            return
        
        while True:
            print("\nAvailable actions:")
            print("1. Display object")
            print("2. Make changes")
            print("3. Exit")

            choice = input('Enter the number of the action you want to execute: ')
            if choice == '1':
                self.displayObject()
            elif choice == '2':
                valid = self.getCommand()
                if valid:
                    print('Changes made successfully!')
                else:
                    print('Invalid command. Please try again.')
            elif choice == '3':
                saved = self.saveChanges()
                if saved:
                    print('Object saved successfully!')
                else:
                    print('Failed to save object:(')
                break
            else:
                print('Invalid choice. Please try again.')

if __name__ == '__main__':
    pc = JSONParserConsole()
    pc.start()


