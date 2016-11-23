#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   Jan Šmejkal
# Created:  18.11.16
#
# Begin code:


class Flight:
	"""
	Represents one flight
	"""
	def __init__(self, splitted_line):
		"""
		Inits from given values
		:param splitted_line: List of values, see src.services.stringParser.StringParser.string_to_flight()
		:return: None
		"""
		self.source_code = splitted_line[0]
		self.destination_code = splitted_line[1]
		self.departure = splitted_line[2]
		self.arrival = splitted_line[3]
		self.flight_number = splitted_line[4]
		self.price = splitted_line[5]
		self.bags_allowed = splitted_line[6]
		self.bag_price = splitted_line[7]

	def __str__(self):
		"""
		To String
		:return: String
		"""
		return self.source_code + " > " + self.flight_number + " > " + self.destination_code

	def to_detailed_string(self):
		"""
		To detailed String, with all informations
		:return: String
		"""
		from src.services.stringParser import StringParser
		return "Flight {}: departure from {} at {}, arrival to {} at {}, price {}, maximum bags {}, price per bag {}".format(
			self.flight_number, self.source_code, StringParser.datetime_to_string(self.departure),
			self.destination_code, StringParser.datetime_to_string(self.arrival), self.price,
			self.bags_allowed, self.bag_price)

	def to_dict(self):
		"""
		To Python dictionary
		:return: dict
		"""
		from src.services.stringParser import StringParser
		out = {
			"origin:": self.source_code,
			"destination": self.destination_code,
			"flight_number": self.flight_number,
			"departure": StringParser.datetime_to_string(self.departure),
			"arrival": StringParser.datetime_to_string(self.arrival),
			"price": self.price,
			"max_bag": self.bags_allowed,
			"price_per_bag": self.bag_price,
		}
		return out
