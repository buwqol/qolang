#!/bin/python3
import argparse
import sys
import os
import io
import enum
import abc
def doIndnt(indnt: int=0):
	for _ in range(indnt): print('\t',end='')
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
			KWLTR=enum.auto()
			KWWHL=enum.auto()
			KWBRK=enum.auto()
			KWCONT=enum.auto()
			KWOBJ=enum.auto()
			KWUNI=enum.auto()
			KWORD=enum.auto()
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
			TUSZ=enum.auto()
			TSSZ=enum.auto()
			TBLN=enum.auto()
			TNON=enum.auto()
			TPTR=enum.auto()
			TCHR=enum.auto()
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
		self.stck = ''
		self.lxms = []
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
		self.lxms.append(tTokeniser.tLex(type, rawValue, self.fileName, lineNum, colNum, calcInt=calcInt, calcFlt=calcFlt, calcStr=calcStr))
	def num(self):
		lineNum = self.lineNum
		colNum = self.colNum
		self.stck += self.curr
		peekedChar = self.ahd()
		intBase = 10
		if self.curr == '0':
			if peekedChar == 'H' or peekedChar == 'h':
				self.stck += peekedChar
				intBase = 16
				self.nxt()
				peekedChar = self.ahd()
			elif peekedChar == 'O' or peekedChar == 'o':
				self.stck += peekedChar
				intBase = 8
				self.nxt()
				peekedChar = self.ahd()
			elif peekedChar == 'B' or peekedChar == 'b':
				self.stck += peekedChar
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
					self.stck += self.curr
					peekedChar = self.ahd()
				elif exponentMark == True and (peekedChar == '-' or peekedChar == '+'):
					if expSign == True:
						self.nxt()
						print(f'ERR: Unexpected repeated sign in numeric literal exponent @ {self.fileName}:{self.lineNum}:{self.colNum}.')
						exit(1)
					self.nxt()
					self.stck += self.curr
					peekedChar = self.ahd()
					expSign = True
				elif peekedChar == '.':
					if decimalPoint == True:
						self.nxt()
						print(f'ERR: Unexpected repeated decimal point in numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
						exit(1)
					self.nxt()
					self.stck += self.curr
					peekedChar = self.ahd()
					decimalPoint = True
				elif peekedChar == 'E' or peekedChar == 'e':
					if exponentMark == True:
						self.nxt()
						print(f'ERR: Unexpected repeated exponent in numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
						exit(1)
					self.nxt()
					self.stck += self.curr
					peekedChar = self.ahd()
					decimalPoint = True
					exponentMark = True
				elif peekedChar.isalpha():
					self.nxt()
					print(f'ERR: Unexpected character \'{peekedChar}\' in numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else: break
			if decimalPoint == True:
				calcFlt = float(''.join(self.stck.split('_')))
				self.add(tTokeniser.tLex.eType.LITFP, self.stck, lineNum, colNum, calcFlt=calcFlt)
			else:
				calcInt = int(''.join(self.stck.split('_')))
				self.add(tTokeniser.tLex.eType.LITIU, self.stck, lineNum, colNum, calcInt=calcInt)
		elif intBase == 16:
			while True:
				if peekedChar.isnumeric() or peekedChar == '_' or peekedChar in ['A', 'B', 'C', 'D', 'E', 'F', 'a', 'b', 'c', 'd', 'e', 'f']:
					self.nxt()
					self.stck += self.curr
					peekedChar = self.ahd()
				elif peekedChar.isalpha():
					self.nxt()
					print(f'ERR: Unexpected character \'{peekedChar}\' in hexadecimal numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else: break
			calcInt = int(''.join(self.stck[2:].split('_')), intBase)
			self.add(tTokeniser.tLex.eType.LITIU, self.stck, lineNum, colNum, calcInt=calcInt)
		elif intBase == 8:
			while True:
				if peekedChar in [str(idx) for idx in range(0, 8)] or peekedChar == '_':
					self.nxt()
					self.stck += self.curr
					peekedChar = self.ahd()
				elif peekedChar.isalnum():
					self.nxt()
					print(f'ERR: Unexpected character \'{peekedChar}\' in octal numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else: break
			calcInt = int(''.join(self.stck[2:].split('_')), intBase)
			self.add(tTokeniser.tLex.eType.LITIU, self.stck, lineNum, colNum, calcInt=calcInt)
		elif intBase == 2:
			while True:
				if peekedChar == '0' or peekedChar == '1' or peekedChar == '_':
					self.nxt()
					self.stck += self.curr
					peekedChar = self.ahd()
				elif peekedChar.isalnum():
					self.nxt()
					print(f'ERR: Unexpected character \'{peekedChar}\' in binary numeric literal @ {self.fileName}:{self.lineNum}:{self.colNum}.')
					exit(1)
				else: break
			calcInt = int(''.join(self.stck[2:].split('_')), intBase)
			self.add(tTokeniser.tLex.eType.LITIU, self.stck, lineNum, colNum, calcInt=calcInt)
		self.stck = ''
	def ident(self):
		lineNum = self.lineNum
		colNum = self.colNum
		self.stck += self.curr
		peekedChar = self.ahd()
		while peekedChar.isalnum() or peekedChar == '_':
			self.nxt()
			self.stck += self.curr
			peekedChar = self.ahd()
		if self.stck == 'if': self.add(tTokeniser.tLex.eType.KWIF, self.stck, lineNum, colNum)
		elif self.stck == 'elif': self.add(tTokeniser.tLex.eType.KWELIF, self.stck, lineNum, colNum)
		elif self.stck == 'else': self.add(tTokeniser.tLex.eType.KWELSE, self.stck, lineNum, colNum)
		elif self.stck == 'ret': self.add(tTokeniser.tLex.eType.KWRET, self.stck, lineNum, colNum)
		elif self.stck == 'ltr': self.add(tTokeniser.tLex.eType.KWLTR, self.stck, lineNum, colNum)
		elif self.stck == 'whl': self.add(tTokeniser.tLex.eType.KWWHL, self.stck, lineNum, colNum)
		elif self.stck == 'brk': self.add(tTokeniser.tLex.eType.KWBRK, self.stck, lineNum, colNum)
		elif self.stck == 'cont': self.add(tTokeniser.tLex.eType.KWCONT, self.stck, lineNum, colNum)
		elif self.stck == 'obj': self.add(tTokeniser.tLex.eType.KWOBJ, self.stck, lineNum, colNum)
		elif self.stck == 'uni': self.add(tTokeniser.tLex.eType.KWUNI, self.stck, lineNum, colNum)
		elif self.stck == 'ord': self.add(tTokeniser.tLex.eType.KWORD, self.stck, lineNum, colNum)
		elif self.stck == 'True': self.add(tTokeniser.tLex.eType.LITTRUE, self.stck, lineNum, colNum)
		elif self.stck == 'False': self.add(tTokeniser.tLex.eType.LITFALSE, self.stck, lineNum, colNum)
		elif self.stck == 'Null': self.add(tTokeniser.tLex.eType.LITNULL, self.stck, lineNum, colNum)
		elif self.stck == 'and': self.add(tTokeniser.tLex.eType.KWAND, self.stck, lineNum, colNum)
		elif self.stck == 'or': self.add(tTokeniser.tLex.eType.KWOR, self.stck, lineNum, colNum)
		elif self.stck == 'iu8': self.add(tTokeniser.tLex.eType.TIU8, self.stck, lineNum, colNum)
		elif self.stck == 'is8': self.add(tTokeniser.tLex.eType.TIS8, self.stck, lineNum, colNum)
		elif self.stck == 'iu16': self.add(tTokeniser.tLex.eType.TIU16, self.stck, lineNum, colNum)
		elif self.stck == 'is16': self.add(tTokeniser.tLex.eType.TIS16, self.stck, lineNum, colNum)
		elif self.stck == 'iu32': self.add(tTokeniser.tLex.eType.TIU32, self.stck, lineNum, colNum)
		elif self.stck == 'is32': self.add(tTokeniser.tLex.eType.TIS32, self.stck, lineNum, colNum)
		elif self.stck == 'iu64': self.add(tTokeniser.tLex.eType.TIU64, self.stck, lineNum, colNum)
		elif self.stck == 'is64': self.add(tTokeniser.tLex.eType.TIS64, self.stck, lineNum, colNum)
		elif self.stck == 'fp32': self.add(tTokeniser.tLex.eType.TFP32, self.stck, lineNum, colNum)
		elif self.stck == 'fp64': self.add(tTokeniser.tLex.eType.TFP64, self.stck, lineNum, colNum)
		elif self.stck == 'usz': self.add(tTokeniser.tLex.eType.TUSZ, self.stck, lineNum, colNum)
		elif self.stck == 'ssz': self.add(tTokeniser.tLex.eType.TSSZ, self.stck, lineNum, colNum)
		elif self.stck == 'bln': self.add(tTokeniser.tLex.eType.TBLN, self.stck, lineNum, colNum)
		elif self.stck == 'non': self.add(tTokeniser.tLex.eType.TNON, self.stck, lineNum, colNum)
		elif self.stck == 'chr': self.add(tTokeniser.tLex.eType.TCHR, self.stck, lineNum, colNum)
		# elif self.stck == 'ptr': self.add(tTokeniser.tLex.eType.TPTR, self.stck, lineNum, colNum) # Maybe I'll add this back, I'll see.
		else: self.add(tTokeniser.tLex.eType.IDENT, self.stck, lineNum, colNum)
		self.stck = ''
	def cstr(self):
		lineNum = self.lineNum
		colNum = self.colNum
		self.stck += self.curr
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
				self.stck += self.curr
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
				self.stck += self.curr
			else:
				self.nxt()
				ahdChar = self.ahd()
				self.stck += self.curr
				calcStr.append(ord(self.curr))
		self.nxt()
		self.stck += self.curr
		calcStr.append(0)
		self.add(tTokeniser.tLex.eType.LITSTR, self.stck, lineNum, colNum, calcStr=calcStr)
		self.stck = ''
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
	class xNoMatch(Exception):pass
	class tParserObj(abc.ABC):
		@abc.abstractmethod
		def __init__(self, lxm: tTokeniser.tLex):pass
		@abc.abstractmethod
		def print(self, indnt: int=0):pass
	class tPrim(tParserObj):pass
	class tLit(tPrim):
		class eType(enum.Enum):
			IU=enum.auto()
			FP=enum.auto()
			STR=enum.auto()
			CHR=enum.auto()
			TRUE=enum.auto()
			FALSE=enum.auto()
			NULL=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if lxm.type == tTokeniser.tLex.eType.LITIU: self.type = tParser.tLit.eType.IU
			elif lxm.type == tTokeniser.tLex.eType.LITFP: self.type = tParser.tLit.eType.FP
			elif lxm.type == tTokeniser.tLex.eType.LITSTR: self.type = tParser.tLit.eType.STR
			elif lxm.type == tTokeniser.tLex.eType.LITCHR: self.type = tParser.tLit.eType.CHR
			elif lxm.type == tTokeniser.tLex.eType.LITTRUE: self.type = tParser.tLit.eType.TRUE
			elif lxm.type == tTokeniser.tLex.eType.LITFALSE: self.type = tParser.tLit.eType.FALSE
			elif lxm.type == tTokeniser.tLex.eType.LITNULL: self.type = tParser.tLit.eType.NULL
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tLit.eType.IU: print('(IU) ' + str(self.lxm.calcInt))
			elif self.type == tParser.tLit.eType.FP: print('(FP) ' + str(self.lxm.calcFlt))
			elif self.type == tParser.tLit.eType.STR: print('(STR) ' + self.lxm.calcStr)
			elif self.type == tParser.tLit.eType.CHR: print('(CHR) ' + str(self.lxm.calcInt))
			elif self.type == tParser.tLit.eType.TRUE: print('(TRUE) True')
			elif self.type == tParser.tLit.eType.FALSE: print('(FALSE) False')
			elif self.type == tParser.tLit.eType.NULL: print('(NULL) Null')
	class tIdnt(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if lxm.type != tTokeniser.tLex.eType.IDENT: raise tParser.xNoMatch
			self.rawValue = self.lxm.rawValue
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2], end='')
			print('(' + self.lxm.rawValue + ')')
	class tPstFx(tParserObj):
		class eType(enum.Enum):
			ACS=enum.auto()
			ARR=enum.auto()
			CALL=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj | list | None
			if lxm.type == tTokeniser.tLex.eType.LPAREN: self.type = tParser.tPstFx.eType.CALL
			elif lxm.type == tTokeniser.tLex.eType.LBRACK: self.type = tParser.tPstFx.eType.ARR
			elif lxm.type == tTokeniser.tLex.eType.PERIOD: self.type = tParser.tPstFx.eType.ACS
			else: raise tParser.xNoMatch
		def fnsh(self, lxm: tTokeniser.tLex):
			if self.type == tParser.tPstFx.eType.CALL and lxm.type != tTokeniser.tLex.eType.RPAREN:
				print(f'ERR: Unclosed parentheses during function call, first opened @ {self.lxm.fileName}:{self.lxm.lineNum}:{self.lxm.colNum}.')
				print(f'\tGot {str(lxm.type).rsplit('.', 1)[-1]} \'{lxm.rawValue}\' @ {lxm.fileName}:{lxm.lineNum}:{lxm.colNum}.')
				exit(1)
			elif self.type == tParser.tPstFx.eType.ARR and lxm.type != tTokeniser.tLex.eType.RBRACK:
				print(f'ERR: Unclosed brackets during array accessor, first opened @ {self.lxm.fileName}:{self.lxm.lineNum}:{self.lxm.colNum}.')
				print(f'\tGot {str(lxm.type).rsplit('.', 1)[-1]} \'{lxm.rawValue}\' @ {lxm.fileName}:{lxm.lineNum}:{lxm.colNum}.')
				exit(1)
		def print(self, indnt: int=0):
			doIndnt(indnt)
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
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.chld: tParser.tParserObj
			if lxm.type == tTokeniser.tLex.eType.PLUS: self.type = tParser.tUnry.eType.POS
			elif lxm.type == tTokeniser.tLex.eType.DASH: self.type = tParser.tUnry.eType.NEG
			elif lxm.type == tTokeniser.tLex.eType.EXCLAM: self.type = tParser.tUnry.eType.NOT
			elif lxm.type == tTokeniser.tLex.eType.TIL: self.type = tParser.tUnry.eType.INV
			elif lxm.type == tTokeniser.tLex.eType.CARET: self.type = tParser.tUnry.eType.PTR
			elif lxm.type == tTokeniser.tLex.eType.ATSGN: self.type = tParser.tUnry.eType.AT
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tUnry.eType.POS: print('(+)')
			elif self.type == tParser.tUnry.eType.NEG: print('(-)')
			elif self.type == tParser.tUnry.eType.NOT: print('(!)')
			elif self.type == tParser.tUnry.eType.INV: print('(~)')
			elif self.type == tParser.tUnry.eType.PTR: print('(^)')
			elif self.type == tParser.tUnry.eType.AT: print('(@)')
			self.chld.print(indnt+1)
	class tFact(tParserObj):
		class eType(enum.Enum):
			MUL=enum.auto()
			DIV=enum.auto()
			MOD=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lxm.type == tTokeniser.tLex.eType.ASTR: self.type = tParser.tFact.eType.MUL
			elif lxm.type == tTokeniser.tLex.eType.FSLSH: self.type = tParser.tFact.eType.DIV
			elif lxm.type == tTokeniser.tLex.eType.PRCNT: self.type = tParser.tFact.eType.MOD
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
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
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lxm.type == tTokeniser.tLex.eType.PLUS: self.type = tParser.tTerm.eType.ADD
			elif lxm.type == tTokeniser.tLex.eType.DASH: self.type = tParser.tTerm.eType.SUB
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
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
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lxm.type == tTokeniser.tLex.eType.AMP: self.type = tParser.tBtws.eType.AND
			elif lxm.type == tTokeniser.tLex.eType.PIPE: self.type = tParser.tBtws.eType.OR
			elif lxm.type == tTokeniser.tLex.eType.CARET: self.type = tParser.tBtws.eType.EOR
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
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
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lxm.type == tTokeniser.tLex.eType.LTLT: self.type = tParser.tShft.eType.LSHF
			elif lxm.type == tTokeniser.tLex.eType.GTGT: self.type = tParser.tShft.eType.RSHF
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tShft.eType.LSHF: print('(<<)')
			elif self.type == tParser.tShft.eType.RSHF: print('(>>)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tCmp(tParserObj):
		class eType(enum.Enum):
			LS=enum.auto()
			LSEQ=enum.auto()
			GR=enum.auto()
			GREQ=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lxm.type == tTokeniser.tLex.eType.LT: self.type = tParser.tCmp.eType.LS
			elif lxm.type == tTokeniser.tLex.eType.LTEQ: self.type = tParser.tCmp.eType.LSEQ
			elif lxm.type == tTokeniser.tLex.eType.GT: self.type = tParser.tCmp.eType.GR
			elif lxm.type == tTokeniser.tLex.eType.GTEQ: self.type = tParser.tCmp.eType.GREQ
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tCmp.eType.LS: print('(<)')
			elif self.type == tParser.tCmp.eType.LSEQ: print('(<=)')
			elif self.type == tParser.tCmp.eType.GR: print('(>)')
			elif self.type == tParser.tCmp.eType.GREQ: print('(>=)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tEqlt(tParserObj):
		class eType(enum.Enum):
			EQUL=enum.auto()
			NEQUL=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
			if lxm.type == tTokeniser.tLex.eType.EQEQ: self.type = tParser.tEqlt.eType.EQUL
			elif lxm.type == tTokeniser.tLex.eType.EXCLAMEQ: self.type = tParser.tEqlt.eType.NEQUL
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tEqlt.eType.EQUL: print('(==)')
			elif self.type == tParser.tEqlt.eType.NEQUL: print('(!=)')
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tExpr(tEqlt):pass
	class tRtrn(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.chld: tParser.tParserObj | None = None
			if lxm.type != tTokeniser.tLex.eType.KWRET: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			if self.chld is not None: self.chld.print(indnt+1)
	class tDfer(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.chld: tParser.tParserObj
			if lxm.type != tTokeniser.tLex.eType.KWLTR: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.chld.print(indnt+1)
	class tCntrl(tParserObj):
		class eType(enum.Enum):
			BRK=enum.auto()
			CONT=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if lxm.type == tTokeniser.tLex.eType.KWBRK: self.type = tParser.tCntrl.eType.BRK
			elif lxm.type == tTokeniser.tLex.eType.KWCONT: self.type = tParser.tCntrl.eType.CONT
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2],end='')
			if self.type == tParser.tCntrl.eType.CONT: print('(CONT)')
			elif self.type == tParser.tCntrl.eType.BRK: print('(BRK)')
	class tStLst(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.kids = []
		def print(self, indnt: int=0):
			for idx in range(len(self.kids)): self.kids[idx].print(indnt)
	class tBlck(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if lxm.type != tTokeniser.tLex.eType.LBRACE: raise tParser.xNoMatch
			self.chld: tParser.tStLst
		def fnsh(self, lxm: tTokeniser.tLex):
			if lxm.type != tTokeniser.tLex.eType.RBRACE:
				print(f'ERR: Unclosed brace during block, first opened @ {self.lxm.fileName}:{self.lxm.lineNum}:{self.lxm.colNum}.')
				print(f'\tGot {str(lxm.type).rsplit('.', 1)[-1]} \'{lxm.rawValue}\' @ {lxm.fileName}:{lxm.lineNum}:{lxm.colNum}.')
				exit(1)
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			for idx in range(len(self.chld.kids)): self.chld.kids[idx].print(indnt+1)
	class tCnd(tParserObj):
		class eType(enum.Enum):
			IF=enum.auto()
			ELIF=enum.auto()
			ELSE=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if self.lxm.type == tTokeniser.tLex.eType.KWIF: self.type = tParser.tCnd.eType.IF
			elif self.lxm.type == tTokeniser.tLex.eType.KWELIF: self.type = tParser.tCnd.eType.ELIF
			elif self.lxm.type == tTokeniser.tLex.eType.KWELSE: self.type = tParser.tCnd.eType.ELSE
			else: raise tParser.xNoMatch
			self.cnd: tParser.tParserObj
			self.bdy: tParser.tParserObj
			self.elifs = []
			self.elseBdy: tParser.tParserObj | None = None
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2], end='')
			if self.type == tParser.tCnd.eType.IF:
				print('(IF)')
				self.cnd.print(indnt+1)
				self.bdy.print(indnt+1)
				for idx in range(len(self.elifs)): self.elifs[idx].print(indnt)
				if self.elseBdy is not None:
					doIndnt(indnt)
					print(str(type(self)).split('.')[-1][1:-2], end='')
					print('(ELSE)')
					self.elseBdy.print(indnt+1)
			elif self.type == tParser.tCnd.eType.ELIF:
				doIndnt(indnt)
				print('(ELIF)')
				self.cnd.print(indnt+1)
				self.bdy.print(indnt+1)
	class tLoop(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if self.lxm.type != tTokeniser.tLex.eType.KWWHL: raise tParser.xNoMatch
			self.cnd: tParser.tParserObj
			self.bdy: tParser.tParserObj
			self.elseBdy: tParser.tParserObj | None = None
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2], end='')
			print('(WHILE)')
			self.cnd.print(indnt+1)
			self.bdy.print(indnt+1)
			if self.elseBdy is not None:
				doIndnt(indnt)
				print(str(type(self)).split('.')[-1][1:-2], end='')
				print('(ELSE)')
				self.elseBdy.print(indnt+1)
	class tAssgn(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if self.lxm.type != tTokeniser.tLex.eType.EQ: raise tParser.xNoMatch
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
		def print(self, indnt: int=0):
			doIndnt(indnt)
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
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if self.lxm.type == tTokeniser.tLex.eType.PLUSEQ: self.type = tParser.tCssgn.eType.ADD
			elif self.lxm.type == tTokeniser.tLex.eType.DASHEQ: self.type = tParser.tCssgn.eType.SUB
			elif self.lxm.type == tTokeniser.tLex.eType.ASTREQ: self.type = tParser.tCssgn.eType.MUL
			elif self.lxm.type == tTokeniser.tLex.eType.FSLSHEQ: self.type = tParser.tCssgn.eType.DIV
			elif self.lxm.type == tTokeniser.tLex.eType.AMPEQ: self.type = tParser.tCssgn.eType.AND
			elif self.lxm.type == tTokeniser.tLex.eType.PIPEEQ: self.type = tParser.tCssgn.eType.OR
			elif self.lxm.type == tTokeniser.tLex.eType.CARETEQ: self.type = tParser.tCssgn.eType.EOR
			elif self.lxm.type == tTokeniser.tLex.eType.PRCNTEQ: self.type = tParser.tCssgn.eType.MOD
			elif self.lxm.type == tTokeniser.tLex.eType.TILEQ: self.type = tParser.tCssgn.eType.NOT
			else: raise tParser.xNoMatch
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
		def print(self, indnt: int=0):
			doIndnt(indnt)
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
			USR=enum.auto()
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
			USZ=enum.auto()
			SSZ=enum.auto()
			BLN=enum.auto()
			NON=enum.auto()
			# PTR=enum.auto()
			CHR=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if self.lxm.type == tTokeniser.tLex.eType.IDENT: self.type = tParser.tTyp.eType.USR
			elif self.lxm.type == tTokeniser.tLex.eType.TIU8: self.type = tParser.tTyp.eType.IU8
			elif self.lxm.type == tTokeniser.tLex.eType.TIS8: self.type = tParser.tTyp.eType.IS8
			elif self.lxm.type == tTokeniser.tLex.eType.TIU16: self.type = tParser.tTyp.eType.IU16
			elif self.lxm.type == tTokeniser.tLex.eType.TIS16: self.type = tParser.tTyp.eType.IS16
			elif self.lxm.type == tTokeniser.tLex.eType.TIU32: self.type = tParser.tTyp.eType.IU32
			elif self.lxm.type == tTokeniser.tLex.eType.TIS32: self.type = tParser.tTyp.eType.IS32
			elif self.lxm.type == tTokeniser.tLex.eType.TIU64: self.type = tParser.tTyp.eType.IU64
			elif self.lxm.type == tTokeniser.tLex.eType.TIS64: self.type = tParser.tTyp.eType.IS64
			elif self.lxm.type == tTokeniser.tLex.eType.TFP32: self.type = tParser.tTyp.eType.FP32
			elif self.lxm.type == tTokeniser.tLex.eType.TFP64: self.type = tParser.tTyp.eType.FP64
			elif self.lxm.type == tTokeniser.tLex.eType.TUSZ: self.type = tParser.tTyp.eType.USZ
			elif self.lxm.type == tTokeniser.tLex.eType.TSSZ: self.type = tParser.tTyp.eType.SSZ
			elif self.lxm.type == tTokeniser.tLex.eType.TBLN: self.type = tParser.tTyp.eType.BLN
			elif self.lxm.type == tTokeniser.tLex.eType.TNON: self.type = tParser.tTyp.eType.NON
			# elif self.lxm.type == tTokeniser.tLex.eType.TPTR: self.type = tParser.tTyp.eType.PTR #TODO: Maybe reintroduce this as `uintptr` equivalent.
			elif self.lxm.type == tTokeniser.tLex.eType.TCHR: self.type = tParser.tTyp.eType.CHR
			else: raise tParser.xNoMatch
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2],end='')
			print(f'({self.type.name})')
	class tMTyp(tParserObj):
		class eType(enum.Enum):
			ARR=enum.auto()
			PTR=enum.auto()
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.chld: tParser.tTyp | tParser.tMTyp | tParser.tFTyp
			if self.lxm.type == tTokeniser.tLex.eType.LBRACK:
				self.type = tParser.tMTyp.eType.ARR
				self.arrSz: tParser.tParserObj
			elif self.lxm.type == tTokeniser.tLex.eType.CARET: self.type = tParser.tMTyp.eType.PTR
			else: raise tParser.xNoMatch
		def fnsh(self, lxm: tTokeniser.tLex):
			if self.type == tParser.tMTyp.eType.ARR and lxm.type != tTokeniser.tLex.eType.RBRACK:
				print(f'ERR: Unclosed square bracket started @ {self.lxm.fileName, self.lxm.lineNum, self.lxm.colNum}.')
				print(f'\tGot {str(lxm.type).rsplit('.', 1)[-1]} \'{lxm.rawValue}\' @ {lxm.fileName}:{lxm.lineNum}:{lxm.colNum}.')
				exit(1)
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2],end='')
			if self.type == tParser.tMTyp.eType.ARR:
				print('([])')
				self.arrSz.print(indnt)
			else: print('(^)')
			self.chld.print(indnt+1)
	class tFTyp(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.type: tParser.tParserObj
			self.args = []
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.type.print(indnt+1)
			for arg in self.args: arg.print(indnt+1)
	class tCst(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if (self.lxm.type != tTokeniser.tLex.eType.COLON): raise tParser.xNoMatch
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tTyp | tParser.tMTyp | tParser.tFTyp
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tLgcA(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if (self.lxm.type != tTokeniser.tLex.eType.KWAND): raise tParser.xNoMatch
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tLgcO(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if (self.lxm.type != tTokeniser.tLex.eType.KWOR): raise tParser.xNoMatch
			self.lhs: tParser.tParserObj
			self.rhs: tParser.tParserObj
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.lhs.print(indnt+1)
			self.rhs.print(indnt+1)
	class tVar(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.vars = []
			self.type: tParser.tParserObj | None = None
			self.val: tParser.tParserObj | None = None
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			for var in self.vars: var.print(indnt+1)
			if self.type is not None: self.type.print(indnt+1)
			if self.val is not None: self.val.print(indnt+1)
	class tFnc(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.idnt: tParser.tIdnt
			self.args = []
			self.type: tParser.tParserObj
			self.bdy: tParser.tBlck | None = None
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.idnt.print(indnt+1)
			for arg in self.args: arg.print(indnt+1)
			self.type.print(indnt+1)
			if self.bdy is not None: self.bdy.print(indnt+1)
	class tArg(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.idnt: tParser.tIdnt
			self.type: tParser.tParserObj
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.idnt.print(indnt+1)
			self.type.print(indnt+1)
	class tDObjA(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.type: tParser.tParserObj
			self.idnts = []
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			for idnt in self.idnts: idnt.print(indnt+1)
			self.type.print(indnt+1)
	class tDObj(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if self.lxm.type != tTokeniser.tLex.eType.KWOBJ: raise tParser.xNoMatch
			self.idnt: tParser.tParserObj
			self.flds = []
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.idnt.print(indnt+1)
			for fld in self.flds: fld.print(indnt+1)
	class tDUniA(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.type: tParser.tParserObj
			self.idnt: tParser.tParserObj
			self.type: tParser.tParserObj
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.idnt.print(indnt+1)
			self.type.print(indnt+1)
	class tDUni(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if self.lxm.type != tTokeniser.tLex.eType.KWUNI: raise tParser.xNoMatch
			self.idnt: tParser.tParserObj
			self.flds = []
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.idnt.print(indnt+1)
			for fld in self.flds: fld.print(indnt+1)
	class tDOrdA(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			self.idnt: tParser.tParserObj
			self.val: tParser.tParserObj | None = None
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.idnt.print(indnt+1)
			if self.val is not None: self.val.print(indnt+1)
	class tDOrd(tParserObj):
		def __init__(self, lxm: tTokeniser.tLex):
			self.lxm = lxm
			if self.lxm.type != tTokeniser.tLex.eType.KWORD: raise tParser.xNoMatch
			self.idnt: tParser.tParserObj
			self.flds = []
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2])
			self.idnt.print(indnt+1)
			for fld in self.flds: fld.print(indnt+1)
	def __init__(self):
		self.idx = 0
		self.lxms = []
		self.tree: tParser.tParserObj | None = None
	def lex(self, fileName):
		t = tTokeniser(fileName)
		t.strt()
		self.lxms = t.lxms.copy()
	def curr(self) -> tTokeniser.tLex:
		return self.lxms[self.idx]
	def trim(self):
		while self.idx < len(self.lxms) and self.curr().type == tTokeniser.tLex.eType.NEWLINE: self.idx+=1
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
				try: ret.arrSz = self.expr()
				except tParser.xNoMatch:
					print(f'ERR: Expected expression within array type @ {self.curr().fileName, self.curr().lineNum, self.curr().colNum}.')
					print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
					exit(1)
				ret.fnsh(self.curr())
				self.idx+=1
			ret.chld = self.mtyp()
		except tParser.xNoMatch:
			try: ret = self.ftyp()
			except tParser.xNoMatch: ret = self.typ()
		return ret
	def ftyp(self):
		startLine = self.curr().lineNum
		startCol = self.curr().colNum
		if self.curr().type != tTokeniser.tLex.eType.LPAREN: raise tParser.xNoMatch
		ret = tParser.tFTyp(self.curr())
		self.idx+=1
		try:
			ret.args.append(self.mtyp())
		except self.xNoMatch:pass
		else:
			while self.curr().type == tTokeniser.tLex.eType.COMMA:
				self.idx+=1
				try: ret.args.append(self.mtyp())
				except tParser.xNoMatch:
					print(f'ERR: Invalid argument type during function pointer @ {self.curr().fileName, startLine, startCol}.')
					print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\' @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
					exit(1)
		if self.curr().type != tTokeniser.tLex.eType.RPAREN:
			print(f'ERR: Unclosed parenthesis started during function pointer @ {self.curr().fileName, startLine, startCol}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\' @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			exit(1)
		self.idx+=1
		if self.curr().type != tTokeniser.tLex.eType.COLON:
			print(f'ERR: Expected colon for function pointer return type @ {self.curr().fileName, startLine, startCol}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\' @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			exit(1)
		self.idx+=1
		try: ret.type = self.mtyp()
		except tParser.xNoMatch:
			print(f'ERR: Invalid return type during function pointer @ {self.curr().fileName, startLine, startCol}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\' @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			exit(1)
		return ret
	def grpng(self):
		startLine = self.curr().lineNum
		startCol = self.curr().colNum
		if self.curr().type != tTokeniser.tLex.eType.LPAREN: raise tParser.xNoMatch
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
		try: ret.rhs = self.mtyp()
		except tParser.xNoMatch:
			print(f'ERR: Expected type name after cast @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		return ret
	def prim(self):
		try: ret = self.grpng()
		except tParser.xNoMatch:
			try: ret = self.idnt()
			except tParser.xNoMatch: ret = self.lit()
		try:
			cst = self.cst()
			cst.lhs = ret
		except tParser.xNoMatch: return ret
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
						try: root.rhs.append(self.expr())
						except tParser.xNoMatch:pass
					root.fnsh(self.curr())
					self.idx+=1
				elif root.type == tParser.tPstFx.eType.ARR:
					root.rhs = self.expr()
					root.fnsh(self.curr())
					self.idx+=1
				else: root.rhs = self.idnt()
		except tParser.xNoMatch: return root
	def unry(self):
		try: ret = tParser.tUnry(self.curr())
		except tParser.xNoMatch: return self.pstfx()
		else:
			self.idx+=1
			ret.chld = self.unry()
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
		except tParser.xNoMatch: return root
	def term(self):
		root = self.fact()
		try:
			while True:
				tmp = tParser.tTerm(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.fact()
		except tParser.xNoMatch: return root
	def btws(self):
		root = self.term()
		try:
			while True:
				tmp = tParser.tBtws(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.term()
		except tParser.xNoMatch: return root
	def shft(self):
		root = self.btws()
		try:
			while True:
				tmp = tParser.tShft(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.btws()
		except tParser.xNoMatch: return root
	def cmp(self):
		root = self.shft()
		try:
			while True:
				tmp = tParser.tCmp(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.shft()
		except tParser.xNoMatch: return root
	def eqlt(self):
		root = self.cmp()
		try:
			while True:
				tmp = tParser.tEqlt(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.cmp()
		except tParser.xNoMatch: return root
	def lgca(self):
		root = self.eqlt()
		try:
			while True:
				tmp = tParser.tLgcA(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.eqlt()
		except tParser.xNoMatch: return root
	def lgco(self):
		root = self.lgca()
		try:
			while True:
				tmp = tParser.tLgcO(self.curr())
				self.idx+=1
				tmp.lhs = root
				root = tmp
				root.rhs = self.lgca()
		except tParser.xNoMatch: return root
	def expr(self):
		return self.lgco()
	def var(self):
		strt = self.idx
		try:
			ret = tParser.tVar(self.curr())
			ret.vars.append(self.idnt())
			while self.curr().type == tTokeniser.tLex.eType.COMMA:
				self.idx+=1
				self.trim()
				try: ret.vars.append(self.idnt())
				except tParser.xNoMatch:
					print(f'Expected identifier after comma in variable declaration list @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
					print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
					exit(1)
			if self.curr().type == tTokeniser.tLex.eType.COLON:
				self.idx+=1
				if self.curr().type == tTokeniser.tLex.eType.EQ: ret.type = None
				else:
					try: ret.type = self.mtyp()
					except tParser.xNoMatch:
						print(f'ERR: Expected colon in variable declaration @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
						print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
						exit(1)
			else: raise tParser.xNoMatch
			if self.curr().type == tTokeniser.tLex.eType.EQ:
				self.idx+=1
				try: ret.val = self.expr()
				except tParser.xNoMatch:
					print(f'ERR: Expected expresion following assignment operator in variable definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
					print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
					exit(1)
			return ret
		except tParser.xNoMatch:
			self.idx = strt
			raise tParser.xNoMatch
	def arg(self):
		ret = tParser.tArg(self.curr())
		ret.idnt = self.idnt()
		if self.curr().type != tTokeniser.tLex.eType.COLON:
			print(f'ERR: Expected colon in argument for function argument definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.idx+=1
		try: ret.type = self.mtyp()
		except tParser.xNoMatch:
			print(f'ERR: Invalid argument type in function definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		return ret
	def fnc(self):
		strt = self.idx
		try:
			ret = tParser.tFnc(self.curr())
			ret.idnt = self.idnt()
			if self.curr().type != tTokeniser.tLex.eType.LPAREN: raise tParser.xNoMatch
			self.idx+=1
			self.trim()
			try:
				ret.args.append(self.arg())
				while self.curr().type == tTokeniser.tLex.eType.COMMA:
					self.idx+=1
					self.trim()
					try: ret.args.append(self.arg())
					except tParser.xNoMatch:
						print(f'ERR: Invalid identifier for argument name in function definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
						print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
						exit(1)
			except tParser.xNoMatch:pass
			if self.curr().type != tTokeniser.tLex.eType.RPAREN:
				print(f'ERR: Expected closing parenthesis during function definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
			self.idx+=1
			if self.curr().type != tTokeniser.tLex.eType.COLON:
				print(f'ERR: Expected colon for function return type in function definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
			self.idx+=1
			try: ret.type = self.mtyp()
			except tParser.xNoMatch:
				print(f'ERR: Invalid type for function return type in function definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
			self.trim() #TODO: Rollback trim if we don't get a function body
			try: ret.bdy = self.blck()
			except tParser.xNoMatch: ret.bdy = None
			return ret
		except tParser.xNoMatch:
			self.idx = strt
			raise tParser.xNoMatch
	def rtrn(self):
		ret = tParser.tRtrn(self.curr())
		self.idx+=1
		try: ret.chld = self.expr()
		except tParser.xNoMatch: ret.chld = None
		return ret
	def dfer(self):
		ret = tParser.tDfer(self.curr())
		self.idx+=1
		try: ret.chld = self.cssgn()
		except tParser.xNoMatch:
			try: ret.chld = self.assgn()
			except tParser.xNoMatch: ret.chld = self.expr()
		return ret
	def cntrl(self):
		ret = tParser.tCntrl(self.curr())
		self.idx+=1
		return ret
	def dobja(self):
		ret = tParser.tDObjA(self.curr())
		ret.idnts.append(self.idnt()) #TODO: Make the identifiers optional for defined types for `obj` 'inheritance' and unnamed `uni`.
		while self.curr().type == tTokeniser.tLex.eType.COMMA:
			self.idx+=1
			self.trim()
			ret.idnts.append(self.idnt())
		if self.curr().type != tTokeniser.tLex.eType.COLON:
			print(f'ERR: Expected colon before type for object field definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.idx+=1
		try: ret.type = self.mtyp()
		except tParser.xNoMatch:
			print(f'ERR: Expected type name for object field definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		return ret
	def dobj(self):
		ret = tParser.tDObj(self.curr())
		self.idx+=1
		try: ret.idnt = self.idnt()
		except tParser.xNoMatch:
			print(f'ERR: Expected identifier name for object definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.trim()
		if self.curr().type != tTokeniser.tLex.eType.LBRACE: return ret
		self.idx+=1
		self.trim()
		try: ret.flds.append(self.dobja())
		except tParser.xNoMatch:
			print(f'ERR: Expected identifier name for object field definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		while self.curr().type == tTokeniser.tLex.eType.NEWLINE:
			self.trim()
			try: ret.flds.append(self.dobja())
			except tParser.xNoMatch: break
		self.trim()
		if self.curr().type != tTokeniser.tLex.eType.RBRACE:
			print(f'ERR: Expected closing brace for object definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.idx+=1
		return ret
	def dunia(self):
		ret = tParser.tDUniA(self.curr())
		ret.idnt = self.idnt()
		if self.curr().type != tTokeniser.tLex.eType.COLON:
			print(f'ERR: Expected colon before type for union field definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.idx+=1
		try: ret.type = self.mtyp()
		except tParser.xNoMatch:
			print(f'ERR: Expected type name for union field definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		return ret
	def duni(self):
		ret = tParser.tDUni(self.curr())
		self.idx+=1
		try: ret.idnt = self.idnt()
		except tParser.xNoMatch:
			print(f'ERR: Expected identifier name for union definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.trim()
		if self.curr().type != tTokeniser.tLex.eType.LBRACE: return ret
		self.idx+=1
		self.trim()
		try: ret.flds.append(self.dobja())
		except tParser.xNoMatch:
			print(f'ERR: Expected identifier name for union field definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		while self.curr().type == tTokeniser.tLex.eType.NEWLINE:
			self.trim()
			try: ret.flds.append(self.dobja())
			except tParser.xNoMatch: break
		self.trim()
		if self.curr().type != tTokeniser.tLex.eType.RBRACE:
			print(f'ERR: Expected closing brace for union definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.idx+=1
		return ret
	def dorda(self):
		ret = tParser.tDOrdA(self.curr())
		ret.idnt = self.idnt()
		if self.curr().type == tTokeniser.tLex.eType.EQ:
			self.idx+=1
			try: ret.val = self.expr()
			except tParser.xNoMatch:
				print(f'ERR: Expected expression for enumeration value @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
		return ret
	def dord(self):
		ret = tParser.tDOrd(self.curr())
		self.idx+=1
		try: ret.idnt = self.idnt()
		except tParser.xNoMatch:
			print(f'ERR: Expected identifier for enumeration name @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.trim()
		if self.curr().type != tTokeniser.tLex.eType.LBRACE: return ret
		self.idx+=1
		self.trim()
		try: ret.flds.append(self.dorda())
		except tParser.xNoMatch:
			print(f'ERR: Expected identifier name for enumeration field definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		while self.curr().type == tTokeniser.tLex.eType.NEWLINE:
			self.trim()
			try: ret.flds.append(self.dorda())
			except tParser.xNoMatch: break
		self.trim()
		if self.curr().type != tTokeniser.tLex.eType.RBRACE:
			print(f'ERR: Expected closing brace for enumeration definition @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		self.idx+=1
		return ret
	def stmnt(self):
		mtchs = [
			self.var,
			self.cssgn,
			self.assgn,
			self.expr,
			self.dfer,
			self.rtrn,
			self.cntrl,
			self.blck,
			self.cnd,
			self.loop
		]
		for mtch in mtchs:
			try: ret = mtch()
			except tParser.xNoMatch: continue
			else: return ret
		return None
	def stlst(self):
		ret = tParser.tStLst(self.curr())
		try:
			chld = self.stmnt()
			if chld is not None: ret.kids.append(chld)
		except tParser.xNoMatch:pass
		else:
			while self.curr().type == tTokeniser.tLex.eType.NEWLINE:
				self.trim()
				chld = self.stmnt()
				if chld is not None: ret.kids.append(chld)
		return ret
	def blck(self):
		ret = tParser.tBlck(self.curr())
		self.idx+=1
		self.trim()
		ret.chld = self.stlst()
		self.trim()
		ret.fnsh(self.curr())
		self.idx+=1
		return ret #TODO: I might change this to just return `ret.chld`, depending on the later steps.
	def cndbdy(self):
		self.trim()
		try: ret = self.blck()
		except tParser.xNoMatch: ret = self.stmnt()
		return ret
	def cnd(self):
		ret = tParser.tCnd(self.curr())
		if ret.type != tParser.tCnd.eType.IF:
			print(f'ERR: `elif` and `else` are not permitted before encountering an `if` @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
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
			chld = tParser.tCnd(self.curr())
			self.idx+=1
			chld.cnd = self.expr()
			chldBdy = self.cndbdy()
			if chldBdy is None:
				print(f'ERR: Expected body following `elif` conditional @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
			chld.bdy = chldBdy
			ret.elifs.append(chld)
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
		try: ret = tParser.tAssgn(self.curr())
		except tParser.xNoMatch:
			self.idx = idx
			raise tParser.xNoMatch
		self.idx+=1
		ret.lhs = retLhs
		try: ret.rhs = self.assgn()
		except tParser.xNoMatch:
			try: ret.rhs = self.expr()
			except tParser.xNoMatch:
				print(f'ERR: Unexpected lexeme encountered following assignment @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
		return ret
	def cssgn(self):
		idx = self.idx
		retLhs = self.unry()
		try: ret = tParser.tCssgn(self.curr())
		except tParser.xNoMatch:
			self.idx = idx
			raise tParser.xNoMatch
		self.idx+=1
		ret.lhs = retLhs
		try: ret.rhs = self.assgn()
		except tParser.xNoMatch:
			try: ret.rhs = self.expr()
			except tParser.xNoMatch:
				print(f'ERR: Unexpected lxm encountered following compound assignment @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
		return ret
	def prog(self):
		self.trim()
		ret = []
		while True:
			if self.curr().type == tTokeniser.tLex.eType.EOF: break
			try: ret.append(self.fnc())
			except tParser.xNoMatch:
				try: ret.append(self.var())
				except tParser.xNoMatch:
					try: ret.append(self.dobj())
					except tParser.xNoMatch:
						try: ret.append(self.duni())
						except tParser.xNoMatch: ret.append(self.dord())
			if self.curr().type == tTokeniser.tLex.eType.EOF: break
			if self.curr().type != tTokeniser.tLex.eType.NEWLINE:
				print(f'ERR: Expected newline @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
				print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
				exit(1)
			self.trim()
		return ret
	def run(self):
		try: self.brnchs = self.prog()
		except tParser.xNoMatch:
			print(f'ERR: Unexpected lexeme encountered @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
		if self.curr().type != tTokeniser.tLex.eType.EOF:
			print(f'ERR: Unhandled lexemes, starting @ {self.curr().fileName}:{self.curr().lineNum}:{self.curr().colNum}.')
			print(f'\tGot {str(self.curr().type).rsplit('.', 1)[-1]} \'{self.curr().rawValue}\'.')
			exit(1)
	def print(self):
		for brnch in self.brnchs: brnch.print()

class tScop(object):
	class tType(object):
		class eType(enum.Enum):
			UNI=enum.auto()
			OBJ=enum.auto()
			ORD=enum.auto()
		def __init__(self):
			self.type: tScop.tType.eType | None = None
			self.decled = False
			self.defed = False
	class tFnc(object):
		def __init__(self):
			self.decled = False
			self.defed = False
			self.lxm: tTokeniser.tLex | None = None
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2],end='')
			print(f', decled: {self.decled}, defed: {self.defed}')
	class tVar(object):
		def __init__(self):
			self.decled = False
			self.defed = False
			self.lxm: tTokeniser.tLex | None = None
		def print(self, indnt: int=0):
			doIndnt(indnt)
			print(str(type(self)).split('.')[-1][1:-2],end='')
			print(f', decled: {self.decled}, defed: {self.defed}')
	def __init__(self, isGlbl: bool=False):
		self.vars = {}
		self.typs = {}
		self.isGlbl = isGlbl
		self.kids = []
		self.prnt: tScop | None = None
		self.idnt = ''
	def print(self, indnt: int=0):
		for k in self.vars:
			doIndnt(indnt)
			print(f'{k} -> ', end='')
			self.vars[k].print()
		for kid in self.kids:
			doIndnt(indnt)
			print(kid.idnt + ':')
			kid.print(indnt+1)
	def parse(self, brnchs: list):
		for elem in brnchs:
			if isinstance(elem, tParser.tFnc):
				if self.isGlbl == False:
					print(f'ERR: Function definitions are forbidden everywhere except in global scope @ {elem.lxm.fileName}:{elem.lxm.lineNum}:{elem.lxm.colNum}.')
					exit(1)
				fnc = tScop.tFnc()
				fnc.decled = True
				if elem.bdy is not None:
					if elem.idnt.rawValue in self.vars and self.vars[elem.idnt.rawValue].defed == True:
						print(f'ERR: Redefinition of function \'{elem.idnt.rawValue}\' @ {elem.lxm.fileName}:{elem.lxm.lineNum}:{elem.lxm.colNum}.')
						print(f'\tFirst defined @ {self.vars[elem.idnt.rawValue].lxm.fileName}:{self.vars[elem.idnt.rawValue].lxm.lineNum}:{self.vars[elem.idnt.rawValue].lxm.colNum}.')
						exit(1)
					fnc.defed = True
					kid = tScop()
					kid.idnt = elem.idnt.rawValue
					for arg in elem.args:
						var = tScop.tVar()
						var.decled = True
						var.defed = True
						kid.vars[arg.idnt.rawValue] = var
					kid.parse(elem.bdy.chld.kids)
					kid.prnt = self
					self.kids.append(kid)
				fnc.lxm = elem.lxm
				self.vars[elem.idnt.rawValue] = fnc
			elif isinstance(elem, tParser.tVar):
				for idnt in elem.vars:
					var = tScop.tVar()
					var.decled = True
					if elem.val is not None: var.defed = True
					if idnt.rawValue in self.vars:
						if var.defed == True and self.vars[idnt.rawValue].defed == True:
							print(f'ERR: Redefinition of variable \'{idnt.rawValue}\' @ {idnt.lxm.fileName}:{idnt.lxm.lineNum}:{idnt.lxm.colNum}.')
							print(f'\tFirst defined @ {self.vars[idnt.rawValue].lxm.fileName}:{self.vars[idnt.rawValue].lxm.lineNum}:{self.vars[idnt.rawValue].lxm.colNum}.')
							exit(1)
					var.lxm = idnt.lxm
					self.vars[idnt.rawValue] = var
			elif isinstance(elem, tParser.tBlck):
				kid = tScop()
				kid.parse(elem.chld.kids)
				kid.prnt = self
				self.kids.append(kid)
			else:
				print(f'ERR: Unexpected @ {elem.lxm.fileName}:{elem.lxm.lineNum}:{elem.lxm.colNum}.')
				exit(1)

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
		print('--- TOKENISER ---')
		for lxm in parser.lxms: print(lxm)
		parser.run()
		print('\n--- SYNTAX PARSER ---')
		parser.print()
		glbl = tScop(True)
		glbl.idnt = 'GLBL'
		glbl.parse(parser.brnchs)
		print('\n--- SEMANTIC PARSER ---')
		glbl.print()