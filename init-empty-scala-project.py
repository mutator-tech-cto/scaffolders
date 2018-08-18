#!/usr/bin/python3

# TODO: fix latest sbt version fetching for Scala Native

# arguments projectName projectOrganization projectType scalaVersion sbtVersion
# projectName: string
# projectOrganization string[.string]*
# projectType (js | jvm | native)
# scalaVersion i.j.k[-RCN] | latest
# sbtVersion i.j.k[-RCN] | latest

import argparse
import os
from sys import argv
import requests
import re


parser = argparse.ArgumentParser(
	description = 'Initialize empty Scala project'
)

parser.add_argument(
	"-n", "--name",
	dest = "name",
	help = "Scala empty project name",
	required = True
)

parser.add_argument(
	"-org", "--organization",
	dest = "organization",
	help = "project organization qualified name",
	required = True
)

parser.add_argument(
	"-t", "--type",
	dest = "type",
	help = "Scala project type: (native | js | jvm)",
	default = "jvm"
)

parser.add_argument(
	"-scala", "--scala-version",
	dest = "scala_version",
	help = "Scala version: (major.minor.patch)(-RC)? | latest",
	default = "latest"
)

parser.add_argument(
	"-scala-js", "--scala-js-version",
	dest = "scala_js_version",
	help = "ScalaJS version: (major.minor.patch)(-RC)? | latest",
	default = "latest"
)

parser.add_argument(
	"-scala-native", "--scala-native",
	dest = "scala_native_version",
	help = "Scala Native version: (major.minor.patch)(-RC)? | latest",
	default = "latest"
)

parser.add_argument(
	"-sbt", "--sbt-version",
	dest = "sbt_version",
	help = "sbt version: (major.minor.patch)(-RC)? | latest",
	default = "latest"
)

arguments = parser.parse_args()

def fetch_latest_sbt_version():
	return requests.get(
		"https://api.bintray.com/packages/sbt/maven-releases/sbt/versions/_latest"
	).json()['name']

def sbt_version(version):
	return {
		'latest': fetch_latest_sbt_version()
	}.get(version, version)

def scala_native_version(version):
	return {
		'latest': fetch_latest_scala_native_sbt_plugin_version()
	}.get(
		version, version
	)

def fetch_latest_scala_native_sbt_plugin_version():
	return requests.get(
		"https://api.bintray.com/packages/sbt/sbt-plugin-releases/sbt-scala-native/versions/_latest"
	).json()['name']

def scala_js_version(version):
	return {
		'latest': fetch_latest_scala_js_sbt_plugin_version()
	}.get(
		version, version
	)

def fetch_latest_scala_js_sbt_plugin_version():
	return requests.get(
		"https://api.bintray.com/packages/sbt/sbt-plugin-releases/sbt-scalajs/versions/_latest"
	).json()['name']

def sbt_plugins(project_type):
	return {
		'native': 'addSbtPlugin("org.scala-native" % "sbt-scala-native" % "{}")'.format(
			scala_native_version(arguments.scala_native_version)
		),
		'js': 'addSbtPlugin("org.scala-js" % "sbt-scalajs" % "{}")'.format(
			scala_js_version(arguments.scala_js_version)
		)
	}.get(project_type, '')

def camel_casify(string):
	result = ''
	next_character_to_upper_case_flag = False
	for i in range(0, len(string)):
		if string[i] == '-':
			next_character_to_upper_case_flag = True
		else:
			if next_character_to_upper_case_flag:
				result += string[i].upper()
				next_character_to_upper_case_flag = False
			else:
				result += string[i]
	return result

def scala_version(version):
	return {
		'latest': requests.get(
			"https://api.github.com/repos/scala/scala/releases/latest"
		).json()['tag_name'][1:]
	}.get(version, version)


if not os.path.exists(arguments.name):
	os.makedirs(
		"{}/project".format(arguments.name)
	)

	with open("{}/project/build.properties".format(arguments.name), 'w') as build_properties:
		print(
			"sbt.version = {}".format(sbt_version(arguments.sbt_version)),
			file = build_properties
		)
	
	with open("{}/project/plugins.sbt".format(arguments.name), 'w') as project_sbt_plugins:
		print(
			sbt_plugins(arguments.type),
			file = project_sbt_plugins
		)

	with open("{}/build.sbt".format(arguments.name), 'w') as build_definition:
		print(
			re.sub("\t\t\t\t", "", f"""
				val {camel_casify(arguments.name)} = (
					project in file(".")
				).{
					{
						'native': 'ScalaNativePlugin',
						'js': 'ScalaJSPlugin'
					}.get(arguments.type, '')
				}settings(
					name := "{arguments.name}",
					organization := "{arguments.organization}",
					version := "0.1.0-SNAPSHOT",
					scalaVersion := "{scala_version(arguments.scala_version)}"
				)
				"""
			),
			file = build_definition
		)

	os.makedirs(
		"{}/src/main/scala".format(arguments.name)
	)
else:
	print(
		"Directory with name {} exists".format(arguments.name)
	)
