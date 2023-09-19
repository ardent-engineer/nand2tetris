from itertools import count


class Tokenizer:

    keywords = ["class", "constructor", "function", "method"
                , "field", "static", "var", "int", "char", "do"
                ,"boolean", "void", "true", "false", "null"
                ,"this", "let", "if", "else", "while", "return"]
    symbols = ["{", "}", "[", "]", ".", ",",";", "+", "-", "*",
               "/", "&", "|", "<", ">", "=", "~", "(", ")"]
    
    def __advanceLine(self):
        self.currentLine = self.file.readline()
        if (self.currentLine == ""):
            return False
        self.seek = 0
        self.__advanceMode = 0
        self.currentLineLen = len(self.currentLine)
        if (self.currentLineLen == 0):
            self.__advanceLine()
        else:
            self.currentLine = self.currentLine.strip()
            self.currentLineLen = len(self.currentLine)
        return True
    
    def __removeGarbage(self):
        for i in range(self.seek, self.currentLineLen):
            if (self.currentLine[i].isspace()):
                continue
            else:
                self.seek = i
                break    
    def line_count(self,file_path):
        with open(file_path, "r") as f:
            return sum(1 for _ in f)
    def advance(self):
        if (self.__advanceMode == 0):
            for i in range (self.seek, self.currentLineLen):
                if (self.currentLine[i].isspace()):
                    continue
                elif (self.currentLine[i].isalpha() or self.currentLine[i] == '_'):
                    self.seek = i
                    self.__advanceMode = 1
                    self.advance()
                    return
                elif (self.currentLine[i].isdigit()):
                    self.seek = i
                    self.__advanceMode = 2
                    self.advance()
                    return
                else:
                    self.seek = i
                    self.__advanceMode = 3
                    self.advance()
                    return
        elif (self.__advanceMode == 1):
            for i in range (self.seek, self.currentLineLen):
                if not (self.currentLine[i].isalpha() or self.currentLine[i] == '_' or self.currentLine[i].isdigit()):
                    self.__advanceMode = 0
                    self.currentToken = self.currentLine[self.seek:i]
                    self.seek = i
                    return
                if i >= self.currentLineLen-1:
                    self.currentToken = self.currentLine[self.seek:self.currentLineLen]
                    self.__advanceLine()
                    self.__advanceMode = 0
                    # self.advance()
                    return
        elif (self.__advanceMode == 2):
            for i in range (self.seek, self.currentLineLen):
                if not self.currentLine[i].isdigit():
                    self.__advanceMode = 0
                    self.currentToken = self.currentLine[self.seek:i]
                    self.seek = i
                    return
                elif i >= self.currentLineLen-1 and self.currentLine[i].isdigit():
                    self.currentToken = self.currentLine[self.seek:self.currentLineLen]
                    self.__advanceLine()
                    self.__advanceMode = 0
                    # self.advance()
                    return
        elif (self.__advanceMode == 3):
            if (self.currentLine[self.seek] == "\""):
                self.__handleStringConstant()
                return
            self.currentToken = self.currentLine[self.seek:self.seek+1]
            self.seek += 1
            self.__advanceMode = 0
            if (self.seek == self.currentLineLen):
                self.__advanceLine()
                return

    def __handleStringConstant(self):
        self.seek += 1
        for i in range (self.seek, self.currentLineLen):
            if (self.currentLine[i] == "\""):
                self.currentToken = self.currentLine[self.seek:i]
                self.seek = i+1
                if (self.seek >= self.currentLineLen):
                    self.__advanceLine()
                self.__advanceMode = 0
                return
            
            

    def __init__(self):
        self.lineCount = self.line_count("code.txt")
        self.file = open("code.txt", "r")
        self.__advanceLine()
        self.currentToken = ""

    def __del__(self):
        self.file.close()

    def getad(self):
        return self.__advanceMode
    
    def determineType(self):
        if (self.currentToken in self.keywords):
            self.tokenType = "keyword"
        elif (self.currentToken in self.symbols):
            self.tokenType = "symbol"
        elif (self.currentToken.isnumeric()):
            self.tokenType = "integerConstant"
        elif (self.currentToken.isalpha()):
            self.currentToken = "identifier"
        elif (self.currentToken[0] == "\"" and self.currentToken[-1] == "\""):
            self.currentToken = "stringConstant"
    
    

def __main__():
    obj = Tokenizer()
    obj.advance()
    print(obj.currentToken)
    obj.advance()
    print(obj.currentToken)
    obj.advance()
    print(obj.currentToken)
    obj.advance()
    print(obj.currentToken)
    obj.advance()
    print(obj.currentToken)
    obj.advance()
    print(obj.currentToken)
    obj.advance()
    print(obj.currentToken)
    obj.advance()
    print(obj.currentToken)
    obj.advance()
    print(obj.currentToken)









__main__()

        
    

