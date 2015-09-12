################################################################################
# Filename: writer.py
# Author:   Brandon Milton, http://brandonio21.com
# Date:     30 August 2015
# 
# This file contains all information pertaining to solution writers
################################################################################
from util import fileops

class Writer:
    DATAFILE_PATH = 'data.json'
    DATAFILE_NAME_FIELD = 'name'
    DATAFILE_EMAIL_FIELD = 'email'

    def __init__(self, writerEmail='', writerName='', writerPath=''):
        self.name = writerName
        self.email = writerEmail
        self._path = writerPath
        self._solutions = {} 

    def _get_datafile_path(self) -> str:
        """
        Return the path of the data file for this writer. 
        """
        return fileops.join_path(self._path, self.DATAFILE_PATH)

    def get_solutions(self, problemNumber: int) -> list:
        """
        Get list of solution for specified problem
        """
        return self._solutions[problemNumber] if problemNumber in self._solutions else []

    def get_all_solutions(self) -> list:
        """
        Get list of all user completed solutions
        """
        totalSolutions = []
        for solutionList in [solutions for problemNumber, solutions in self._solutions.items()]:
            totalSolutions.extend(solutionList)

        return totalSolutions

    @staticmethod
    def load_from_path(path):
        """
        Loads a writer and all their solutions from a specified path
        """
        # Check if writer directoroy exists. If not, return nothing
        if not fileops.exists(path, fileops.FileType.DIRECTORY):
            return None

        loadedWriter = Writer(writerPath=path)

        # Load the user data from the data file
        dataDictionary = fileops.get_json_dict(loadedWriter._get_datafile_path)

        # Populate the data if available
        # Load name
        if DATAFILE_NAME_FIELD in dataDictionary:
            loadedWriter.name = dataDictionary[DATAFILE_NAME_FIELD]

        # Load email
        if DATAFILE_EMAIL_FIELD in dataDictionary:
            loadedWriter.email = dataDictionary[DATAFILE_EMAIL_FIELD]

        # Load all solutions