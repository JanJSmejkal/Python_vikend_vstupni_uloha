#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   Jan Šmejkal
# Created:  18.11.16
#
# Begin code:


class Airport:
	"""
	Simple structure representing airport
	"""
	def __init__(self, code):
		"""
		Init
		:param code: String
		:return: None
		"""
		self.code = code
		self.flights = []
