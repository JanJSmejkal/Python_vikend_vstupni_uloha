#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   Jan Šmejkal
# Created:  21.11.16
#
# Begin code:
import sys


class STD_com:
	"""
	Class for proper console writing
	"""
	@staticmethod
	def file_from_stdin():
		"""
		Returns String found on stdin
		:return: [String]
		"""
		return sys.stdin

	@staticmethod
	def file_from_path(path):
		"""
		Loads file from given path - for testing purposes!
		:param path: String
		:return: [String]
		"""
		with open(path, "r") as f:
			file = f.read().split("\n")
		return file

	@staticmethod
	def print_stdout(to_print):
		"""
		Prints to stdout
		:param to_print: String
		:return: None
		"""
		print(to_print, file=sys.stdout)

	@staticmethod
	def print_stderr(to_print):
		"""
		Prints to stderr
		:param to_print: String
		:return: None
		"""
		print(to_print, file=sys.stderr)
