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

import getopt
import sys
from datetime import timedelta


def process_arguments(argv):
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

	usage = "find_combinations.py [-d | --debug] [-o | --output_type] <output type> \n\n"
	usage += "{:<30}{:<50}\n".format("-d, --debug", "inputs are loaded from internal file and not from command line")
	usage += "{:<30}{:<50}\n".format("-o, --output_type", "switch output type/style")
	usage += "{:<30}{:<50}\n".format(" ", "- possible values: "+", ".join(list(settings["output_type_values"].keys())))

	try:
		opts, args = getopt.getopt(argv, "hdo:", ["debug", "output_type="])
	except getopt.GetoptError:
		STD_com.print_stdout(usage)
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			STD_com.print_stdout(usage)
			sys.exit(0)
		elif opt in ("-d", "--debug"):
			settings["debug"] = True
		elif opt in ("-o", "--output_type"):
			if arg in settings["output_type_values"]:
				settings["output_type"] = arg
			else:
				STD_com.print_stderr("{} is unsupported value for output type!".format(arg))
				STD_com.print_stdout(usage)
				sys.exit(2)
	return settings


def main(settings):
	# Loading data
	if settings["debug"]:
		file = STD_com.file_from_path("input.csv")
	else:
		file = STD_com.file_from_stdin()

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
	loaded_settings = process_arguments(sys.argv[1:])
	main(loaded_settings)
