'''
    This is an simple wrapper used to launch commands on dockerised caretta-cli
'''

import subprocess
import os
import sys


class DockerComposeNotFound(Exception):
    pass


class CarettaCli:

    def __init__(self, path_to_caretta, cmd):
        # Requirement is the full path to the copied repository. This is needed to execute commands in the container.
        path_to_caretta = os.path.normpath(path_to_caretta)
        path_to_compose = os.path.join(path_to_caretta, '.docker\\docker-compose.yml')

        if not os.path.isfile(path_to_compose):
            raise DockerComposeNotFound('Provided caretta path does not contain docker files:\n\t', path_to_caretta)

        subprocess.run((
            'docker-compose -f {path} exec caretta '
            'caretta-cli {cmd}'
            .format(
                path=path_to_compose.replace('\\', '/'),
                cmd=cmd.replace('\\', '/')
            )
        ))


if __name__ == '__main__':
    CarettaCli(path_to_caretta=sys.argv[1], cmd=sys.argv[2])
