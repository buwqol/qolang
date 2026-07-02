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
		POINT=enum.auto()
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

		NUMINT=enum.auto()

	def __init__(self, lexemeType, rawValue, lineNum, colNum):
		self.lexemeType = lexemeType
		self.rawValue = rawValue
		self.lineNum = lineNum
		self.colNum = colNum
		self.calcVal = 0
	def __repr__(self):
		return f'(@{self.lineNum},{self.colNum}) {str(self.lexemeType)[6:]}: \'{self.rawValue}\' {self.calcVal}'
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
	def add(self, lexemeType, rawValue='', lineNum=-1, colNum=-1):
		if lineNum == -1: lineNum = self.lineNum
		if colNum == -1: colNum = self.colNum
		if rawValue == '': rawValue = self.curr
		lexeme = tLexeme(lexemeType, rawValue, lineNum, colNum)
		if lexemeType == tLexeme.eType.NUMINT: lexeme.calcVal = int(rawValue)
		self.lexemes.append(lexeme)
	def num(self):
		lineNum = self.lineNum
		colNum = self.colNum
		self.stack += self.curr
		peekedChar = self.ahd()
		while peekedChar.isnumeric():
			self.nxt()
			self.stack += self.curr
			peekedChar = self.ahd()
		self.add(tLexeme.eType.NUMINT, self.stack, lineNum, colNum)
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
					if ahdChar == '\n' or ahdChar == '':
						break
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
				elif ahdChar == '>':
					self.add(tLexeme.eType.POINT, '=>')
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
			elif self.curr.isalpha() or self.curr == '_':
				self.ident()
			elif self.curr.isnumeric():
				self.num()
			else:
				print(f'Err: Unknown lexeme \'{self.curr}\' encountered ({self.fileName}:{self.lineNum}:{self.colNum}).')
				exit(1)

if __name__ == '__main__':
	argParser = argparse.ArgumentParser(prog='qolang', description='qolang language compiler.')
	argParser.add_argument('infiles', help='Input source files.', nargs='+')
	args = argParser.parse_args(sys.argv[1:])
	for fileName in args.infiles:
		if not os.path.exists(fileName):
			print(f'Err: File \'{fileName}\' does not exist.')
			sys.exit(1)
	for fileName in args.infiles:
		t = tTokeniser(fileName)
		t.strt()
		for lexeme in t.lexemes:
			print(lexeme)