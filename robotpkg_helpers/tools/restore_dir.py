#!/usr/bin/python3
import os
import sys
from robotpkg_helpers import HandlingImgs

def restore_dir(filename):
    aHandlingImgs = HandlingImgs()

    aHandlingImgs.restore_from_backup_dir(tar_file_name=filename)


if __name__ == "__main__":
    filename=sys.argv[1]
    restore_dir(filename)

