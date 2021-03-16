# Caretta docker image

Unofficial fork of the protein structure alignment tool Caretta.
Launch the web app or use the caretta-cli on any platform using Docker.

For official release and documentation see: https://github.com/TurtleTools/caretta



# Usage

Git clone and navigate to the directory

```commandline
git clone https://github.com/noxjonas/caretta.git
cd caretta
```

To build docker image run:
```commandline
docker-compose -f .docker/docker-dompose.yml build
```

To start the container run:
```commandline
docker-compose -f .docker/docker-compose.yml up -d
```

Navigate to http://localhost:8091 for the web app.

Or take a look at an example python wrapper class.
```commandline
python .docker/wrapper.py <path-to-caretta> "--help"
```

# Filepaths
Note that you need to link your system storage with the container in order to use the cli.
Do so by editing the `volumes:` field in the .docker/docker-compose.yml file.
