#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   Jan Šmejkal
# Created:  22.11.16
#
# Begin code:
from src.services.stringParser import StringParser
from src.services.infrastructureManager import InfrastructureManager

import unittest
from datetime import timedelta


class TestSearching(unittest.TestCase):
	def setUp(self):
		self.settings = {
			"min_bags": 0,
			"max_bags": 2,
			"min_travel_length": 2,
			"max_travel_length": 10,
			"min_wait_time": timedelta(hours=1),
			"max_wait_time": timedelta(hours=4),
		}

	def create_infrastructure_from_fligths(self, flights):
		header = ["source,destination,departure,arrival,flight_number,price,bags_allowed,bag_price"]
		header.extend(flights)
		flights = StringParser.file_to_flights(header)
		return InfrastructureManager.create_from_flights(flights, self.settings)

	def test_one_possible_route_zero_bags(self):
		flights = [
			"Airport1,Airport2,2017-02-11T00:00:01,2017-02-11T01:00:00,FLIGHT1,10,0,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT2,10,0,0",
		]
		infr_str = self.create_infrastructure_from_fligths(flights)
		routes = infr_str.find_all_connections(bags=0)
		self.assertEqual(len(routes), 1)
		self.assertEqual(len(routes[0]), 2)

	def test_one_possible_route_one_bag(self):
		flights = [
			"Airport1,Airport2,2017-02-11T00:00:01,2017-02-11T01:00:00,FLIGHT1,10,1,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT2,10,1,0",
		]
		infr_str = self.create_infrastructure_from_fligths(flights)
		routes = infr_str.find_all_connections(bags=1)
		self.assertEqual(len(routes), 1)
		self.assertEqual(len(routes[0]), 2)
		for r in routes:
			for f in r.flights:
				self.assertTrue(f.bags_allowed >= r.BAGS)

	def test_one_possible_route_one_bag_one_false_flight(self):
		flights = [
			"Airport1,Airport2,2017-02-11T00:00:01,2017-02-11T01:00:00,FLIGHT1,10,1,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT2,10,1,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT3,10,0,0",
		]
		infr_str = self.create_infrastructure_from_fligths(flights)
		routes = infr_str.find_all_connections(bags=1)
		self.assertEqual(len(routes), 1)
		self.assertEqual(len(routes[0]), 2)
		for r in routes:
			for f in r.flights:
				self.assertTrue(f.bags_allowed >= r.BAGS)

	def test_one_possible_route_two_bags(self):
		flights = [
			"Airport1,Airport2,2017-02-11T00:00:01,2017-02-11T01:00:00,FLIGHT1,10,2,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT2,10,2,0",
		]
		infr_str = self.create_infrastructure_from_fligths(flights)
		routes = infr_str.find_all_connections(bags=2)
		self.assertEqual(len(routes), 1)
		self.assertEqual(len(routes[0]), 2)
		for r in routes:
			for f in r.flights:
				self.assertTrue(f.bags_allowed >= r.BAGS)

	def test_one_possible_route_two_bags_one_false_flight(self):
		flights = [
			"Airport1,Airport2,2017-02-11T00:00:01,2017-02-11T01:00:00,FLIGHT1,10,2,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT2,10,2,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT3,10,1,0",
		]
		infr_str = self.create_infrastructure_from_fligths(flights)
		routes = infr_str.find_all_connections(bags=2)
		self.assertEqual(len(routes), 1)
		self.assertEqual(len(routes[0]), 2)
		for r in routes:
			for f in r.flights:
				self.assertTrue(f.bags_allowed >= r.BAGS)

	def test_two_possible_routes_zero_bags(self):
		flights = [
			"Airport1,Airport2,2017-02-11T00:00:01,2017-02-11T01:00:00,FLIGHT1,10,0,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT2,10,0,0",
			"Airport2,Airport3,2017-02-11T02:35:00,2017-02-11T05:00:00,FLIGHT3,10,0,0",
		]
		infr_str = self.create_infrastructure_from_fligths(flights)
		routes = infr_str.find_all_connections(bags=0)
		self.assertEqual(len(routes), 2)
		self.assertEqual(len(routes[0]), 2)

	def test_two_possible_routes_zero_bags_repeating_segments(self):
		flights = [
			"Airport1,Airport2,2017-02-11T00:00:01,2017-02-11T01:00:00,FLIGHT1,10,0,0",
			"Airport2,Airport1,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT2,10,0,0",
			"Airport1,Airport2,2017-02-11T07:00:00,2017-02-11T09:00:00,FLIGHT3,10,0,0",
		]
		infr_str = self.create_infrastructure_from_fligths(flights)
		routes = infr_str.find_all_connections(bags=0)
		self.assertEqual(len(routes), 2)
		self.assertEqual(len(routes[0]), 2)
		self.assertEqual(len(routes[1]), 2)

	def test_six_possible_routes_zero_bags(self):
		flights = [
			"Airport1,Airport2,2017-02-11T00:00:01,2017-02-11T01:00:00,FLIGHT1,10,0,0",
			"Airport2,Airport3,2017-02-11T02:30:00,2017-02-11T05:00:00,FLIGHT2,10,0,0",
			"Airport3,Airport4,2017-02-11T06:35:00,2017-02-11T08:00:00,FLIGHT3,10,0,0",
			"Airport4,Airport5,2017-02-11T09:35:00,2017-02-11T11:00:00,FLIGHT4,10,0,0",
		]
		infr_str = self.create_infrastructure_from_fligths(flights)
		routes = infr_str.find_all_connections(bags=0)
		self.assertEqual(len(routes), 6)
		self.assertEqual(max([len(r) for r in routes]), 4)