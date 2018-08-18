# Init ? project.empty [ Scala { JVM | JS | Native } ]

```bash
usage: init-empty-scala-project.py [-h] -n NAME -org ORGANIZATION [-t TYPE]
                                   [-scala SCALA_VERSION] [-sbt SBT_VERSION]

Initialize empty Scala project

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  Scala empty project name
  -org ORGANIZATION, --organization ORGANIZATION
                        project organization qualified name
  -t TYPE, --type TYPE  Scala project type: (native | js | jvm)
  -scala SCALA_VERSION, --scala-version SCALA_VERSION
                        Scala version: (major.minor.patch)(-RC)? | latest
  -sbt SBT_VERSION, --sbt-version SBT_VERSION
                        sbt version: (major.minor.patch)(-RC)? | latest
```
