################################################################################
# Filename: fileops.py
# Author:   Brandon Milton, http://brandonio21.com
# Date:     30 August 2015
#
# This module contains many useful functions for operating with files
################################################################################
import os
import json
import shutil

def exists(path, fileType):
    """
    Returns whether the object at the given path exists
    """
    # Check if file exists
    if not os.path.exists(path):
        return False
    # File exists. If type is file, check if path is file
    elif fileType == FileType.FILE:
        return os.path.isfile(path)
    # File exists. Type is dir. Check if path is dir
    else:
        return os.path.isdir(path)

def make(path, fileType):
    """
    Makes the file located at the given path if it doesnt already exist
    Returns: A boolean indicating whether the file was made
    """
    if exists(path, fileType):
        return False

    if fileType == FileType.FILE:
        os.mknod(path)
    else:
        os.mkdir(path)
    return True

def remove(path, fileType):
    """
    Removes the file given by path
    Returns: A boolean indicating whether the file was deleted
    """
    if not exists(path, fileType):
        return False

    if fileType == FileType.FILE:
        os.remove(path)
    else:
        try:
            shutil.rmtree(path)
        except Exception:
            return False

    return True

def get_json_dict(path):
    """
    Returns a dictionary for a json file if it exists, else an empty dict
    """
    dictionary = {}
    if exists(path, FileType.FILE):
        with open(path) as openFile:
            dictionary = json.loads(openFile.read())

    return dictionary

def write_json_dict(path, dictionary):
    """
    Writes a dictionary into a json file
    """
    with open(path, 'w+') as openFile:
        openFile.write(json.dumps(dictionary))

def join_path(path, *parts):
    """
    Joins the path with a list of parts
    """
    return os.path.join(path, *parts)

def get_files_in_dir(path: str, recursive: bool=False) -> list:
    """
    Returns a list of filepaths within a directory. Also includes child directories if recursive
    """
    if not recursive:
        return [join_path(path, filePath) for filePath in os.listdir(path) if os.path.isfile(join_path(path, filePath))]
    else:
        workingFileList = get_files_in_dir(path, recursive=False)
        for filePath in os.listdir(path):
            if os.path.isdir(join_path(path, filePath)):
                workingFileList.extend(get_files_in_dir(join_path(path, filePath), recursive=True))

        return workingFileList

def get_basename_less_extension(path: str) -> str:
    """
    Returns the basename of the file given by path without its extension
    """
    return os.path.splitext(os.path.basename(path))[0]

def get_basename(path: str) -> str:
    """
    Returns the basename of the file given by path
    """
    return os.path.basename(path)

def get_extension(path: str) -> str:
    """
    Returns the extension of the file given by path
    """
    return os.path.splitext(os.path.basename(path))[1][1:]

def get_parent_dir(path: str) -> str:
    """
    Returns the parent directory of the given path
    """
    return os.path.dirname(path)

def get_path_with_changed_extension(path: str, newExtension:str) -> str:
    """
    Changes the extension of a file given at path to the newExtension
    """
    return path.replace('.{}'.format(get_extension(path)), newExtension)


class FileType:
    FILE = 0
    DIRECTORY = 1
