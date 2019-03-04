#!/usr/bin/python3
import os
import sys
from robotpkg_helpers import HandlingImgs

def clean_integration_directory():
    aHandlingImgs = HandlingImgs()

    aHandlingImgs.clean_integration_directory()


if __name__ == "__main__":
    clean_integration_directory()

