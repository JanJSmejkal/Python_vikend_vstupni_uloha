#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author:   Jan Šmejkal
# Created:  18.11.16
#
# Begin code:
from src.services.std_com import STD_com
from src.services.stringParser import StringParser
from src.services.infrastructureManager import InfrastructureManager

import argparse
from datetime import timedelta


def process_arguments():
	"""
	Processes given arguments and returns settings dict
	:param argv: [String]
	:return: dict
	"""
	# All available settings
	settings = {
		"debug": False,
		"output_type": "json",
		"output_type_values": {"readable": "get_description()", "json": "to_json()", "min_json": "to_json(minimize=True)"},
		"min_bags": 0,
		"max_bags": 2,
		"min_travel_length": 2,
		"max_travel_length": 10,
		"min_wait_time": timedelta(hours=1),
		"max_wait_time": timedelta(hours=4),
	}

	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--debug", type=bool, default=False, help="inputs are loaded from internal file and not from command line")
	parser.add_argument("-o", "--output_type", type=str, default="min_json", help="switch output type/style, possible values: " + ",".join(list(settings["output_type_values"].keys())))

	args = parser.parse_args()

	settings["debug"] = True
	if args.output_type in settings["output_type_values"]:
		settings["output_type"] = args.output_type

	return settings


def main(settings):
	# Loading data
	file = STD_com.file_from_path("input.csv") if settings["debug"] else STD_com.file_from_stdin()

	# Parsing loaded data to objects
	flights = StringParser.file_to_flights(file)
	if not flights:
		STD_com.print_stderr("Couldn't load data, shutting down!")
		exit(1)

	# Creating infrastructure from parsed flights objects
	infrastructure = InfrastructureManager.create_from_flights(flights, settings)

	# Searching for all possible combinations
	for bags in range(settings["min_bags"], settings["max_bags"]+1):
		travels = infrastructure.find_all_connections(bags)
		for t in travels:
			STD_com.print_stdout(eval("t."+settings["output_type_values"][settings["output_type"]]))

if __name__ == "__main__":
	loaded_settings = process_arguments()
	main(loaded_settings)
