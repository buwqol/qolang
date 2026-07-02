#!/bin/python3

import argparse
import sys
import os
import io
import enum

class tLexeme(object):
	class eType(enum.Enum):
		IDENT=0
		COLON=1
		LPAREN=2
		RPAREN=3
		COMMA=4
		CARET=5
		ASSIGN=6
		EQUIV=7
		POINT=8
		LBRACE=9
		RBRACE=10
	def __init__(self, lexemeType, rawValue, lineNum, colNum):
		self.lexemeType = lexemeType
		self.rawValue = rawValue
		self.lineNum = lineNum
		self.colNum = colNum
	def __repr__(self):
		return f'(@{self.lineNum: 4},{self.colNum: 4}) {str(self.lexemeType)[6:]}: \'{self.rawValue}\''
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
	def ahd(self, off=1):
		nextChar = self.file.read(off)
		self.file.seek(self.lastReadByte - off, io.SEEK_SET)
		return nextChar
	def add(self, lexemeType, rawValue='', lineNum=-1, colNum=-1):
		if lineNum == -1: lineNum = self.lineNum
		if colNum == -1: colNum = self.colNum
		if rawValue == '': rawValue = self.curr
		self.lexemes.append(tLexeme(lexemeType, rawValue, lineNum, colNum))
	def ident(self):
		lineNum = self.lineNum
		colNum = self.colNum
		self.stack += self.curr
		peekedChar = self.ahd(1)
		while peekedChar.isalnum() or peekedChar == '_':
			self.nxt()
			self.stack += self.curr
			peekedChar = self.ahd(1)
		self.add(tLexeme.eType.IDENT, self.stack, lineNum, colNum)
		self.stack = ''
	def strt(self):
		while True:
			self.nxt()
			if self.curr == '': break
			elif self.curr == '\n':
				self.lineNum += 1
				self.colNum = 0
			elif self.curr == '\r': self.colNum = 0
			elif self.curr == ' ': continue
			elif self.curr == ':': self.add(tLexeme.eType.COLON)
			elif self.curr == '(': self.add(tLexeme.eType.LPAREN)
			elif self.curr == ')': self.add(tLexeme.eType.RPAREN)
			elif self.curr == ',': self.add(tLexeme.eType.COMMA)
			elif self.curr == '^': self.add(tLexeme.eType.CARET)
			elif self.curr == '{': self.add(tLexeme.eType.LBRACE)
			elif self.curr == '}': self.add(tLexeme.eType.RBRACE)
			elif self.curr == '=':
				ahdChar = self.ahd(1)
				if ahdChar == '=':
					self.add(tLexeme.eType.EQUIV, '==')
					self.nxt()
				elif ahdChar == '>':
					self.add(tLexeme.eType.POINT, '=>')
					self.nxt()
				else: self.add(tLexeme.eType.ASSIGN)
			elif self.curr.isalpha() or self.curr == '_':
				self.ident()
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