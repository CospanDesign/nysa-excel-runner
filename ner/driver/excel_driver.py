#Distributed under the MIT licesnse.
#Copyright (c) 2015 Dave McCoy (dave.mccoy@cospandesign.com)

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

"""
Facilitates communication with the an arbitraty core, user must pass in an
SDB Component to initialize this device

"""

__author__ = "dave.mccoy@cospandesign.com (Dave McCoy)"

import sys
import os
import time
from array import array as Array

from nysa.host.driver.driver import Driver


class ExcelDriver(Driver):

    def get_abi_class(self):
        return self.platform.get_abi_class(self.urn)

    def get_abi_major(self):
        return self.platform.get_abi_major(self.urn)

    def get_abi_minor(self):
        return self.platform.get_abi_minor(self.urn)

    def get_vendor_id(self):
        return self.platform.get_vendor_id(self.urn)

    def get_version(self):
        return self.platfrom.get_version(self.urn)

    def get_date(self):
        return self.platform.get_date(self.urn)

    def __init__(self, platform, urn, status):
        print "Platform: %s" % str(platform)
        self.status = status
        print "entered init!"
        super (ExcelDriver, self).__init__(platform, urn, False)
