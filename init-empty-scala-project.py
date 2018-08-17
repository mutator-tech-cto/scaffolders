#!/usr/bin/python3

# arguments projectName projectOrganization projectType scalaVersion sbtVersion
# projectName: string
# projectOrganization string[.string]*
# projectType (js | jvm | native)
# scalaVersion i.j.k[-RCN] | latest
# sbtVersion i.j.k[-RCN] | latest

import argparse
from sys import argv


parser = argparse.ArgumentParser(description='Initialize empty Scala project')

parser.add_argument(
    "-n", "--name",
    help = "Scala empty project name",
    required = True
)

parser.add_argument(
    "-org", "--organization",
    help = "project organization qualified name",
    required = True
)

parser.add_argument(
    "-t", "--type",
    help = "Scala project type: (native | js | jvm)",
    default = "jvm"
)

parser.add_argument(
    "-scala", "--scala-version",
    help = "Scala version: (major.minor.patch)(-RC)? | latest",
    default = "latest"
)

parser.add_argument(
    "-sbt", "--sbt-version",
    help = "sbt version: (major.minor.patch)(-RC)? | latest",
    default = "latest"
)

arguments = parser.parse_args()

