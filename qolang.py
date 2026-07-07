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
			LBRACK=enum.auto()
			RBRACK=enum.auto()
			COMMA=enum.auto()
			PERIOD=enum.auto()
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
			FSLSH=enum.auto()
			PLUSEQ=enum.auto()
			DASHEQ=enum.auto()
			ASTREQ=enum.auto()
			FSLSHEQ=enum.auto()
			PRCNT=enum.auto()
			PRCNTEQ=enum.auto()
			CARET=enum.auto()
			CARETEQ=enum.auto()
			ATSGN=enum.auto()
			AMP=enum.auto()
			PIPE=enum.auto()
			TIL=enum.auto()
			AMPEQ=enum.auto()
			PIPEEQ=enum.auto()
			TILEQ=enum.auto()
			EXCLAM=enum.auto()
			EXCLAMEQ=enum.auto()
			NEWLINE=enum.auto()

			KWIF=enum.auto()
			KWELIF=enum.auto()
			KWELSE=enum.auto()
			KWAND=enum.auto()
			KWOR=enum.auto()
			KWRET=enum.auto()
			KWWHILE=enum.auto()
			KWBRK=enum.auto()
			KWCONT=enum.auto()

			TIU8=enum.auto()
			TIS8=enum.auto()
			TIU16=enum.auto()
			TIS16=enum.auto()
			TIU32=enum.auto()
			TIS32=enum.auto()
			TIU64=enum.auto()
			TIS64=enum.auto()
			TFP32=enum.auto()
			TFP64=enum.auto()
			TBLN=enum.auto()
			TNONE=enum.auto()
			TPTR=enum.auto()

			LITIU=enum.auto()
			LITFP=enum.auto()
			LITSTR=enum.auto()
			LITCHR=enum.auto()
			LITTRUE=enum.auto()
			LITFALSE=enum.auto()
			LITNULL=enum.auto()

			EOF=enum.auto()

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
			return f'(@ {self.lineNum},{self.colNum}) {str(self.type)[6:]}: \'{self.rawValue}\' {self.calcInt}/{self.calcFlt}/{self.calcStr}'

	def __init__(self, fileName):
		self.colNum = 0
		self.lineNum = 1
		self.fileName = fileName
		self.file = open(fileName, 'r')
		self.curr = ''
		self.stack = ''
		self.lexemes = []
		self.lastReadByte = 1
		self.parenDepth = 0
		self.brackDepth = 0
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
		elif self.stack == 'elif': self.add(tTokeniser.tLex.eType.KWELIF, self.stack, lineNum, colNum)
		elif self.stack == 'else': self.add(tTokeniser.tLex.eType.KWELSE, self.stack, lineNum, colNum)
		elif self.stack == 'ret': self.add(tTokeniser.tLex.eType.KWRET, self.stack, lineNum, colNum)
		elif self.stack == 'while': self.add(tTokeniser.tLex.eType.KWWHILE, self.stack, lineNum, colNum)
		elif self.stack == 'brk': self.add(tTokeniser.tLex.eType.KWBRK, self.stack, lineNum, colNum)
		elif self.stack == 'cont': self.add(tTokeniser.tLex.eType.KWCONT, self.stack, lineNum, colNum)
		elif self.stack == 'True': self.add(tTokeniser.tLex.eType.LITTRUE, self.stack, lineNum, colNum)
		elif self.stack == 'False': self.add(tTokeniser.tLex.eType.LITFALSE, self.stack, lineNum, colNum)
		elif self.stack == 'Null': self.add(tTokeniser.tLex.eType.LITNULL, self.stack, lineNum, colNum)
		elif self.stack == 'and': self.add(tTokeniser.tLex.eType.KWAND, self.stack, lineNum, colNum)
		elif self.stack == 'or': self.add(tTokeniser.tLex.eType.KWOR, self.stack, lineNum, colNum)
		elif self.stack == 'tIU8': self.add(tTokeniser.tLex.eType.TIU8, self.stack, lineNum, colNum)
		elif self.stack == 'tIS8': self.add(tTokeniser.tLex.eType.TIS8, self.stack, lineNum, colNum)
		elif self.stack == 'tIU16': self.add(tTokeniser.tLex.eType.TIU16, self.stack, lineNum, colNum)
		elif self.stack == 'tIS16': self.add(tTokeniser.tLex.eType.TIS16, self.stack, lineNum, colNum)
		elif self.stack == 'tIU32': self.add(tTokeniser.tLex.eType.TIU32, self.stack, lineNum, colNum)
		elif self.stack == 'tIS32': self.add(tTokeniser.tLex.eType.TIS32, self.stack, lineNum, colNum)
		elif self.stack == 'tIU64': self.add(tTokeniser.tLex.eType.TIU64, self.stack, lineNum, colNum)
		elif self.stack == 'tIS64': self.add(tTokeniser.tLex.eType.TIS64, self.stack, lineNum, colNum)
		elif self.stack == 'tFP32': self.add(tTokeniser.tLex.eType.TFP32, self.stack, lineNum, colNum)
		elif self.stack == 'tFP64': self.add(tTokeniser.tLex.eType.TFP64, self.stack, lineNum, colNum)
		elif self.stack == 'tBln': self.add(tTokeniser.tLex.eType.TBLN, self.stack, lineNum, colNum)
		elif self.stack == 'tNone': self.add(tTokeniser.tLex.eType.TNONE, self.stack, lineNum, colNum)
		elif self.stack == 'tPtr': self.add(tTokeniser.tLex.eType.TPTR, self.stack, lineNum, colNum)
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
				print(f'\tGot \'{ahdChar}\' @ {self.fileName}:{self.lineNum}:{self.colNum}.')
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
				if self.parenDepth == 0 and self.brackDepth == 0: self.add(tTokeniser.tLex.eType.NEWLINE)
			elif self.curr == '\r': self.colNum = 0
			elif self.curr == ' ' or self.curr == '\t': continue
			elif self.curr == ':': self.add(tTokeniser.tLex.eType.COLON)
			elif self.curr == '(':
				self.parenDepth += 1
				self.add(tTokeniser.tLex.eType.LPAREN)
			elif self.curr == ')':
				self.parenDepth -= 1
				self.add(tTokeniser.tLex.eType.RPAREN)
			elif self.curr == ',': self.add(tTokeniser.tLex.eType.COMMA)
			elif self.curr == '.': self.add(tTokeniser.tLex.eType.PERIOD)
			elif self.curr == '{': self.add(tTokeniser.tLex.eType.LBRACE)
			elif self.curr == '}': self.add(tTokeniser.tLex.eType.RBRACE)
			elif self.curr == '@': self.add(tTokeniser.tLex.eType.ATSGN)
			elif self.curr == '[':
				self.brackDepth += 1
				self.add(tTokeniser.tLex.eType.LBRACK)
			elif self.curr == ']':
				self.brackDepth -= 1
				self.add(tTokeniser.tLex.eType.RBRACK)
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
					self.add(tTokeniser.tLex.eType.FSLSHEQ, '/=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.FSLSH)
			elif self.curr == '%':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tTokeniser.tLex.eType.PRCNTEQ, '%=')
					self.nxt()
				else: self.add(tTokeniser.tLex.eType.PRCNT)
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
		self.add(tTokeniser.tLex.eType.EOF)
class tParser(object):
	class tParserObj(abc.ABC):
		@abc.abstractmethod
		def __init__(self, lexeme: tTokeniser.tLex): pass
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
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tLit.eType.IU: print('(IU) ' + str(self.lexeme.calcInt))
			elif self.type == tParser.tLit.eType.FP: print('(FP) ' + str(self.lexeme.calcFlt))
			elif self.type == tParser.tLit.eType.STR: print('(STR) ' + self.lexeme.calcStr)
			elif self.type == tParser.tLit.eType.CHR: print('(CHR) ' + str(self.lexeme.calcInt))
			elif self.type == tParser.tLit.eType.TRUE: print('(TRUE) True')
			elif self.type == tParser.tLit.eType.FALSE: print('(FALSE) False')
			elif self.type == tParser.tLit.eType.NULL: print('(NULL) Null')
	class tIdnt(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if lexeme.type != tTokeniser.tLex.eType.IDENT: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			print('(' + self.lexeme.rawValue + ')')
	class tPstFx(tParserObj):
		class eType(enum.Enum):
			ACS=enum.auto()
			ARR=enum.auto()
			CALL=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj | list | None
			if lexeme.type == tTokeniser.tLex.eType.LPAREN: self.type = tParser.tPstFx.eType.CALL
			elif lexeme.type == tTokeniser.tLex.eType.LBRACK: self.type = tParser.tPstFx.eType.ARR
			elif lexeme.type == tTokeniser.tLex.eType.PERIOD: self.type = tParser.tPstFx.eType.ACS
			else: raise ValueError
		def fnsh(self, lexeme: tTokeniser.tLex):
			if self.type == tParser.tPstFx.eType.CALL and lexeme.type != tTokeniser.tLex.eType.RPAREN:
				print(f'ERR: Unclosed parentheses during function call, first opened @ {self.lexeme.fileName}:{self.lexeme.lineNum}:{self.lexeme.colNum}.')
				print(f'\tGot {str(lexeme.type).rsplit('.', 1)[-1]} \'{lexeme.rawValue}\' @ {lexeme.fileName}:{lexeme.lineNum}:{lexeme.colNum}.')
				exit(1)
			elif self.type == tParser.tPstFx.eType.ARR and lexeme.type != tTokeniser.tLex.eType.RBRACK:
				print(f'ERR: Unclosed brackets during array accessor, first opened @ {self.lexeme.fileName}:{self.lexeme.lineNum}:{self.lexeme.colNum}.')
				print(f'\tGot {str(lexeme.type).rsplit('.', 1)[-1]} \'{lexeme.rawValue}\' @ {lexeme.fileName}:{lexeme.lineNum}:{lexeme.colNum}.')
				exit(1)
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tPstFx.eType.CALL: print('(())')
			elif self.type == tParser.tPstFx.eType.ARR: print('([])')
			elif self.type == tParser.tPstFx.eType.ACS: print('(.)')
			self.lhs.print(indnt+1)
			if isinstance(self.rhs, list):
				for idx in range(len(self.rhs)): self.rhs[idx].print(indnt+1)
			elif self.rhs != None: self.rhs.print(indnt+1)
	class tUnry(tParserObj):
		class eType(enum.Enum):
			POS=enum.auto()
			NEG=enum.auto()
			NOT=enum.auto()
			INV=enum.auto()
			PTR=enum.auto()
			AT=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.child: tParser.tParserObj
			if lexeme.type == tTokeniser.tLex.eType.PLUS: self.type = tParser.tUnry.eType.POS
			elif lexeme.type == tTokeniser.tLex.eType.DASH: self.type = tParser.tUnry.eType.NEG
			elif lexeme.type == tTokeniser.tLex.eType.EXCLAM: self.type = tParser.tUnry.eType.NOT
			elif lexeme.type == tTokeniser.tLex.eType.TIL: self.type = tParser.tUnry.eType.INV
			elif lexeme.type == tTokeniser.tLex.eType.CARET: self.type = tParser.tUnry.eType.PTR
			elif lexeme.type == tTokeniser.tLex.eType.ATSGN: self.type = tParser.tUnry.eType.AT
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tUnry.eType.POS: print('(+)')
			elif self.type == tParser.tUnry.eType.NEG: print('(-)')
			elif self.type == tParser.tUnry.eType.NOT: print('(!)')
			elif self.type == tParser.tUnry.eType.INV: print('(~)')
			elif self.type == tParser.tUnry.eType.PTR: print('(^)')
			elif self.type == tParser.tUnry.eType.AT: print('(@)')
			self.child.print(indnt+1)
	class tFact(tParserObj):
		class eType(enum.Enum):
			MUL=enum.auto()
			DIV=enum.auto()
			MOD=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lexeme.type == tTokeniser.tLex.eType.ASTR: self.type = tParser.tFact.eType.MUL
			elif lexeme.type == tTokeniser.tLex.eType.FSLSH: self.type = tParser.tFact.eType.DIV
			elif lexeme.type == tTokeniser.tLex.eType.PRCNT: self.type = tParser.tFact.eType.MOD
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tFact.eType.MUL: print('(*)')
			elif self.type == tParser.tFact.eType.DIV: print('(/)')
			elif self.type == tParser.tFact.eType.MOD: print('(%)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tTerm(tParserObj):
		class eType(enum.Enum):
			ADD=enum.auto()
			SUB=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lexeme.type == tTokeniser.tLex.eType.PLUS: self.type = tParser.tTerm.eType.ADD
			elif lexeme.type == tTokeniser.tLex.eType.DASH: self.type = tParser.tTerm.eType.SUB
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tTerm.eType.ADD: print('(+)')
			elif self.type == tParser.tTerm.eType.SUB: print('(-)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tBtws(tParserObj):
		class eType(enum.Enum):
			AND=enum.auto()
			OR=enum.auto()
			EOR=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lexeme.type == tTokeniser.tLex.eType.AMP: self.type = tParser.tBtws.eType.AND
			elif lexeme.type == tTokeniser.tLex.eType.PIPE: self.type = tParser.tBtws.eType.OR
			elif lexeme.type == tTokeniser.tLex.eType.CARET: self.type = tParser.tBtws.eType.EOR
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tBtws.eType.AND: print('(&)')
			elif self.type == tParser.tBtws.eType.OR: print('(|)')
			elif self.type == tParser.tBtws.eType.EOR: print('(^)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tShft(tParserObj):
		class eType(enum.Enum):
			LSHF=enum.auto()
			RSHF=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lexeme.type == tTokeniser.tLex.eType.LTLT: self.type = tParser.tShft.eType.LSHF
			elif lexeme.type == tTokeniser.tLex.eType.GTGT: self.type = tParser.tShft.eType.RSHF
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tShft.eType.LSHF: print('(<<)')
			elif self.type == tParser.tShft.eType.RSHF: print('(>>)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tComp(tParserObj):
		class eType(enum.Enum):
			LS=enum.auto()
			LSEQ=enum.auto()
			GR=enum.auto()
			GREQ=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lexeme.type == tTokeniser.tLex.eType.LT: self.type = tParser.tComp.eType.LS
			elif lexeme.type == tTokeniser.tLex.eType.LTEQ: self.type = tParser.tComp.eType.LSEQ
			elif lexeme.type == tTokeniser.tLex.eType.GT: self.type = tParser.tComp.eType.GR
			elif lexeme.type == tTokeniser.tLex.eType.GTEQ: self.type = tParser.tComp.eType.GREQ
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tComp.eType.LS: print('(<)')
			elif self.type == tParser.tComp.eType.LSEQ: print('(<=)')
			elif self.type == tParser.tComp.eType.GR: print('(>)')
			elif self.type == tParser.tComp.eType.GREQ: print('(>=)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tEqlt(tParserObj):
		class eType(enum.Enum):
			EQUL=enum.auto()
			NEQUL=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lexeme.type == tTokeniser.tLex.eType.EQEQ: self.type = tParser.tEqlt.eType.EQUL
			elif lexeme.type == tTokeniser.tLex.eType.EXCLAMEQ: self.type = tParser.tEqlt.eType.NEQUL
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tEqlt.eType.EQUL: print('(==)')
			elif self.type == tParser.tEqlt.eType.NEQUL: print('(!=)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tExpr(tEqlt): pass
	class tRtrn(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.child: tParser.tParserObj
			if lexeme.type != tTokeniser.tLex.eType.KWRET: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2])
			self.child.print(indnt+1)
	class tBrk(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if lexeme.type != tTokeniser.tLex.eType.KWBRK: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2])
	class tStLst(tParserObj):
		def __init__(self):
			self.kids = []
		def print(self, indnt: int=0):
			for idx in range(len(self.kids)): self.kids[idx].print(indnt)
	class tBlck(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if lexeme.type != tTokeniser.tLex.eType.LBRACE: raise ValueError
			self.child: tParser.tStLst
		def fnsh(self, lexeme: tTokeniser.tLex):
			if lexeme.type != tTokeniser.tLex.eType.RBRACE:
				print(f'ERR: Unclosed brace during block, first opened @ {self.lexeme.fileName}:{self.lexeme.lineNum}:{self.lexeme.colNum}.')
				print(f'\tGot {str(lexeme.type).rsplit('.', 1)[-1]} \'{lexeme.rawValue}\' @ {lexeme.fileName}:{lexeme.lineNum}:{lexeme.colNum}.')
				exit(1)
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2])
			for idx in range(len(self.child.kids)): self.child.kids[idx].print(indnt+1)
	class tCnd(tParserObj):
		class eType(enum.Enum):
			IF=enum.auto()
			ELIF=enum.auto()
			ELSE=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if self.lexeme.type == tTokeniser.tLex.eType.KWIF: self.type = tParser.tCnd.eType.IF
			elif self.lexeme.type == tTokeniser.tLex.eType.KWELIF: self.type = tParser.tCnd.eType.ELIF
			elif self.lexeme.type == tTokeniser.tLex.eType.KWELSE: self.type = tParser.tCnd.eType.ELSE
			else: raise ValueError
			self.cnd: tParser.tParserObj
			self.bdy: tParser.tParserObj
			self.elifs = []
			self.elseBdy: tParser.tParserObj | None = None
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tCnd.eType.IF:
				print('(IF)')
				self.cnd.print(indnt+1)
				self.bdy.print(indnt+1)
				for idx in range(len(self.elifs)): self.elifs[idx].print(indnt)
				if self.elseBdy is not None:
					print(str(type(self)).split('.')[-1][1:-2], end='')
					print('(ELSE)')
					self.elseBdy.print(indnt+1)
			elif self.type == tParser.tCnd.eType.ELIF:
				print('(ELIF)')
				self.cnd.print(indnt+1)
				self.bdy.print(indnt+1)
	class tLoop(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if self.lexeme.type != tTokeniser.tLex.eType.KWWHILE: raise ValueError
			self.cnd: tParser.tParserObj
			self.bdy: tParser.tParserObj
			self.elseBdy: tParser.tParserObj | None = None
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2], end='')
			print('(WHILE)')
			self.cnd.print(indnt+1)
			self.bdy.print(indnt+1)
			if self.elseBdy is not None:
				print(str(type(self)).split('.')[-1][1:-2], end='')
				print('(ELSE)')
				self.elseBdy.print(indnt+1)
	class tAssgn(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if self.lexeme.type != tTokeniser.tLex.eType.EQ: raise ValueError
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2])
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tCssgn(tParserObj):
		class eType(enum.Enum):
			ADD=enum.auto()
			SUB=enum.auto()
			MUL=enum.auto()
			DIV=enum.auto()
			AND=enum.auto()
			OR=enum.auto()
			EOR=enum.auto()
			MOD=enum.auto()
			NOT=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if self.lexeme.type == tTokeniser.tLex.eType.PLUSEQ: self.type = tParser.tCssgn.eType.ADD
			elif self.lexeme.type == tTokeniser.tLex.eType.DASHEQ: self.type = tParser.tCssgn.eType.SUB
			elif self.lexeme.type == tTokeniser.tLex.eType.ASTREQ: self.type = tParser.tCssgn.eType.MUL
			elif self.lexeme.type == tTokeniser.tLex.eType.FSLSHEQ: self.type = tParser.tCssgn.eType.DIV
			elif self.lexeme.type == tTokeniser.tLex.eType.AMPEQ: self.type = tParser.tCssgn.eType.AND
			elif self.lexeme.type == tTokeniser.tLex.eType.PIPEEQ: self.type = tParser.tCssgn.eType.OR
			elif self.lexeme.type == tTokeniser.tLex.eType.CARETEQ: self.type = tParser.tCssgn.eType.EOR
			elif self.lexeme.type == tTokeniser.tLex.eType.PRCNTEQ: self.type = tParser.tCssgn.eType.MOD
			elif self.lexeme.type == tTokeniser.tLex.eType.TILEQ: self.type = tParser.tCssgn.eType.NOT
			else: raise ValueError
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2],end='')
			if self.type == tParser.tCssgn.eType.ADD: print('(+=)')
			elif self.type == tParser.tCssgn.eType.SUB: print('(-=)')
			elif self.type == tParser.tCssgn.eType.MUL: print('(*=)')
			elif self.type == tParser.tCssgn.eType.DIV: print('(/=)')
			elif self.type == tParser.tCssgn.eType.AND: print('(&=)')
			elif self.type == tParser.tCssgn.eType.OR: print('(|=)')
			elif self.type == tParser.tCssgn.eType.EOR: print('(^=)')
			elif self.type == tParser.tCssgn.eType.MOD: print('(%=)')
			elif self.type == tParser.tCssgn.eType.NOT: print('(~=)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tTyp(tParserObj):
		class eType(enum.Enum):
			DEF=enum.auto()
			IU8=enum.auto()
			IS8=enum.auto()
			IU16=enum.auto()
			IS16=enum.auto()
			IU32=enum.auto()
			IS32=enum.auto()
			IU64=enum.auto()
			IS64=enum.auto()
			FP32=enum.auto()
			FP64=enum.auto()
			BLN=enum.auto()
			NONE=enum.auto()
			PTR=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if self.lexeme.type == tTokeniser.tLex.eType.IDENT: self.type = tParser.tTyp.eType.DEF
			elif self.lexeme.type == tTokeniser.tLex.eType.TIU8: self.type = tParser.tTyp.eType.IU8
			elif self.lexeme.type == tTokeniser.tLex.eType.TIS8: self.type = tParser.tTyp.eType.IS8
			elif self.lexeme.type == tTokeniser.tLex.eType.TIU16: self.type = tParser.tTyp.eType.IU16
			elif self.lexeme.type == tTokeniser.tLex.eType.TIS16: self.type = tParser.tTyp.eType.IS16
			elif self.lexeme.type == tTokeniser.tLex.eType.TIU32: self.type = tParser.tTyp.eType.IU32
			elif self.lexeme.type == tTokeniser.tLex.eType.TIS32: self.type = tParser.tTyp.eType.IS32
			elif self.lexeme.type == tTokeniser.tLex.eType.TIU64: self.type = tParser.tTyp.eType.IU64
			elif self.lexeme.type == tTokeniser.tLex.eType.TIS64: self.type = tParser.tTyp.eType.IS64
			elif self.lexeme.type == tTokeniser.tLex.eType.TFP32: self.type = tParser.tTyp.eType.FP32
			elif self.lexeme.type == tTokeniser.tLex.eType.TFP64: self.type = tParser.tTyp.eType.FP64
			elif self.lexeme.type == tTokeniser.tLex.eType.TBLN: self.type = tParser.tTyp.eType.BLN
			elif self.lexeme.type == tTokeniser.tLex.eType.TNONE: self.type = tParser.tTyp.eType.NONE
			elif self.lexeme.type == tTokeniser.tLex.eType.TPTR: self.type = tParser.tTyp.eType.PTR
			else: raise ValueError
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2],end='')
			print(f'({self.type.name})')
	class tMTyp(tParserObj):
		class eType(enum.Enum):
			ARR=enum.auto()
			PTR=enum.auto()
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			self.child: tParser.tTyp | tParser.tMTyp
			if self.lexeme.type == tTokeniser.tLex.eType.LBRACK:
				self.type = tParser.tMTyp.eType.ARR
				self.arrSz: tParser.tParserObj
			elif self.lexeme.type == tTokeniser.tLex.eType.CARET: self.type = tParser.tMTyp.eType.PTR
			else: raise ValueError
		def fnsh(self, lexeme: tTokeniser.tLex):
			if self.type == tParser.tMTyp.eType.ARR and lexeme.type != tTokeniser.tLex.eType.RBRACK:
				print(f'ERR: Unclosed square bracket started @ {self.lexeme.fileName, self.lexeme.lineNum, self.lexeme.colNum}.')
				print(f'\tGot {str(lexeme.type).rsplit('.', 1)[-1]} \'{lexeme.rawValue}\' @ {lexeme.fileName}:{lexeme.lineNum}:{lexeme.colNum}.')
				exit(1)
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2],end='')
			if self.type == tParser.tMTyp.eType.ARR:
				print('([])')
				self.arrSz.print(indnt)
			else:
				print('(^)')
			self.child.print(indnt+1)
	class tCst(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if (self.lexeme.type != tTokeniser.tLex.eType.COLON): raise ValueError
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tTyp | tParser.tMTyp
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2])
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tLgcA(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if (self.lexeme.type != tTokeniser.tLex.eType.KWAND): raise ValueError
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2])
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tLgcO(tParserObj):
		def __init__(self, lexeme: tTokeniser.tLex):
			self.lexeme = lexeme
			if (self.lexeme.type != tTokeniser.tLex.eType.KWOR): raise ValueError
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2])
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tVar(tParserObj):
		def __init__(self):
			self.vars = []
			self.type: tParser.tParserObj | None
			self.val: tParser.tParserObj | None
		def print(self, indnt: int=0):
			for _ in range(indnt): print('\t',end='')
			print(str(type(self)).split('.')[-1][1:-2])
			for var in self.vars: var.print(indnt+1)
			if self.type is not None: self.type.print(indnt+1)
			if self.val is not None: self.val.print(indnt+1)
	def __init__(self):
		self.idx = 0
		self.lexemes = []
		self.tree: tParser.tParserObj | None = None
	def lex(self, fileName):
		t = tTokeniser(fileName)
		t.strt()
		self.lexemes = t.lexemes.copy()
	def curr(self) -> tTokeniser.tLex:
		return self.lexemes[self.idx]
	def trim(self):
		while self.idx < len(self.lexemes) and self.curr().type == tTokeniser.tLex.eType.NEWLINE: self.idx+=1
	def lit(self):
		ret = tParser.tLit(self.curr())
		self.idx+=1
		return ret
	def typ(self):
		ret = tParser.tTyp(self.curr())
		self.idx+=1
		return ret
	def mtyp(self):
		try:
			ret = tParser.tMTyp(self.curr())
			self.idx+=1
			if ret.type == tParser.tMTyp.eType.ARR:
				try:
					ret.arrSz = self.expr()
				except ValueError:
					print(f'ERR: Expected expression within array type @ {self.curr().fileName, self.curr().lineNum, self.curr().colNum}.')
					print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
					exit(1)
				ret.fnsh(self.curr())
				self.idx+=1
			ret.child = self.mtyp()
		except ValueError:
			ret = self.typ()
		return ret
	def grpng(self):
		startLine = self.curr().lineNum
		startCol = self.curr().colNum
		if self.curr().type != tTokeniser.tLex.eType.LPAREN: raise ValueError
		self.idx+=1
		ret = self.expr()
		if self.curr().type != tTokeniser.tLex.eType.RPAREN:
			print(f'ERR: Unclosed parenthesis started @ {self.curr().fileName, startLine, startCol}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\' @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			exit(1)
		self.idx+=1
		return ret
	def idnt(self):
		ret = tParser.tIdnt(self.curr())
		self.idx+=1
		return ret
	def cst(self):
		ret = tParser.tCst(self.curr())
		self.idx+=1
		try:
			ret.rhs = self.mtyp()
		except ValueError:
			print(f'ERR: Expected type name after cast @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		return ret
	def prim(self):
		try:
			ret = self.grpng()
		except ValueError:
			try:
				ret = self.idnt()
			except ValueError:
				ret = self.lit()
		try:
			cst = self.cst()
			cst.lhs = ret
		except ValueError:
			return ret
		return cst
	def pstfx(self):
		root = self.prim()
		try:
			while True:
				tmp = tParser.tPstFx(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				if root.type == tParser.tPstFx.eType.CALL:
					lineNum = self.curr().lineNum
					colNum = self.curr().colNum
					root.rhs = []
					while True:
						if self.curr().type == tTokeniser.tLex.eType.RPAREN: break
						elif len(root.rhs) != 0 and self.curr().type != tTokeniser.tLex.eType.COMMA:
							print(f'ERR: Expected comma @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum} to separate arguments of function call @ {self.curr().fileName}:{lineNum}:{colNum}.')
							print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
							exit(1)
						elif self.curr().type == tTokeniser.tLex.eType.COMMA:
							self.idx+=1
						try:
							root.rhs.append(self.expr())
						except ValueError, IndexError: pass
					root.fnsh(self.curr())
					self.idx+=1
				elif root.type == tParser.tPstFx.eType.ARR:
					root.rhs = self.expr()
					root.fnsh(self.curr())
					self.idx+=1
				else:
					root.rhs = self.idnt()
		except ValueError, IndexError:
			return root
	def unry(self):
		try:
			ret = tParser.tUnry(self.curr())
		except ValueError:
			return self.pstfx()
		else:
			self.idx+=1
			ret.child = self.unry()
			return ret
	def fact(self):
		root = self.unry()
		try:
			while True:
				tmp = tParser.tFact(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.unry()
		except ValueError, IndexError:
			return root
	def term(self):
		root = self.fact()
		try:
			while True:
				tmp = tParser.tTerm(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.fact()
		except ValueError, IndexError:
			return root
	def btws(self):
		root = self.term()
		try:
			while True:
				tmp = tParser.tBtws(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.term()
		except ValueError, IndexError:
			return root
	def shft(self):
		root = self.btws()
		try:
			while True:
				tmp = tParser.tShft(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.btws()
		except ValueError, IndexError:
			return root
	def comp(self):
		root = self.shft()
		try:
			while True:
				tmp = tParser.tComp(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.shft()
		except ValueError, IndexError:
			return root
	def eqlt(self):
		root = self.comp()
		try:
			while True:
				tmp = tParser.tEqlt(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.comp()
		except ValueError, IndexError:
			return root
	def lgca(self):
		root = self.eqlt()
		try:
			while True:
				tmp = tParser.tLgcA(self.curr())
				self.idx +=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.eqlt()
		except ValueError, IndexError:
			return root
	def lgco(self):
		root = self.lgca()
		try:
			while True:
				tmp = tParser.tLgcO(self.curr())
				self.idx +=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.lgca()
		except ValueError, IndexError:
			return root
	def expr(self):
		return self.lgco()
	def var(self):
		strt = self.idx
		try:
			ret = tParser.tVar()
			ret.vars.append(self.idnt())
			while self.curr().type == tTokeniser.tLex.eType.COMMA:
				self.idx+=1
				self.trim()
				try:
					ret.vars.append(self.idnt())
				except ValueError:
					print(f'Expected identifier after comma in variable declaration list @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
					print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
					exit(1)
			if self.curr().type == tTokeniser.tLex.eType.COLON:
				self.idx+=1
				try:
					ret.type = self.mtyp()
				except ValueError:
					print(f'Expected colon in variable declaration @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
					print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
					exit(1)
			else: raise ValueError
			if self.curr().type == tTokeniser.tLex.eType.EQ:
				self.idx+=1
				try:
					ret.val = self.expr()
				except ValueError:
					print(f'Expected expresion following assignment operator in variable definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
					print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
					exit(1)
			return ret
		except Exception as e:
			self.idx = strt
			raise e
	def rtrn(self):
		ret = tParser.tRtrn(self.curr())
		self.idx+=1
		ret.child = self.expr()
		return ret
	def brk(self):
		ret = tParser.tBrk(self.curr())
		self.idx += 1
		return ret
	def stmnt(self):
		try: ret = self.var()
		except ValueError:
			try: ret = self.cssgn()
			except ValueError:
				try: ret = self.assgn()
				except ValueError:
					try: ret = self.expr()
					except ValueError:
						try: ret = self.rtrn()
						except ValueError:
							try: ret = self.brk()
							except ValueError:
								try: ret = self.blck()
								except ValueError:
									try: ret = self.cnd()
									except ValueError:
										try: ret = self.loop()
										except ValueError: return None
		return ret
	def stlst(self):
		ret = tParser.tStLst()
		try:
			child = self.stmnt()
			if child is not None: ret.kids.append(child)
		except ValueError: pass
		else:
			try:
				while self.curr().type == tTokeniser.tLex.eType.NEWLINE:
					self.trim()
					child = self.stmnt()
					if child is not None: ret.kids.append(child)
			except IndexError: pass
		return ret
	def blck(self):
		ret = tParser.tBlck(self.curr())
		self.idx+=1
		self.trim()
		ret.child = self.stlst()
		self.trim()
		ret.fnsh(self.curr())
		self.idx+=1
		return ret # I might change this to just return `ret.child`, depending on the later steps.
	def cndbdy(self):
		self.trim()
		try:
			ret = self.blck()
		except ValueError:
			ret = self.stmnt()
		return ret
	def cnd(self):
		ret = tParser.tCnd(self.curr())
		if ret.type != tParser.tCnd.eType.IF:
			print(f'ERR: `elif` and `else` are not permitted before encountering `if` @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.idx+=1
		ret.cnd = self.expr()
		retBdy = self.cndbdy()
		if retBdy is None:
			print(f'ERR: Expected body following `if` conditional @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		ret.bdy = retBdy
		self.trim()
		while self.curr().type == tTokeniser.tLex.eType.KWELIF:
			self.trim()
			child = tParser.tCnd(self.curr())
			self.idx+=1
			child.cnd = self.expr()
			childBdy = self.cndbdy()
			if childBdy is None:
				print(f'ERR: Expected body following `elif` conditional @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
			child.bdy = childBdy
			ret.elifs.append(child)
		self.trim()
		if self.curr().type == tTokeniser.tLex.eType.KWELSE:
			self.idx+=1
			elseBdy = self.cndbdy()
			if elseBdy is None:
				print(f'ERR: Expected body following `else` conditional @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
			ret.elseBdy = elseBdy
		return ret
	def loop(self):
		ret = tParser.tLoop(self.curr())
		self.idx+=1
		ret.cnd = self.expr()
		retBdy = self.cndbdy()
		if retBdy is None:
			print(f'ERR: Expected body following `while` loop @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		ret.bdy = retBdy
		self.trim()
		if self.curr().type == tTokeniser.tLex.eType.KWELSE:
			self.idx+=1
			elseBdy = self.cndbdy()
			if elseBdy is None:
				print(f'ERR: Expected body following `else` conditional @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
			ret.elseBdy = elseBdy
		return ret
	def assgn(self):
		idx = self.idx
		retLhs = self.unry()
		try:
			ret = tParser.tAssgn(self.curr())
		except (ValueError, IndexError) as exp:
			self.idx = idx
			raise exp
		self.idx+=1
		ret.lhs = retLhs
		try:
			ret.rhs = self.assgn()
		except ValueError:
			try: ret.rhs = self.expr()
			except:
				print(f'ERR: Unexpected lexeme encountered following assignment @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
		return ret
	def cssgn(self):
		idx = self.idx
		retLhs = self.unry()
		try:
			ret = tParser.tCssgn(self.curr())
		except (ValueError, IndexError) as exp:
			self.idx = idx
			raise exp
		self.idx+=1
		ret.lhs = retLhs
		try:
			ret.rhs = self.assgn()
		except ValueError:
			try: ret.rhs = self.expr()
			except:
				print(f'ERR: Unexpected lexeme encountered following compound assignment @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
		return ret
	def prog(self):
		self.trim()
		ret = self.stlst()
		self.trim()
		return ret
	def run(self):
		try:
			self.tree = self.prog()
		except ValueError:
			print(f'ERR: Unexpected lexeme encountered @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		if self.curr().type != tTokeniser.tLex.eType.EOF:
			print(f'ERR: Unhandled lexemes, starting @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
	def print(self):
		if self.tree is not None: self.tree.print()

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
		if parser.tree is None: continue
		parser.print()