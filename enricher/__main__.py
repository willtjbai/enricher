#! /usr/bin/env python3
import sys

from enricher import enricher_core

if __name__ == '__main__':
    # Check if the user is using the correct version of Python
    python_version = sys.version.split()[0]

    if sys.version_info < (3, 9):
        print("Enricher requires Python 3.9+\n"
              "You are using Python %s, which is not supported by Enricher" % python_version)
        sys.exit(1)

    enricher_core.main()
