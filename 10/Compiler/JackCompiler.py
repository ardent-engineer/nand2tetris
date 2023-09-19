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
        # Tuple Format: (type, kind(arg, static), #)
        for x in range(0, lenList):
            listed = list(self.list[x].values())
            lenDict = len(self.list[x]) - 1
            for i in range (lenDict, -1, -1):
                y = listed[0][i] == kind
                if listed[i][1] == kind:
                    self.list[0][name] = (type, kind, listed[i][2]+1)
                    return
        self.list[0][name] = (type, kind, 0)


    def printDicts(self):
        print(self.list)

    def varCount(self, kind):
        c = 0
        for i in range(0, self.lenList):
            for x in self.list[i].values():
                if (x[1] == kind):
                    c += 1
        return c
    
    def kindOf(self, name):
        for i in range(0, self.lenList):
            if (self.list[i].get(name)):
                return self.list[i].get(name)[1]
        return "NONE"
    
    def typeOf(self, name):
        for i in range(0, self.lenList):
            if (self.list[i].get(name)):
                return self.list[i].get(name)[0]
        return "NONE"
    
    def indexOf(self, name):
        for i in range(0, self.lenList):
            if (self.list[i].get(name)):
                return self.list[i].get(name)[2]
        return "NONE"

class VmWriter:

    def openFile(self ,filePath):
        self.file = open(filePath, "wt")

    def closeFile(self):
        self.file.close()

    def writePush(self ,segment, index):
        self.file.write("push {} {}\n".format(segment, index))

    def writePop(self ,segment, index):
        self.file.write("pop {} {}\n".format(segment, index))

    def writeArthmetic(self, op):
        if (op == "+"):
            self.file.write("add\n")
        elif (op == "-"):
            self.file.write("sub\n")
        elif (op == "/"):
            self.file.write("call Math.divide 2\n")
        elif (op == "*"):
            self.file.write("call Math.multiply 2\n")
        elif (op == "neg"):
            self.file.write(op + "\n")
        elif (op == "="):
            self.file.write("eq\n")
        elif (op == ">"):
            self.file.write("gt\n")
        elif (op == "<"):
            self.file.write("lt\n")
        elif (op == "&"):
            self.file.write("and\n")
        elif (op == "|"):
            self.file.write("or\n")
        elif (op == "~"):
            self.file.write("not\n")

    def writeLabel(self, label):
        self.file.write("label {}\n".format(label))

    def writeGoto(self, label):
        self.file.write("goto {}\n".format(label))

    def writeIfGoto(self, label):
        self.file.write("if-goto {}\n".format(label))

    def writeCall(self, functionName, nArgs):
        self.file.write("call {} {}\n".format(functionName, nArgs))

    def writeFunction(self, functionName, nLcls):
        self.file.write("function {} {}\n".format(functionName, nLcls))

    def writeAnything(self, command):
        self.file.write(command)

    def writeReturn(self):
        self.file.write("return\n")

class Counter:
    def __init__(self):
        self.count0 = -1
        self.count1 = -1
    def incrementIf(self):
        self.count0 += 1
    def incrementWhile(self):
        self.count1 += 1
    def reset(self):
        self.count0 = -1
        self.count1 = -1

class SyntaxAnalyzer:
    def __init__(self):
        self.token1 = ""
        self.token1Type = ""
        self.currentClass = ""
        self.currentSubIsConstructor = False
        self.currentSub = ""
        self.currentSubType = ""
        self.objOperate = False
        self.tokenizer = Tokenizer()
        self.table = SymbolTable()
        self.writer = VmWriter()
        self.counter = Counter()

    def openFile(self ,filePath):
        self.tokenizer.openFile(filePath)
        withoutJack = filePath.find(".")
        path = filePath[0:withoutJack] + ".vm"
        self.file = open("xyz.txt", "wt")
        self.writer.openFile(path)

    def closeFile(self):
        self.tokenizer.closeFile()
        self.writer.closeFile()

    def advance(self):
            self.tokenizer.advance()
            self.tokenizer.tokenType()
            self.token1 = self.tokenizer.currentToken
            self.token1Type = self.tokenizer.currentTokenType
            if self.token1 == "false":
                self.token1 = "0"         
                self.token1Type = "integerConstant"
            elif self.token1 == "null":
                self.token1 = "0"
                self.token1Type = "integerConstant"
            return True
    
    def compileClass(self):
        lvl = 1
        self.file.write("<class>\n")
        self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type)) 
        self.advance()
        self.currentClass = self.token1
        self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
        self.advance()
        self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
        self.advance()
        self.compileClassVarDec()
        self.compileSubroutineDec()
        self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
        self.file.write("</class>\n")
        

    def compileClassVarDec(self):
        typeIdent = ""
        kindIdent = ""
        lvl = 1
        while (self.token1 in ["field", "static"]):
            kindIdent = self.token1
            self.file.write("{}<classVarDec>\n".format((lvl-1)*"\t"))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            typeIdent = self.token1
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.table.addToDict(self.token1, typeIdent, kindIdent)
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            if (self.token1 == ","):
                while not self.token1 == ";":
                    if self.token1 != ",":
                        self.table.addToDict(self.token1, typeIdent, kindIdent)
                    self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
                    self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}</classVarDec>\n".format((lvl-1)*"\t"))


    def compileSubroutineDec(self):
        lvl = 1
        subroutineType = ""
        while (self.token1 in ["function", "method", "constructor"]) or (self.token1Type == "identifier"):
            self.counter.reset()
            subroutineType = self.token1
            self.currentSubType = self.token1
            self.currentSubIsConstructor = self.token1 == "constructor"
            self.objOperate = subroutineType in ["method", "constructor"]
            self.file.write("{}<subroutineDec>\n".format((lvl-1)*"\t"))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.currentSub = self.token1
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.table.addDict()
            if (subroutineType == "method"):
                self.table.addToDict("this", self.currentClass, "argument")
            self.compileParList()
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileSubroutineBody()
            self.objOperate = False
            self.currentSubIsConstructor = False
            self.file.write("{}</subroutineDec>\n".format((lvl-1)*"\t"))


    def compileVarDec(self):
        lvl = 1
        identType = ""
        while self.token1 == "var":
            self.file.write("{}<varDec>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            identType = self.token1
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            while self.token1 != ";":
                self.table.addToDict(self.token1, identType, "local")
                self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
                self.advance()
                if (self.token1 == ","):
                    self.advance()
            self.advance()
            if (self.token1 != "var"):
                self.writer.writeFunction(self.currentClass+"."+self.currentSub, self.table.varCount("local"))
                if self.currentSubIsConstructor:
                    self.writer.writePush("constant", self.table.varCount("field"))
                    self.writer.writeCall("Memory.alloc", 1)
            self.file.write("{}</varDec>\n".format("\t"*(lvl-1)))

    def compileParList(self):
        lvl = 1
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

    def compileSubroutineBody(self):
        lvl = 1
        if self.token1 == "{":
            self.file.write("{}<subroutineBody>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            if (self.token1 == "var"):
                self.compileVarDec()
            else:
                self.writer.writeFunction(self.currentClass+"."+self.currentSub, 0)
                if self.currentSubIsConstructor:
                    self.writer.writePush("constant", self.table.varCount("field"))
                    self.writer.writeCall("Memory.alloc", 1)
            if self.currentSubType == "method":
                self.writer.writePush("argument", 0)
            if self.currentSubType in ["method", "constructor"]:
                self.writer.writePop("pointer", 0)
            self.compileStatements()
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.table.printDicts()
            self.table.deleteDict()
            self.file.write("{}</subroutineBody>\n".format("\t"*(lvl-1)))

    def compileStatements(self):
        lvl = 1
        self.file.write("{}<statements>\n".format("\t"*(lvl-1)))
        while self.token1 in ["let", "if", "while", "do", "return"]:
            self.compileLet()
            self.compileIf()
            self.compileWhile()
            self.compileReturn()
            self.compileDo()
        # self.advance()
        self.file.write("{}</statements>\n".format("\t"*(lvl-1)))

    def compileLet(self):
        lvl = 1
        ident = ""
        while self.token1 == "let":
            self.file.write("{}<letStatement>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            ident = self.token1
            kindOf = self.table.kindOf(ident)
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            if (self.token1 != "="):
                self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.compileExpression()
                self.writer.writePush("this" if kindOf == "field" else kindOf, self.table.indexOf(ident))
                self.writer.writeArthmetic("+")
                self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.compileExpression()
                self.advance()
                self.writer.writePop("temp", 0)
                self.writer.writePop("pointer", 1)
                self.writer.writePush("temp", 0)
                self.writer.writePop("that", 0)
                return
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileExpression()
            self.advance()
            self.writer.writePop("this" if kindOf == "field" else kindOf, self.table.indexOf(ident))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.file.write("{}</letStatement>\n".format("\t"*(lvl-1)))

    def compileWhile(self):
        lvl = 1
        while self.token1 == "while":
            self.counter.incrementWhile()
            saved_count = self.counter.count1
            self.writer.writeLabel("WHILE_EXP"+str(saved_count))
            self.file.write("{}<whileStatement>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.compileExpression()
            self.writer.writeAnything("not\n")
            self.writer.writeIfGoto("WHILE_END"+str(saved_count))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.compileStatements()
            self.writer.writeGoto("WHILE_EXP"+str(saved_count))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.writer.writeLabel("WHILE_END"+str(saved_count))
            self.file.write("{}</whileStatement>\n".format("\t"*(lvl-1)))
                
    def compileReturn(self):
        lvl = 1
        if (self.token1 != "return"):
            return
        else:
            self.advance()
            if(self.token1 == ";"):
                self.writer.writePush("constant", 0)
            self.compileExpression()
            self.advance()
            self.writer.writeReturn()
            return

    def compileDo(self):
        lvl = 1
        while self.token1 == "do":
            self.file.write("{}<doStatement>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            print(self.token1)
            self.compileExpression()
            print("\t\t"+self.token1)
            self.advance()
            self.writer.writePop("temp", 0)
            print("\t\t"+self.token1)

    def compileIf(self):
        lvl = 1
        while self.token1 == "if":
            self.counter.incrementIf()
            self.file.write("{}<ifStatement>\n".format("\t"*(lvl-1)))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            saved_count = self.counter.count0
            if (self.token1 != ")"):
                self.compileExpression()
                self.writer.writeIfGoto("IF_TRUE"+str(saved_count))
                self.writer.writeGoto("IF_FALSE"+str(saved_count))
                print("\n"+self.token1+"\n")
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            self.writer.writeLabel("IF_TRUE"+str(saved_count))
            self.compileStatements()
            self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
            self.advance()
            if self.token1 == "else":
                self.writer.writeGoto("IF_END" + str(saved_count))
                self.writer.writeLabel("IF_FALSE" + str(saved_count))
                self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
                self.advance()
                self.compileStatements()
                self.writer.writeLabel("IF_END" + str(saved_count))
                self.file.write("{}<{}> {} </{}>\n".format("\t", self.token1Type, self.token1, self.token1Type))
                self.advance()
            else:
                self.writer.writeLabel("IF_FALSE" + str(saved_count))
            self.file.write("{}</ifStatement>\n".format("\t"*(lvl-1)))


    def compileExpression(self):
        if (self.token1Type == "integerConstant"):
            self.writer.writePush("constant", self.token1)
            self.advance()
            self.compileExpression()
            return
        if (self.token1Type == "stringConstant"):
            self.writer.writePush("constant", len(self.token1))
            self.writer.writeCall("String.new", 1)
            for ch in self.token1:
                if (self.token1 == "\""):
                    continue
                else:
                    self.writer.writePush("constant", ord(ch))
                    self.writer.writeCall("String.appendChar", 2)
            self.advance()
            self.compileExpression()
            return
        elif (self.token1 == "true"):
            self.writer.writePush("constant", 0)
            self.writer.writeAnything("not\n")
            self.advance()
            self.compileExpression()
        elif self.token1 == "this":
            self.writer.writePush("pointer", "0")
            self.advance()
            self.compileExpression()
            return
        elif (self.token1Type == "identifier"):
            var = self.token1
            varKind = self.table.kindOf(var)
            self.advance()
            if not (self.token1 in [".", "(", "["]):
                self.writer.writePush("this" if varKind == "field" else varKind, self.table.indexOf(var))
            elif self.token1 == ".":
                if (self.table.kindOf(var) == "NONE"):
                    self.advance()
                    fName = self.token1
                    self.advance()
                    self.advance()
                    nArgs = self.compileExpressionList()
                    self.writer.writeCall(var+"."+fName, nArgs)
                else:
                    self.advance()
                    fName = self.token1
                    self.advance()
                    self.advance()
                    self.writer.writePush("this" if varKind == "field" else varKind, self.table.indexOf(var))
                    nArgs = self.compileExpressionList() + 1
                    self.writer.writeCall(self.table.typeOf(var)+"."+fName, nArgs)
            elif self.token1 == "(":
                    self.advance()
                    nArgs = self.compileExpressionList()
                    self.writer.writePush("pointer", "0")
                    self.writer.writeCall(self.currentClass+"."+var, nArgs+1)
            elif self.token1 == "[":
                    self.advance()
                    self.compileExpression()
                    self.writer.writePush("this" if varKind == "field" else varKind, self.table.indexOf(var))
                    self.writer.writeArthmetic("+")
                    self.writer.writePop("pointer",1)
                    self.writer.writePush("that", 0)
            self.compileExpression()
            return
        elif (self.token1 in ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]):
            op = self.token1
            self.advance()
            self.compileExpression()
            self.writer.writeArthmetic(op)
        elif(self.token1 == "("):
            self.advance()
            self.compileExpression()
            op = self.token1
            if self.token1 in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
                self.advance()
                self.compileExpression()
                self.writer.writeArthmetic(op)
        if(self.token1 in [")", ']']):
            self.advance()
            return
        else:
            return

    def compileTerm(self, lvl):
        if (self.token1Type == "integerConstant"):
            self.writer.writePush("constant", str(self.token1))


    def compileExpressionList(self):
        nArg = 0
        while (not self.token1Type in ["keyword", "symbol"]) or (self.token1 == "this") or (self.token1 == "("):
            self.compileExpression()
            nArg += 1
            if self.token1 == ",":
                self.advance()
        return nArg
    
def __main__():
    analyzer = SyntaxAnalyzer()
    if (sys.argv[1].find(".jack") != -1):
        analyzer.openFile(sys.argv[1])
        analyzer.advance()
        analyzer.compileClass()
        analyzer.closeFile()
    else:
        files = os.listdir(sys.argv[1])
        numberOfFiles = len(files)
        print(files)
        for i in range (0, numberOfFiles):
            if (files[i].find(".jack") != -1):
                analyzer.openFile(sys.argv[1] + "/" +files[i])
                analyzer.advance()
                analyzer.compileClass()
                analyzer.closeFile()
        
__main__()