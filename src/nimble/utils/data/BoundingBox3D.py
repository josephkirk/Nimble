# BoundingBox3D.py
# (C)2014
# Scott Ernst

import random

#___________________________________________________________________________________________________ BoundingBox3D
class BoundingBox3D(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, xmin =0.0, xmax =0.0, ymin =0.0, ymax=0.0, zmin =0.0, zmax =0.0):
        """Creates a new instance of BoundingBox3D."""
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: deltaX
    @property
    def deltaX(self):
        return self.xmax - self.xmin

#___________________________________________________________________________________________________ GS: deltaY
    @property
    def deltaY(self):
        return self.ymax - self.ymin

#___________________________________________________________________________________________________ GS: deltaZ
    @property
    def deltaZ(self):
        return self.zmax - self.zmin

#___________________________________________________________________________________________________ GS: volume
    @property
    def volume(self):
        return self.deltaX*self.deltaY*self.deltaZ

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ fromExactWorldBoundingBox
    def fromExactWorldBoundingBox(self, bbox):
        """ Populates the bounding values from a list of the form:
            [xmin, ymin, zmin, xmax, ymax, zmax], as returned by the Maya exactWorldBoundingBox
            command. """

        self.xmin = bbox[0]
        self.ymin = bbox[1]
        self.zmin = bbox[2]
        self.xmax = bbox[3]
        self.ymax = bbox[4]
        self.zmax = bbox[5]

#___________________________________________________________________________________________________ getRandomPointInside
    def getRandomPointInside(self):
        """ Returns a tuple representing a 3D point that resides within the bounding box. """

        return (
            self.xmin + self.deltaX*random.random(),
            self.ymin + self.deltaY*random.random(),
            self.zmin + self.deltaZ*random.random() )

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__
