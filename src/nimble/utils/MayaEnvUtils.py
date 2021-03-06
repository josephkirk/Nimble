# MayaEnvUtils.py
# (C)2013-2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import os
import re
from collections import namedtuple

import pyaid
from pyaid.OsUtils import OsUtils
from pyaid.file.FileUtils import FileUtils
import pyglass

import nimble
from nimble.utils.MayaEnvEntry import MayaEnvEntry



class MayaEnvUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    MAYA_ENV_MODIFIED_RESULT_NT = namedtuple(
        'MAYA_ENV_MODIFIED_RESULT_NT',
        ['added', 'removed'])

    _PYTHON_PATH_PATTERN = re.compile('PYTHONPATH=(?P<paths>[^\n\r]*)')


    @classmethod
    def locateMayaEnvFiles(cls):
        """ Finds the location of all Maya.env files located in the default location on the host
            and return them as a list. If no such env files exist, the method returns an empty
            list. """

        home = FileUtils.cleanupPath(OsUtils.getHomePath(), isDir=True)
        if not os.path.exists(home):
            return []

        if OsUtils.isWindows():
            root = FileUtils.createPath(OsUtils.getDocumentsPath(), 'maya', isDir=True)
            if not os.path.exists(root):
                return []
        elif OsUtils.isMac():
            root = FileUtils.createPath(
                home, 'Library', 'Preferences', 'Autodesk', 'maya', isDir=True)
            if not os.path.exists(root):
                return []
        else:
            return []

        out = []
        FileUtils.walkPath(root, cls._handleFindEnvFiles, out)
        return out


    @classmethod
    def checkEnvFile(cls, target, otherPaths =None):
        """Doc..."""
        pathSep   = OsUtils.getPerOsValue(';', ':')
        additions = cls._getSourcePaths(otherPaths=otherPaths)

        with open(target, 'r') as f:
            contents = f.read()

        result = cls._PYTHON_PATH_PATTERN.search(contents)
        if not result:
            return False

        paths = result.groupdict()['paths'].split(pathSep)
        for addition in additions:
            found = False
            for p in paths:
                p = FileUtils.cleanupPath(p, noTail=True)
                if p == FileUtils.cleanupPath(addition.folderPath, noTail=True):
                    found = True
                    break
            if not found:
                return False

        return True


    @classmethod
    def modifyEnvFile(cls, target, install =True, test =False, otherPaths =None):
        """Doc..."""
        pathSep   = OsUtils.getPerOsValue(';', ':')
        removals  = []
        entries   = cls._getSourcePaths(otherPaths=otherPaths)
        additions = entries + []

        with open(target, 'r') as f:
            contents = f.read().strip()

        result = cls._PYTHON_PATH_PATTERN.search(contents)
        if not result:
            if install and not test:
                with open(target, 'w') as f:
                    f.write(
                        (contents + '\n' if contents else '') + 'PYTHONPATH='
                        + cls._joinPathEntries(additions) )
            return cls.MAYA_ENV_MODIFIED_RESULT_NT(additions if install else [], removals)

        paths = result.groupdict()['paths'].strip()
        paths = paths.split(pathSep) if paths else []
        if not paths and not install:
            return cls.MAYA_ENV_MODIFIED_RESULT_NT([], [])

        index = 0
        while index < len(paths):
            # Stop if no more additions remain
            if not additions:
                break

            p = FileUtils.cleanupPath(paths[index], noTail=True)

            # If path already exists don't add it again
            pathMatch = cls._hasPath(p, additions)
            if pathMatch:
                additions.remove(pathMatch)

                # If uninstalling add to removals
                if not install:
                    removals.append(pathMatch)
                    paths.remove(p)
                else:
                    index += 1
                continue
            elif not install:
                index += 1
                continue

            for entry in entries:
                testPath = FileUtils.createPath(p, entry.rootName, noTail=True)
                if os.path.exists(testPath):
                    paths.remove(p)

            index += 1

        for entry in additions:
            paths.append(entry.folderPath)

        insertion = ('PYTHONPATH=' + pathSep.join(paths) + '\n') if paths else ''
        contents  = contents[:result.start()] + insertion + contents[result.end():]

        result = cls.MAYA_ENV_MODIFIED_RESULT_NT(additions if install else [], removals)
        if test:
            return result

        with open(target, 'w') as f:
            f.write(contents)

        return result

#===================================================================================================
#                                                                               P R O T E C T E D


    @classmethod
    def _hasPath(cls, path, entries):
        for entry in entries:
            if path == entry.folderPath:
                return entry
        return None


    @classmethod
    def _joinPathEntries(cls, entries):
        out = []
        for entry in entries:
            out.append(entry.folderPath)
        return OsUtils.getPerOsValue(';', ':').join(out)


    @classmethod
    def _getSourcePaths(cls, otherPaths =None):
        nimbleEntry = MayaEnvEntry.fromRootPath(FileUtils.createPath(
            FileUtils.getDirectoryOf(nimble.__file__), noTail=True) )

        pyaidEntry = MayaEnvEntry.fromRootPath(FileUtils.createPath(
            FileUtils.getDirectoryOf(pyaid.__file__), noTail=True) )

        pyglassEntry = MayaEnvEntry.fromRootPath(FileUtils.createPath(
            FileUtils.getDirectoryOf(pyglass.__file__), noTail=True) )

        additions = [nimbleEntry, pyaidEntry, pyglassEntry]

        if not otherPaths:
            return additions

        for p in otherPaths:
            additions.append(
                p if isinstance(p, MayaEnvEntry) else
                MayaEnvEntry.fromRootPath(p) )

        return additions

#===================================================================================================
#                                                                                 H A N D L E R S


    @classmethod
    def _handleFindEnvFiles(cls, walkData):
        for name in walkData.names:
            if name == 'Maya.env':
                walkData.data.append(FileUtils.createPath(walkData.folder, name))
