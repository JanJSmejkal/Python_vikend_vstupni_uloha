#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   Jan Šmejkal
# Created:  20.11.16
#
# Begin code:
from copy import deepcopy
import json

from src.services.stringParser import StringParser


class Travel:
	"""
	Represents travel plan - flights, bags, price, airports, ...
	"""
	def __init__(self, start_flight, desired_bags, settings):
		"""
		Inits self with given start flight, desired number of bags and settings
		:param start_flight: src.model.flight.Flight
		:param desired_bags: Integer
		:param settings: dict
		:return:
		"""
		self.flights = [start_flight]
		self.segments = {Travel.flight_segment_to_string(start_flight): 0}
		self.settings = settings
		self.BAGS = desired_bags

	def __len__(self):
		"""
		Returns length of this travel plan (number of used flights)
		Usage: len(travelInstance)
		:return: Integer
		"""
		return len(self.flights)

	def __contains__(self, flight):
		"""
		Tests if this travel plan uses (contains) given flight
		Usage: flightInstance in travelInstance
		:param flight: src.model.flight.Flight
		:return: Boolean
		"""
		return Travel.flight_segment_to_string(flight) in self.segments

	def __str__(self):
		"""
		To simple String
		:return: String
		"""
		return " ==> ".join([str(flight) for flight in self.flights])

	@property
	def last_flight(self):
		"""
		Returns last flight in this travel plan
		:return: src.model.flight.Flight
		"""
		return self.flights[-1]

	@staticmethod
	def flight_segment_to_string(flight):
		"""
		Converts flight to String
		Used for testing if this travel plan already uses given airports connection
		:param flight: src.model.flight.Flight
		:return: String
		"""
		return flight.source_code + flight.destination_code

	def try_add_flight(self, flight):
		"""
		Adds given flight to this travel plan if conditions are met.
		Returns True if flight was added, False otherwise
		:param flight: src.model.flight.Flight
		:return: Boolean
		"""
		if self.can_be_added(flight):
			self.flights.append(flight)
			self.segments[Travel.flight_segment_to_string(flight)] = len(self.flights)
			return True
		return False

	def can_be_added(self, flight):
		"""
		Returns True if given flight can be added to this travel plan, False otherwise
		:param flight: src.model.flight.Flight
		:return: Boolean
		"""
		if flight.bags_allowed < self.BAGS or len(self) >= self.settings["max_travel_length"]:
			return False
		if not (self.settings["min_wait_time"] <= flight.departure - self.last_flight.arrival <= self.settings["max_wait_time"]):
			return False
		flight_as_segment = Travel.flight_segment_to_string(flight)
		return flight_as_segment not in self.segments

	def get_price(self):
		"""
		Counts price for this whole travel plan
		:return: Float
		"""
		return sum([flight.price + self.BAGS*flight.bag_price for flight in self.flights])

	def generate_stops_to_string(self):
		"""
		Creates String with stops of this travel
		:return: String
		"""
		stops = [f.destination_code for f in self.flights]
		del stops[-1]
		return "-".join(stops)

	def get_description(self):
		"""
		Returns this travel plan as String in a human readable form
		:return: String
		"""
		out = "Traveling from {} to {}\n".format(self.flights[0].source_code, self.last_flight.destination_code)
		out += "    > departure: {}\n".format(StringParser.datetime_to_string(self.flights[0].departure))
		out += "    > arrival: {}\n".format(StringParser.datetime_to_string(self.last_flight.arrival))
		out += "    > bags: {}\n".format(self.BAGS)
		out += "    > total price: {}\n".format(self.get_price())
		out += "    > stops: {}\n".format(self.generate_stops_to_string())
		out += "    > FLIGHTS\n        "
		out += "\n        ".join([f.to_detailed_string() for f in self.flights])
		out += "\n"
		return out

	def to_json(self, sort_keys=True, indent=4, minimize=False):
		"""
		Returns this travel plan as String in json
		Removes all spaces from output if minimize = True
		:param sort_keys: Boolean
		:param indent: Integer
		:param minimize: Boolean
		:return: String
		"""
		out = {
			"total_price": self.get_price(),
			"bags": self.BAGS,
			"flights": [f.to_dict() for f in self.flights],
		}
		out = json.dumps(out, sort_keys=sort_keys, indent=indent)
		if minimize:
			return out.replace("\n", "").replace(" ", "")
		return out

	def copy(self):
		"""
		Returns copy of itself
		:return: src.model.travel.Travel
		"""
		return deepcopy(self)
