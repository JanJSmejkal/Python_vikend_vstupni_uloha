#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   Jan Šmejkal
# Created:  18.11.16
#
# Begin code:
from src.model.flight import Flight
from src.services.std_com import STD_com

from datetime import datetime


class StringParser:
	"""
	Class for String Parsing
	"""
	datetime_format = "%Y-%m-%d %H:%M:%S"

	@staticmethod
	def file_to_flights(file):
		"""
		Converts file (splitted in lines) to array of flights
		:param file: [String]
		:return: [src.model.flight.Flight]
		"""
		flights = []
		for i, line in enumerate(file):
			if i <= 0:
				continue
			new_flight = StringParser.string_to_flight(line)
			if not new_flight:
				return None
			flights.append(new_flight)
		return flights

	@staticmethod
	def string_to_flight(string):
		"""
		Converts one String line to flight
		:param string: String
		:return: src.model.flight.Flight
		"""
		try:
			split = string.split(",")
			split[2] = StringParser.string_to_datetime(split[2])
			split[3] = StringParser.string_to_datetime(split[3])
			split[5] = float(split[5])
			split[6] = int(split[6])
			split[7] = float(split[7])
			return Flight(split)
		except (ValueError, IndexError) as e:
			STD_com.print_stderr("Couldn't convert input file to proper values!\n - Error message: {}".format(e))
			return None

	@staticmethod
	def string_to_datetime(string):
		"""
		Converts String to datetime object
		:param string: String
		:return: datetime.datetime
		"""
		try:
			dtime = datetime.strptime(string.replace("T", " "), StringParser.datetime_format)
			return dtime
		except ValueError as e:
			STD_com.print_stderr("Couldn't convert {} to datetime format!\n - Error message: {}".format(string, e))
			return None

	@staticmethod
	def datetime_to_string(dtime):
		"""
		Converts datetime object to String
		:param dtime: datetime.datetime
		:return: String
		"""
		return dtime.strftime(StringParser.datetime_format)
