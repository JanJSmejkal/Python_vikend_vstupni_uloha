#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   Jan Šmejkal
# Created:  19.11.16
#
# Begin code:
from src.model.airport import Airport
from src.model.travel import Travel


class InfrastructureManager:
	"""
	Manages searching of connections between airports
	"""
	def __init__(self, airports, settings):
		"""
		Init
		:param airports: {AirportStringName: [src.model.flight.Flight]}
		:param settings: dict
		:return: None
		"""
		self.airports = airports
		self.settings = settings
		self.MAX_SEARCH_DEPTH = 100

	@staticmethod
	def create_from_flights(flights, settings):
		"""
		Creates InfrastructureManager instance from given array of flights and with given settings
		:param flights: [src.model.flight.Flight]
		:param settings: dict
		:return: InfrastructureManager
		"""
		airports = {}
		for f in flights:
			if f.source_code not in airports:
				airports[f.source_code] = Airport(f.source_code)
			if f.destination_code not in airports:
				airports[f.destination_code] = Airport(f.destination_code)

			airports[f.source_code].flights.append(f)
		return InfrastructureManager(airports, settings)

	def find_all_connections(self, bags=0):
		"""
		Finds all connection in available airports for passenger with given number of bags
		:param bags: Integer
		:return: None
		"""
		routes = []
		for airport_code in self.airports:
			for flight in self.airports[airport_code].flights:
				if flight.bags_allowed < bags:
					continue
				new_routes = self._non_target_breadth_first_search([Travel(flight, bags, self.settings)])
				new_routes = [route for route in new_routes if len(route) >= self.settings["min_travel_length"]]
				if len(new_routes) > 0:
					routes.extend(new_routes)
		return routes

	def _non_target_breadth_first_search(self, travels, current_depth=1):
		"""
		Searches in available airports with breadth first search algorithm with given starting points
		:param travels: [src.model.travel.Travel]
		:param current_depth: Integer
		:return: [src.model.travel.Travel]
		"""
		if current_depth > self.MAX_SEARCH_DEPTH:
			return travels
		out = []
		for travel in travels:
			for flight in self.airports[travel.last_flight.destination_code].flights:
				if travel.can_be_added(flight):
					new_travel_branch = travel.copy()
					new_travel_branch.try_add_flight(flight)
					out.append(new_travel_branch)
		if len(out) > 0:
			out = self._non_target_breadth_first_search(out, current_depth+1)
			travels.extend(out)
		return travels
