import sys
import os
class Tokenizer:

    keywords = ["class", "constructor", "function", "method"
                , "field", "static", "var", "int", "char", "do"
                ,"boolean", "void", "true", "false", "null"
                ,"this", "let", "if", "else", "while", "return"]
    
    symbols = ["{", "}", "[", "]", ".", ",",";", "+", "-", "*",
               "/", "&", "|", "<", ">", "=", "~", "(", ")"]
    
    def __init__(self):
        self.currentToken = ""
        self.lineSeek = 0
        self.lineLen = 0

    def openFile(self, fileName):
        self.file = open(fileName, "r")
        self.__advanceLine()

    def closeFile(self):
        self.file.close()

    def __advanceLine(self):
        self.currentLine = self.file.readline()
        self.advanceMode = 0
        self.lineSeek = 0
        if (self.currentLine == ""):
            return False
        else:
            self.currentLine = self.currentLine.strip()
            self.currentLine = self.currentLine + "\n"
            self.lineLen = len(self.currentLine)
            return True

    def determineMode(self):
        for i in range(self.lineSeek, self.lineLen):
            if (self.currentLine[i] == '\n' or (self.currentLine[i] == "/" and self.currentLine[i+1] == "/")):
                if (self.__advanceLine()):
                    return (True) and (self.determineMode())
                else:
                    return False
            elif (self.currentLine[i].isspace()):
                continue
            else:
                if (self.currentLine[i].isalpha()):
                    self.lineSeek = i
                    self.advanceMode = 1
                elif (self.currentLine[i].isdigit()):
                    self.advanceMode = 2
                    self.lineSeek = i
                else:
                    self.advanceMode = 3
                    self.lineSeek = i
            return True

    def advance(self):
        if (self.determineMode()):
            if (self.advanceMode == 1):
                for i in range (self.lineSeek, self.lineLen):
                    if not (self.currentLine[i].isalpha() or self.currentLine.isdigit()):
                        self.currentToken = self.currentLine[self.lineSeek:i]
                        self.lineSeek = i
                        return True
            elif (self.advanceMode == 2):
                for i in range (self.lineSeek, self.lineLen):
                    if not (self.currentLine[i].isdigit()):
                        self.currentToken = self.currentLine[self.lineSeek:i]
                        self.lineSeek = i
                        return True
            elif (self.advanceMode == 3):
                if (self.currentLine[self.lineSeek] == "/" and self.currentLine[self.lineSeek+1] == "*"):
                    while (self.currentLine.find("*/") == -1):
                        if not (self.__advanceLine()):
                            return False
                    self.lineSeek = self.currentLine.find("*/") + 2
                    return True and self.advance()
                elif self.currentLine[self.lineSeek] == "/" and self.currentLine[self.lineSeek+1] == "/":
                    self.__advanceLine()
                    return True and self.advance()
                elif not (self.currentLine[self.lineSeek] == "\""):
                    self.currentToken = self.currentLine[self.lineSeek:self.lineSeek+1]
                    self.lineSeek += 1
                else:
                    for i in range (self.lineSeek, self.lineLen):
                        if (self.currentLine[i] == "\""):
                            self.currentToken = self.currentLine[self.lineSeek-1:i+1]
                            self.lineSeek = i+1
                return True
        else:
            return False
        
    def tokenType(self):
        if (self.currentToken in self.keywords):
            self.currentTokenType = "keyword"
        elif (self.currentToken in self.symbols):
            self.currentTokenType = "symbol"
        elif (self.currentToken.isnumeric()):
            self.currentTokenType = "integerConstant"
        elif (self.currentToken.isalpha()):
            self.currentTokenType = "identifier"
        elif (self.currentToken[0] == "\"" and self.currentToken[-1] == "\""):
            self.currentTokenType = "stringConstant"
            self.currentToken = self.currentToken[1:len(self.currentToken)-1]


class SymbolTable:
    def __init__(self):
        self.list = list()
        dictionary = dict()
        self.list.append(dictionary)
        self.lenList = 1
     
    def addDict(self):
        dictionary = dict()
        self.list.insert(0, dictionary)
        self.lenList += 1

    def deleteDict(self):
        del self.list[0]
        self.lenList -= 1
        
    def addToDict(self, name, type, kind):
        lenList = len(self.list)
        lenDict = len(self.list[0]) - 1
        # Tuple Format: (type, kind(arg, static), #)
        for x in range(0, lenList):
            listed = list(self.list[x].values())    
            for i in range (lenDict, -1, -1):
                if listed[i][1] == kind:
                    self.list[0][name] = (type, kind, listed[i][2]+1)
                    return
        self.list[0][name] = (type, kind, 0)

    def printDicts(self):
        print(self.list)

    def varCount(self, kind):
        c = 0
        for i in range(0, self.lenList):
            for x in self.listi[i].values():
                if (x[0] == kind):
                    c += 1
        return c
    
    def kindOf(self, name):
        for i in range(0, self.lenList):
            if (self.list[i].get(name)):
                return self.list[i].get(name)[0]
        return "NONE"
    
    def typeOf(self, name):
        for i in range(0, self.lenList):
            if (self.list[i].get(name)):
                return self.list[i].get(name)[1]
        return "NONE"
    
    def indexOf(self, name):
        for i in range(0, self.lenList):
            if (self.list[i].get(name)):
                return self.list[i].get(name)[2]
        return "NONE"



class SyntaxAnalyzer:
    def __init__(self):
        self.token1 = ""
        self.token1Type = ""
        self.currentClass = ""
        self.tokenizer = Tokenizer()
        self.table = SymbolTable()

    def openFile(self ,filePath):
        self.tokenizer.openFile(filePath)
        withoutJack = filePath.find(".")
        path = filePath[0:withoutJack] + ".xml"
        self.file = open(path, "wt")

    def closeFile(self):
        self.tokenizer.closeFile()
        self.file.close()

    def advance(self):
            self.tokenizer.advance()
            self.tokenizer.tokenType()
            self.token1 = self.tokenizer.currentToken
            self.token1Type = self.tokenizer.currentTokenType
            if (self.token1 == "<"):
                self.token1 = "&lt;"
            if (self.token1 == ">"):
                self.token1 = "&gt;"
            if (self.token1 == "&"):
                self.token1 = "&amp;"            
            return True
    
    def compileClass(self, lvl=0):
        self.file.write("<class>\n")
        self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type)) 
        self.advance()
        self.currentClass = self.token1
        self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
        self.advance()
        self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
        self.advance()
        self.compileClassVarDec(lvl+1)
        self.compileSubroutineDec(lvl+1)
        self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
        self.file.write("</class>\n")
        

    def compileClassVarDec(self, lvl):
        typeIdent = ""
        kindIdent = ""
        while (self.token1 in ["field", "static"]):
            kindIdent = self.token1
            self.file.write("{}<classVarDec>\n".format((lvl-1)*"\t"))
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            typeIdent = self.token1
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.table.addToDict(self.token1, typeIdent, kindIdent)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            if (self.token1 == ","):
                while not self.token1 == ";":
                    if self.token1 != ",":
                        self.table.addToDict(self.token1, typeIdent, kindIdent)
                    self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                    self.advance()

            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}</classVarDec>\n".format((lvl-1)*"\t"))


    def compileSubroutineDec(self, lvl):
        subroutineType = ""
        while (self.token1 in ["function", "method", "constructor"]) or (self.token1Type == "identifier"):
            subroutineType = self.token1
            self.file.write("{}<subroutineDec>\n".format((lvl-1)*"\t"))
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.table.addDict()
            if (subroutineType == "method"):
                self.table.addToDict("this", self.currentClass, "argument")
            self.compileParList(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileSubroutineBody(lvl+1)
            # self.advance()
            self.file.write("{}</subroutineDec>\n".format((lvl-1)*"\t"))


    def compileVarDec(self, lvl):
        identType = ""
        while self.token1 == "var":
            self.file.write("{}<varDec>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            identType = self.token1
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            while self.token1 != ";":
                self.table.addToDict(self.token1, identType, "local")
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
                if (self.token1 == ","):
                    self.advance()
            self.advance()
            self.file.write("{}</varDec>\n".format("\t"*(lvl-1)))

    def compileParList(self, lvl):
        identType = ""
        self.file.write("{}<parameterList>\n".format("\t"*(lvl-1)))
        while self.token1 != ")":
            identType = self.token1
            self.advance()
            self.table.addToDict(self.token1, identType, "argument")
            self.advance()
            if (self.token1 == ","):
                self.advance()
        self.file.write("{}</parameterList>\n".format("\t"*(lvl-1)))

    def compileSubroutineBody(self, lvl):
        if self.token1 == "{":
            self.file.write("{}<subroutineBody>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileVarDec(lvl+1)
            self.compileStatements(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.table.printDicts()
            self.table.deleteDict()
            self.file.write("{}</subroutineBody>\n".format("\t"*(lvl-1)))

    def compileStatements(self, lvl):
        self.file.write("{}<statements>\n".format("\t"*(lvl-1)))
        while self.token1 in ["let", "if", "while", "do", "return"]:
            self.compileLet(lvl+1)
            self.compileIf(lvl+1)
            self.compileWhile(lvl+1)
            self.compileReturn(lvl+1)
            self.compileDo(lvl+1)
        # self.advance()
        self.file.write("{}</statements>\n".format("\t"*(lvl-1)))

    def compileLet(self, lvl):
        while self.token1 == "let":
            self.file.write("{}<letStatement>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            if (self.token1 != "="):
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.compileExpression(lvl+1)
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileExpression(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}</letStatement>\n".format("\t"*(lvl-1)))

    def compileWhile(self, lvl):
        while self.token1 == "while":
            self.file.write("{}<whileStatement>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileExpression(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileStatements(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}</whileStatement>\n".format("\t"*(lvl-1)))
                
    def compileReturn(self, lvl):
        if (self.token1 != "return"):
            return
        self.file.write("{}<returnStatement>\n".format("\t"*(lvl-1)))
        self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
        self.advance()
        if (self.token1 == ";"):
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
        else:
            self.compileExpression(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
        self.file.write("{}</returnStatement>\n".format("\t"*(lvl-1)))
        
    def compileDo(self, lvl):
        while self.token1 == "do":
            self.file.write("{}<doStatement>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            if (self.token1 == "."):
                self.advance()
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()


                self.compileExpressionList(lvl+1)
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                # else:
                #     self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            else:
                self.advance()
                self.compileExpressionList(lvl+1)
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}</doStatement>\n".format("\t"*(lvl-1)))

    def compileIf(self, lvl):
        while self.token1 == "if":
            self.file.write("{}<ifStatement>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            if (self.token1 != ")"):
                self.compileExpression(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileStatements(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            if self.token1 == "else":
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.compileStatements(lvl+1)
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
            self.file.write("{}</ifStatement>\n".format("\t"*(lvl-1)))


    def compileExpression(self, lvl):
        self.file.write("{}<expression>\n".format("\t"*(lvl-1)))
        self.compileTerm(lvl+1)
        while self.token1 in ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="]:
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileTerm(lvl+1)
        self.file.write("{}</expression>\n".format("\t"*(lvl-1)))

    def compileTerm(self, lvl):
        self.file.write("{}<term>\n".format("\t"*(lvl-1)))
        if (self.token1 == "("):
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type)) 
            self.advance()
            self.compileExpression(lvl+1)
            if (self.token1 == ")"):
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.file.write("{}</term>\n".format("\t"*(lvl-1)))
                return
        if (self.token1 in ["-", "~"]):
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type)) 
            self.advance()
            self.compileTerm(lvl+1)
            self.file.write("{}</term>\n".format("\t"*(lvl-1)))
            return
        self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
        self.advance()
        if (self.token1 == "["):
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileExpression(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
        if (self.token1 == "."):
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()            
        if (self.token1 == "("):
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileExpressionList(lvl+1)
            self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
            self.advance()
        # if (self.token1 in ["(", "{"]):
        #     self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
        #     self.advance()
        #     self.compileExpression(lvl+1)
        #     self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
        #     self.advance()
        self.file.write("{}</term>\n".format("\t"*(lvl-1)))

    def compileExpressionList(self, lvl):
        self.file.write("{}<expressionList>\n".format("\t"*(lvl-1)))
        while (self.token1 != ")"):
            self.compileExpression(lvl+1)
            if (self.token1 == ","):
                self.file.write("{}<{}> {} </{}>\n".format("\t"*(lvl), self.token1Type, self.token1, self.token1Type))
                self.advance()
        self.file.write("{}</expressionList>\n".format("\t"*(lvl-1)))

def __main__():
    analyzer = SyntaxAnalyzer()
    if (sys.argv[1].find(".jack") != -1):
        analyzer.openFile(sys.argv[1])
        analyzer.advance()
        analyzer.compileClass(1)
        analyzer.closeFile()
    else:
        files = os.listdir(sys.argv[1])
        numberOfFiles = len(files)
        print(files)
        for i in range (0, numberOfFiles):
            if (files[i].find(".jack") != -1):
                analyzer.openFile(sys.argv[1] + "/" +files[i])
                analyzer.advance()
                analyzer.compileClass(1)
                analyzer.closeFile()
        
__main__()