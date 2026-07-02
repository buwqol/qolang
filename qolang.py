#!/bin/python3
import argparse
import sys
import os
import io
import enum

class tLexeme(object):
	class eType(enum.Enum):
		IDENT=enum.auto()
		COLON=enum.auto()
		LPAREN=enum.auto()
		RPAREN=enum.auto()
		COMMA=enum.auto()
		ASSIGN=enum.auto()
		EQUIV=enum.auto()
		LBRACE=enum.auto()
		RBRACE=enum.auto()
		GT=enum.auto()
		LT=enum.auto()
		GTEQ=enum.auto()
		LTEQ=enum.auto()
		LEFTSH=enum.auto()
		RIGHTSH=enum.auto()
		LEFTSHEQ=enum.auto()
		RIGHTSHEQ=enum.auto()
		PLUS=enum.auto()
		MINUS=enum.auto()
		ASTERISK=enum.auto()
		FSLASH=enum.auto()
		PLUSEQ=enum.auto()
		MINUSEQ=enum.auto()
		ASTERISKEQ=enum.auto()
		FSLASHEQ=enum.auto()
		PERCENT=enum.auto()
		PERCENTEQ=enum.auto()
		CARET=enum.auto()
		CARETEQ=enum.auto()
		AND=enum.auto()
		OR=enum.auto()
		XOR=enum.auto()
		NOT=enum.auto()
		ANDEQ=enum.auto()
		OREQ=enum.auto()
		XOREQ=enum.auto()
		NOTEQ=enum.auto()

		KWIF=enum.auto()
		KWELSE=enum.auto()
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

		LITIU=enum.auto()
		LITFP=enum.auto()
		LITCSTR=enum.auto()
		LITCHR=enum.auto()

	def __init__(self, lexemeType, rawValue, lineNum, colNum, calcInt=0, calcFlt=0.0):
		self.lexemeType = lexemeType
		self.rawValue = rawValue
		self.lineNum = lineNum
		self.colNum = colNum
		self.calcInt = calcInt
		self.calcFlt = calcFlt
	def __repr__(self):
		return f'(@{self.lineNum},{self.colNum}) {str(self.lexemeType)[6:]}: \'{self.rawValue}\' {self.calcInt}/{self.calcFlt}'

class tTokeniser(object):
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
	def add(self, lexemeType, rawValue='', lineNum=-1, colNum=-1, calcInt=0, calcFlt=0.0):
		if lineNum == -1: lineNum = self.lineNum
		if colNum == -1: colNum = self.colNum
		if rawValue == '': rawValue = self.curr
		lexeme = tLexeme(lexemeType, rawValue, lineNum, colNum)
		lexeme.calcInt = calcInt
		lexeme.calcFlt = calcFlt
		self.lexemes.append(lexeme)
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
				self.add(tLexeme.eType.LITFP, self.stack, lineNum, colNum, calcFlt=calcFlt)
				LITCSTR=enum.auto()
			else:
				calcInt = int(''.join(self.stack.split('_')))
				self.add(tLexeme.eType.LITIU, self.stack, lineNum, colNum, calcInt=calcInt)
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
			self.add(tLexeme.eType.LITIU, self.stack, lineNum, colNum, calcInt=calcInt)
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
			self.add(tLexeme.eType.LITIU, self.stack, lineNum, colNum, calcInt=calcInt)
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
			self.add(tLexeme.eType.LITIU, self.stack, lineNum, colNum, calcInt=calcInt)
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
		if self.stack == 'if': self.add(tLexeme.eType.KWIF, self.stack, lineNum, colNum)
		elif self.stack == 'else': self.add(tLexeme.eType.KWELSE, self.stack, lineNum, colNum)
		elif self.stack == 'ret': self.add(tLexeme.eType.KWRET, self.stack, lineNum, colNum)
		elif self.stack == 'while': self.add(tLexeme.eType.KWWHILE, self.stack, lineNum, colNum)
		elif self.stack == 'tIU8': self.add(tLexeme.eType.TYPEIU8, self.stack, lineNum, colNum)
		elif self.stack == 'tIS8': self.add(tLexeme.eType.TYPEIS8, self.stack, lineNum, colNum)
		elif self.stack == 'tIU16': self.add(tLexeme.eType.TYPEIU16, self.stack, lineNum, colNum)
		elif self.stack == 'tIS16': self.add(tLexeme.eType.TYPEIS16, self.stack, lineNum, colNum)
		elif self.stack == 'tIU32': self.add(tLexeme.eType.TYPEIU32, self.stack, lineNum, colNum)
		elif self.stack == 'tIS32': self.add(tLexeme.eType.TYPEIS32, self.stack, lineNum, colNum)
		elif self.stack == 'tIU64': self.add(tLexeme.eType.TYPEIU64, self.stack, lineNum, colNum)
		elif self.stack == 'tIS64': self.add(tLexeme.eType.TYPEIS64, self.stack, lineNum, colNum)
		elif self.stack == 'tFP32': self.add(tLexeme.eType.TYPEFP32, self.stack, lineNum, colNum)
		elif self.stack == 'tFP64': self.add(tLexeme.eType.TYPEFP64, self.stack, lineNum, colNum)
		else: self.add(tLexeme.eType.IDENT, self.stack, lineNum, colNum)
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
			elif self.curr == ':': self.add(tLexeme.eType.COLON)
			elif self.curr == '(': self.add(tLexeme.eType.LPAREN)
			elif self.curr == ')': self.add(tLexeme.eType.RPAREN)
			elif self.curr == ',': self.add(tLexeme.eType.COMMA)
			elif self.curr == '{': self.add(tLexeme.eType.LBRACE)
			elif self.curr == '}': self.add(tLexeme.eType.RBRACE)
			elif self.curr == ';':
				while True:
					ahdChar = self.ahd()
					if ahdChar == '\n' or ahdChar == '': break
					self.nxt()
			elif self.curr == '^':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.CARETEQ, '^=')
					self.nxt()
				else: self.add(tLexeme.eType.CARET)
			elif self.curr == '=':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.EQUIV, '==')
					self.nxt()
				else: self.add(tLexeme.eType.ASSIGN)
			elif self.curr == '<':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.LTEQ, '<=')
					self.nxt()
				elif ahdChar == '<':
					colNum = self.colNum
					self.nxt()
					if self.ahd() == '=':
						self.add(tLexeme.eType.LEFTSHEQ, '<<=', self.lineNum, colNum)
						self.nxt()
					else:
						self.add(tLexeme.eType.LEFTSH, '<<', self.lineNum, colNum)
				else: self.add(tLexeme.eType.LT)
			elif self.curr == '>':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.GTEQ, '>=')
					self.nxt()
				elif ahdChar == '>':
					colNum = self.colNum
					self.nxt()
					if self.ahd() == '=':
						self.add(tLexeme.eType.RIGHTSHEQ, '>>=', self.lineNum, colNum)
						self.nxt()
					else:
						self.add(tLexeme.eType.RIGHTSH, '>>', self.lineNum, colNum)
				else: self.add(tLexeme.eType.GT)
			elif self.curr == '+':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.PLUSEQ, '+=')
					self.nxt()
				else: self.add(tLexeme.eType.PLUS)
			elif self.curr == '-':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.MINUSEQ, '-=')
					self.nxt()
				else: self.add(tLexeme.eType.MINUS)
			elif self.curr == '*':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.ASTERISKEQ, '*=')
					self.nxt()
				else: self.add(tLexeme.eType.ASTERISK)
			elif self.curr == '/':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.FSLASHEQ, '/=')
					self.nxt()
				else: self.add(tLexeme.eType.FSLASH)
			elif self.curr == '%':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.PERCENTEQ, '%=')
					self.nxt()
				else: self.add(tLexeme.eType.PERCENT)
			elif self.curr == '&':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.ANDEQ, '&=')
					self.nxt()
				else: self.add(tLexeme.eType.AND)
			elif self.curr == '|':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.OREQ, '|=')
					self.nxt()
				else: self.add(tLexeme.eType.OR)
			elif self.curr == '~':
				ahdChar = self.ahd()
				if ahdChar == '=':
					self.add(tLexeme.eType.NOTEQ, '~=')
					self.nxt()
				else: self.add(tLexeme.eType.NOT)
			elif self.curr.isalpha() or self.curr == '_': self.ident()
			elif self.curr.isnumeric(): self.num()
			else:
				print(f'ERR: Unknown lexeme \'{self.curr}\' encountered @ {self.fileName}:{self.lineNum}:{self.colNum}.')
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
		t = tTokeniser(fileName)
		t.strt()
		for lexeme in t.lexemes:
			print(lexeme)