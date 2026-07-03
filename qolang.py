#!/bin/python3
import argparse
import sys
import os
import io
import enum
import abc

class tTokeniser(object):

	class tLex(object):
		class eType(enum.Enum):
			IDENT=enum.auto()
			COLON=enum.auto()
			LPAREN=enum.auto()
			RPAREN=enum.auto()
			COMMA=enum.auto()
			EQ=enum.auto()
			EQEQ=enum.auto()
			LBRACE=enum.auto()
			RBRACE=enum.auto()
			GT=enum.auto()
			LT=enum.auto()
			GTEQ=enum.auto()
			LTEQ=enum.auto()
			LTLT=enum.auto()
			GTGT=enum.auto()
			LTLTEQ=enum.auto()
			GTGTEQ=enum.auto()
			PLUS=enum.auto()
			DASH=enum.auto()
			ASTR=enum.auto()
			FSLASH=enum.auto()
			PLUSEQ=enum.auto()
			DASHEQ=enum.auto()
			ASTREQ=enum.auto()
			FSLASHEQ=enum.auto()
			PERCENT=enum.auto()
			PERCENTEQ=enum.auto()
			CARET=enum.auto()
			CARETEQ=enum.auto()
			AMP=enum.auto()
			PIPE=enum.auto()
			XOR=enum.auto()
			TIL=enum.auto()
			AMPEQ=enum.auto()
			PIPEEQ=enum.auto()
			TILEQ=enum.auto()
			EXCLAM=enum.auto()
			EXCLAMEQ=enum.auto()

			KWIF=enum.auto()
			KWELSE=enum.auto()
			KWAND=enum.auto()
			KWOR=enum.auto()
			KWRET=enum.auto()
			KWWHILE=enum.auto()

			TYPEIU8=enum.auto()
			TYPEIS8=enum.auto()
			TYPEIU16=enum.auto()
			TYPEIS16=enum.auto()
			TYPEIU32=enum.auto()
			TYPEIS32=enum.auto()
			TYPEIU64=enum.auto()
			TYPEIS64=enum.auto()
			TYPEFP32=enum.auto()
			TYPEFP64=enum.auto()
			TYPEBLN=enum.auto()
			TYPENONE=enum.auto()
			TYPEPTR=enum.auto()

			LITIU=enum.auto()
			LITFP=enum.auto()
			LITSTR=enum.auto()
			LITCHR=enum.auto()
			LITTRUE=enum.auto()
			LITFALSE=enum.auto()
			LITNULL=enum.auto()

		def __init__(self, type, rawValue, fileName, lineNum, colNum, calcInt=0, calcFlt=0.0, calcStr=[]):
			self.type = type
			self.rawValue = rawValue
			self.fileName = fileName
			self.lineNum = lineNum
			self.colNum = colNum
			self.calcInt = calcInt
			self.calcFlt = calcFlt
			self.calcStr = calcStr
		def __repr__(self):
			return f'(@{self.lineNum},{self.colNum}) {str(self.type)[6:]}: \'{self.rawValue}\' {self.calcInt}/{self.calcFlt}/{self.calcStr}'

	def __init__(self, fileName):
		self.colNum = 0
		self.lineNum = 1
		self.fileName = fileName
		self.file = open(fileName, 'r')
		self.curr = ''
		self.stack = ''
		self.lexemes = []
		self.lastReadByte = 1
	def __del__(self):
		self.file.close()
	def nxt(self):
		self.lastReadByte += 1
		self.curr = self.file.read(1)
		self.colNum += 1
	def ahd(self):
		nextChar = self.file.read(1)
		self.file.seek(self.lastReadByte - 1, io.SEEK_SET)
		return nextChar
	def add(self, type, rawValue='', lineNum=-1, colNum=-1, calcInt=0, calcFlt=0.0, calcStr=[]):
		if lineNum == -1: lineNum = self.lineNum
		if colNum == -1: colNum = self.colNum
		if rawValue == '': rawValue = self.curr
		self.lexemes.append(tTokeniser.tLex(type, rawValue, self.fileName, lineNum, colNum, calcInt=calcInt, calcFlt=calcFlt, calcStr=calcStr))
	def num(self):
		lineNum = self.lineNum
		colNum = self.colNum
		self.stack += self.curr
		peekedChar = self.ahd()
		intBase = 10
		if self.curr == '0':
			if peekedChar == 'H' or peekedChar == 'h':
				self.stack += peekedChar
				intBase = 16
				self.nxt()
				peekedChar = self.ahd()
			elif peekedChar == 'O' or peekedChar == 'o':
				self.stack += peekedChar
				intBase = 8
				self.nxt()
				peekedChar = self.ahd()
			elif peekedChar == 'B' or peekedChar == 'b':
				self.stack += peekedChar
				intBase = 2
				self.nxt()
				peekedChar = self.ahd()
		if intBase == 10:
			decimalPoint = False
			exponentMark = False
			expSign = False
			while True:
				if peekedChar.isnumeric() or peekedChar == '_':
					self.nxt()
					self.stack += self.curr
					peekedChar = self.ahd()
				elif exponentMark == True and (peekedChar == '-' or peekedChar == '+'):
					if expSign == True:
						self.nxt()
						print(f'ERR: Unexpected repeated sign in numeric literal exponent @ {self.fileName}:{self.lineNum}:{self.colNum}.')
						exit(1)
					self.nxt()
					self.stack += self.curr
					peekedChar = self.ahd()
					expSign = True
				elif peekedChar == '.':
					if decimalPoint == True:
						self.nxt()
						print(f'ERR: Unexpected repeated decimal point in numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
						exit(1)
					self.nxt()
					self.stack += self.curr
					peekedChar = self.ahd()
					decimalPoint = True
				elif peekedChar == 'E' or peekedChar == 'e':
					if exponentMark == True:
						self.nxt()
						print(f'ERR: Unexpected repeated exponent in numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
						exit(1)
					self.nxt()
					self.stack += self.curr
					peekedChar = self.ahd()
					decimalPoint = True
					exponentMark = True
				elif peekedChar.isalpha():
					self.nxt()
					print(f'ERR: Unexpected character \'{peekedChar}\' in numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else: break
			if decimalPoint == True:
				calcFlt = float(''.join(self.stack.split('_')))
				self.add(tTokeniser.tLex.eType.LITFP, self.stack, lineNum, colNum, calcFlt=calcFlt)
			else:
				calcInt = int(''.join(self.stack.split('_')))
				self.add(tTokeniser.tLex.eType.LITIU, self.stack, lineNum, colNum, calcInt=calcInt)
		elif intBase == 16:
			while True:
				if peekedChar.isnumeric() or peekedChar == '_' or peekedChar in ['A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']:
					self.nxt()
					self.stack += self.curr
					peekedChar = self.ahd()
				elif peekedChar.isalpha():
					self.nxt()
					print(f'ERR: Unexpected character \'{peekedChar}\' in hexadecimal numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else: break
			calcInt = int(''.join(self.stack[2:].split('_')), intBase)
			self.add(tTokeniser.tLex.eType.LITIU, self.stack, lineNum, colNum, calcInt=calcInt)
		elif intBase == 8:
			while True:
				if peekedChar in [str(idx) for idx in range(0, 8)] or peekedChar == '_':
					self.nxt()
					self.stack += self.curr
					peekedChar = self.ahd()
				elif peekedChar.isalnum():
					self.nxt()
					print(f'ERR: Unexpected character \'{peekedChar}\' in octal numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else: break
			calcInt = int(''.join(self.stack[2:].split('_')), intBase)
			self.add(tTokeniser.tLex.eType.LITIU, self.stack, lineNum, colNum, calcInt=calcInt)
		elif intBase == 2:
			while True:
				if peekedChar == '0' or peekedChar == '1' or peekedChar == '_':
					self.nxt()
					self.stack += self.curr
					peekedChar = self.ahd()
				elif peekedChar.isalnum():
					self.nxt()
					print(f'ERR: Unexpected character \'{peekedChar}\' in binary numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else: break
			calcInt = int(''.join(self.stack[2:].split('_')), intBase)
			self.add(tTokeniser.tLex.eType.LITIU, self.stack, lineNum, colNum, calcInt=calcInt)
		self.stack = ''
	def ident(self):
		lineNum = self.lineNum
		colNum = self.colNum
		self.stack += self.curr
		peekedChar = self.ahd()
		while peekedChar.isalnum() or peekedChar == '_':
			self.nxt()
			self.stack += self.curr
			peekedChar = self.ahd()
		if self.stack == 'if': self.add(tTokeniser.tLex.eType.KWIF, self.stack, lineNum, colNum)
		elif self.stack == 'else': self.add(tTokeniser.tLex.eType.KWELSE, self.stack, lineNum, colNum)
		elif self.stack == 'ret': self.add(tTokeniser.tLex.eType.KWRET, self.stack, lineNum, colNum)
		elif self.stack == 'while': self.add(tTokeniser.tLex.eType.KWWHILE, self.stack, lineNum, colNum)
		elif self.stack == 'True': self.add(tTokeniser.tLex.eType.LITTRUE, self.stack, lineNum, colNum)
		elif self.stack == 'False': self.add(tTokeniser.tLex.eType.LITFALSE, self.stack, lineNum, colNum)
		elif self.stack == 'Null': self.add(tTokeniser.tLex.eType.LITNULL, self.stack, lineNum, colNum)
		elif self.stack == 'and': self.add(tTokeniser.tLex.eType.KWAND, self.stack, lineNum, colNum)
		elif self.stack == 'or': self.add(tTokeniser.tLex.eType.KWOR, self.stack, lineNum, colNum)
		elif self.stack == 'tIU8': self.add(tTokeniser.tLex.eType.TYPEIU8, self.stack, lineNum, colNum)
		elif self.stack == 'tIS8': self.add(tTokeniser.tLex.eType.TYPEIS8, self.stack, lineNum, colNum)
		elif self.stack == 'tIU16': self.add(tTokeniser.tLex.eType.TYPEIU16, self.stack, lineNum, colNum)
		elif self.stack == 'tIS16': self.add(tTokeniser.tLex.eType.TYPEIS16, self.stack, lineNum, colNum)
		elif self.stack == 'tIU32': self.add(tTokeniser.tLex.eType.TYPEIU32, self.stack, lineNum, colNum)
		elif self.stack == 'tIS32': self.add(tTokeniser.tLex.eType.TYPEIS32, self.stack, lineNum, colNum)
		elif self.stack == 'tIU64': self.add(tTokeniser.tLex.eType.TYPEIU64, self.stack, lineNum, colNum)
		elif self.stack == 'tIS64': self.add(tTokeniser.tLex.eType.TYPEIS64, self.stack, lineNum, colNum)
		elif self.stack == 'tFP32': self.add(tTokeniser.tLex.eType.TYPEFP32, self.stack, lineNum, colNum)
		elif self.stack == 'tFP64': self.add(tTokeniser.tLex.eType.TYPEFP64, self.stack, lineNum, colNum)
		elif self.stack == 'tBln': self.add(tTokeniser.tLex.eType.TYPEBLN, self.stack, lineNum, colNum)
		elif self.stack == 'tNone': self.add(tTokeniser.tLex.eType.TYPENONE, self.stack, lineNum, colNum)
		elif self.stack == 'tPtr': self.add(tTokeniser.tLex.eType.TYPEPTR, self.stack, lineNum, colNum)
		else: self.add(tTokeniser.tLex.eType.IDENT, self.stack, lineNum, colNum)
		self.stack = ''
	def cstr(self):
		lineNum = self.lineNum
		colNum = self.colNum
		self.stack += self.curr
		calcStr = []
		ahdChar = self.ahd()
		while ahdChar != '"':
			if ahdChar in ['\n', '\b', '\r', '\v', '\f']:
				print(f'ERR: Unclosed string literal @ {self.fileName}:{lineNum}:{colNum}.')
				exit(1)
			elif ahdChar == '\\':
				self.nxt()
				ahdChar = self.ahd()
				self.stack += self.curr
				if ahdChar == 'n': calcStr.append(ord('\n'))
				elif ahdChar == 't': calcStr.append(ord('\t'))
				elif ahdChar == 'r': calcStr.append(ord('\r'))
				elif ahdChar == 'v': calcStr.append(ord('\v'))
				elif ahdChar == '\'':calcStr.append(ord('\''))
				elif ahdChar == '0': calcStr.append(ord('\0'))
				elif ahdChar == 'f': calcStr.append(ord('\f'))
				elif ahdChar == '"': calcStr.append(ord('"'))
				elif ahdChar == 'b': calcStr.append(ord('\b'))
				elif ahdChar == '\\':calcStr.append(ord('\\'))
				else:
					print(f'ERR: Unsupported escape character \'\\{self.curr}\' in string literal @ {self.fileName}:{lineNum}:{colNum}.')
					exit(1)
				self.nxt()
				ahdChar = self.ahd()
				self.stack += self.curr
			else:
				self.nxt()
				ahdChar = self.ahd()
				self.stack += self.curr
				calcStr.append(ord(self.curr))
		self.nxt()
		self.stack += self.curr
		calcStr.append(0)
		self.add(tTokeniser.tLex.eType.LITSTR, self.stack, lineNum, colNum, calcStr=calcStr)
		self.stack = ''
	def strt(self):
		while True:
			self.nxt()
			if self.curr == '': break
			elif self.curr == '\n':
				self.lineNum += 1
				self.colNum = 0
			elif self.curr == '\r': self.colNum = 0
			elif self.curr == ' ' or self.curr == '\t': continue
			elif self.curr == ':': self.add(tTokeniser.tLex.eType.COLON)
			elif self.curr == '(': self.add(tTokeniser.tLex.eType.LPAREN)
			elif self.curr == ')': self.add(tTokeniser.tLex.eType.RPAREN)
			elif self.curr == ',': self.add(tTokeniser.tLex.eType.COMMA)
			elif self.curr == '{': self.add(tTokeniser.tLex.eType.LBRACE)
			elif self.curr == '}': self.add(tTokeniser.tLex.eType.RBRACE)
			elif self.curr == ';':
				while True:
					ahdChar = self.ahd()
					if ahdChar == '\n' or ahdChar == '': break
					self.nxt()
			elif self.curr == '^':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.CARETEQ, '^=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.CARET)
			elif self.curr == '=':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.EQEQ, '==')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.EQ)
			elif self.curr == '!':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.EXCLAMEQ, '!=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.EXCLAM)
			elif self.curr == '<':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.LTEQ, '<=')
					self.nxt()
				elif ahdChar == '<':
					colNum = self.colNum
					self.nxt()
					if self.ahd() == '=':
						self.add(tTokeniser.tLex.eType.LTLTEQ, '<<=', self.lineNum, colNum)
						self.nxt()
					else: self.add(tTokeniser.tLex.eType.LTLT, '<<', self.lineNum, colNum)
				else: self.add(tTokeniser.tLex.eType.LT)
			elif self.curr == '>':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.GTEQ, '>=')
					self.nxt()
				elif ahdChar == '>':
					colNum = self.colNum
					self.nxt()
					if self.ahd() == '=':
						self.add(tTokeniser.tLex.eType.GTGTEQ, '>>=', self.lineNum, colNum)
						self.nxt()
					else: self.add(tTokeniser.tLex.eType.GTGT, '>>', self.lineNum, colNum)
				else: self.add(tTokeniser.tLex.eType.GT)
			elif self.curr == '+':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.PLUSEQ, '+=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.PLUS)
			elif self.curr == '-':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.DASHEQ, '-=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.DASH)
			elif self.curr == '*':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.ASTREQ, '*=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.ASTR)
			elif self.curr == '/':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.FSLASHEQ, '/=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.FSLASH)
			elif self.curr == '%':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.PERCENTEQ, '%=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.PERCENT)
			elif self.curr == '&':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.AMPEQ, '&=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.AMP)
			elif self.curr == '|':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.PIPEEQ, '|=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.PIPE)
			elif self.curr == '~':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.TILEQ, '~=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.TIL)
			elif self.curr.isalpha() or self.curr == '_': self.ident()
			elif self.curr.isnumeric(): self.num()
			elif self.curr == '"': self.cstr()
			elif self.curr == '\'':
				ahdChar = self.ahd()
				lineNum = self.lineNum
				colNum = self.colNum
				if ahdChar == '\\':
					self.nxt()
					self.nxt()
					ahdChar = self.ahd()
					if ahdChar != '\'':
						print(f'ERR: Unexpected character \'{ahdChar}\' in character literal encountered @ {self.fileName}:{self.lineNum}:{self.colNum}.')
						exit(1)
					elif self.curr == 'n': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum, calcInt=ord('\n'))
					elif self.curr == 't': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum, calcInt=ord('\t'))
					elif self.curr == 'r': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum, calcInt=ord('\r'))
					elif self.curr == 'v': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum, calcInt=ord('\v'))
					elif self.curr == '\'': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum,calcInt=ord('\''))
					elif self.curr == 'f': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum, calcInt=ord('\f'))
					elif self.curr == '0': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum, calcInt=ord('\0'))
					elif self.curr == '"': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum, calcInt=ord('"'))
					elif self.curr == 'b': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum, calcInt=ord('\b'))
					elif self.curr == '\\': self.add(tTokeniser.tLex.eType.LITCHR, f'\'\\{self.curr}\'', lineNum, colNum,calcInt=ord('\\'))
					else:
						print(f'ERR: Unsupported escape character \'\\{self.curr}\' in character literal @ {self.fileName}:{lineNum}:{colNum}.')
						exit(1)
					self.nxt()
				elif ahdChar.isspace() and not (ahdChar == ' ' or ahdChar == '\t'):
					print(f'ERR: Unsupported whitespace encountered in character literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				elif ahdChar == '\'':
					print(f'ERR: Empty char literal encountered @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else:
					self.nxt()
					ahdChar = self.ahd()
					if ahdChar != '\'':
						self.nxt()
						print(f'ERR: Unexpected character \'{ahdChar}\' in character literal encountered @ {self.fileName}:{self.lineNum}:{self.colNum}.')
						exit(1)
					self.add(tTokeniser.tLex.eType.LITCHR, f'\'{self.curr}\'', lineNum, colNum, calcInt=ord(self.curr))
					self.nxt()
			else:
				print(f'ERR: Unknown lexeme \'{self.curr}\' encountered @ {self.fileName}:{self.lineNum}:{self.colNum}.')
				exit(1)

class tParser(object):
	class tParserObj(abc.ABC):
		@abc.abstractmethod
		def print(self, indnt: int=0): pass
	class tPrim(tParserObj): pass
	class tLit(tPrim):
		class eType(enum.Enum):
			IU=enum.auto()
			FP=enum.auto()
			STR=enum.auto()
			CHR=enum.auto()
			TRUE=enum.auto()
			FALSE=enum.auto()
			NULL=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if lexeme.type == tTokeniser.tLex.eType.LITIU: self.type = tParser.tLit.eType.IU
			elif lexeme.type == tTokeniser.tLex.eType.LITFP: self.type = tParser.tLit.eType.FP
			elif lexeme.type == tTokeniser.tLex.eType.LITSTR: self.type = tParser.tLit.eType.STR
			elif lexeme.type == tTokeniser.tLex.eType.LITCHR: self.type = tParser.tLit.eType.CHR
			elif lexeme.type == tTokeniser.tLex.eType.LITTRUE: self.type = tParser.tLit.eType.TRUE
			elif lexeme.type == tTokeniser.tLex.eType.LITFALSE: self.type = tParser.tLit.eType.FALSE
			elif lexeme.type == tTokeniser.tLex.eType.LITNULL: self.type = tParser.tLit.eType.NULL
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range (indnt): print('\t',end='')
			print('LITERAL', end='')
			if self.type == tParser.tLit.eType.IU: print("(IU) " + str(self.lexeme.calcInt))
			elif self.type == tParser.tLit.eType.FP: print("(FP) " + str(self.lexeme.calcFlt))
			elif self.type == tParser.tLit.eType.STR: print("(STR) " + self.lexeme.calcStr)
			elif self.type == tParser.tLit.eType.CHR: print("(CHR) " + str(self.lexeme.calcInt))
			elif self.type == tParser.tLit.eType.TRUE: print("(TRUE) " + "True")
			elif self.type == tParser.tLit.eType.FALSE: print("(FALSE) " + "False")
			elif self.type == tParser.tLit.eType.NULL: print("(NULL) " + "Null")
			else: assert(False and "Unreachable.")
	class tUnry(tParserObj):
		class eType(enum.Enum):
			POS=enum.auto()
			NEG=enum.auto()
			NOT=enum.auto()
			INV=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.child: tParser.tUnry | tParser.tPrim
			if lexeme.type == tTokeniser.tLex.eType.PLUS: self.type = tParser.tUnry.eType.POS
			elif lexeme.type == tTokeniser.tLex.eType.DASH: self.type = tParser.tUnry.eType.NEG
			elif lexeme.type == tTokeniser.tLex.eType.EXCLAM: self.type = tParser.tUnry.eType.NOT
			elif lexeme.type == tTokeniser.tLex.eType.TIL: self.type = tParser.tUnry.eType.INV
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range (indnt): print('\t',end='')
			print('UNARY', end='')
			if self.type == tParser.tUnry.eType.POS: print("(+)")
			elif self.type == tParser.tUnry.eType.NEG: print("(-)")
			elif self.type == tParser.tUnry.eType.NOT: print("(!)")
			elif self.type == tParser.tUnry.eType.INV: print("(~)")
			else: assert(False and "Unreachable.")
			self.child.print(indnt + 1)
	def __init__(self):
		self.idx = 0
		self.lexemes = []
		self.tree: tParser.tParserObj
	def lex(self, fileName):
		t = tTokeniser(fileName)
		t.strt()
		self.lexemes = t.lexemes.copy()
	def curr(self) -> tTokeniser.tLex:
		return self.lexemes[self.idx]
	def lit(self):
		ret = tParser.tLit(self.curr())
		self.idx += 1
		return ret
	def prim(self):
		return self.lit()
	def unry(self):
		try:
			ret = tParser.tUnry(self.curr())
			self.idx += 1
			ret.child = self.unry()
			return ret
		except ValueError:
			return self.prim()
	def run(self):
		try:
			self.tree = self.unry()
		except ValueError:
			print(f'ERR: Unexpected token encountered @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]}.')
			exit(1)
		if self.idx < len(self.lexemes):
			print(f'ERR: Unhandled tokens, starting @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]}.')
			exit(1)
	def print(self):
		self.tree.print()

if __name__ == '__main__':
	argParser = argparse.ArgumentParser(prog='qolang', description='qolang language compiler.')
	argParser.add_argument('infiles', help='Input source files.', nargs='+')
	args = argParser.parse_args(sys.argv[1:])
	for fileName in args.infiles:
		if not os.path.exists(fileName):
			print(f'ERR: File \'{fileName}\' does not exist.')
			sys.exit(1)
	for fileName in args.infiles:
		parser = tParser()
		parser.lex(fileName)
		parser.run()
		parser.print()