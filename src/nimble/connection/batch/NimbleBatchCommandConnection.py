# NimbleBatchCommandConnection.py
# (C)2013 http://www.ThreeAddOne.com
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import functools

from nimble.connection.NimbleConnection import NimbleConnection


class NimbleBatchCommandConnection(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S


    def __init__(self):
        """Creates a new instance of NimbleBatchCommandConnection."""
        self._batch = []

#===================================================================================================
#                                                                                     P U B L I C


    def sendCommandBatch(self):
        conn = NimbleConnection.getConnection()
        return conn.mayaBatch(self._batch)

#===================================================================================================
#                                                                               P R O T E C T E D


    def _mayaCommand(self, item, *args, **kwargs):
        self._batch.append({'command':item, 'args':args, 'kwargs':kwargs})

#===================================================================================================
#                                                                               I N T R I N S I C


    def __getattr__(self, item):
        if item.startswith('_'):
            raise AttributeError

        return functools.partial(self._mayaCommand, item)


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return '<%s>' % self.__class__.__name__
