#!/usr/bin/env python
#=========================================================================
#
#  Copyright Insight Software Consortium
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#=========================================================================

from __future__ import print_function

import SimpleITK as sitk
import sys
import os

if len ( sys.argv ) < 4:
    print( "Usage: "+sys.argv[0]+ " <input> <variance> <output>" )
    sys.exit ( 1 )

class MyCommand(sitk.Command):
    def __init__(self, po):
        # required
        super(MyCommand,self).__init__()
        self.processObject = po

    def Execute(self):
        print("{0} Progress: {1:1.2f}".format(self.processObject.GetName(),self.processObject.GetProgress()))


reader = sitk.ImageFileReader()
reader.SetFileName ( sys.argv[1] )
image = reader.Execute()

pixelID = image.GetPixelIDValue()

gaussian = sitk.DiscreteGaussianImageFilter()
gaussian.SetVariance( float ( sys.argv[2] ) )


#cmd = sitk.PyCommand()
#cmd.SetCommandCallable(lambda: terminal_progress_callback(gaussian.GetName(), gaussian.GetProgress()))
#gaussian.AddCommand(sitk.sitkProgressEvent, lambda: terminal_progress_callback(gaussian.GetName(), gaussian.GetProgress()))
#gaussian.AddCommand(sitk.sitkEndEvent, lambda: terminal_end_callback(gaussian.GetName()))
#gaussian.AddCommand(sitk.sitkProgressEvent, lambda: abort_on(gaussian))
#gaussian.AddCommand(sitk.sitkAbortEvent, lambda: abort())
cmd = MyCommand(gaussian)
gaussian.AddCommand(sitk.sitkProgressEvent, cmd)
image = gaussian.Execute ( image )

caster = sitk.CastImageFilter()
caster.SetOutputPixelType( pixelID )
image = caster.Execute( image )

writer = sitk.ImageFileWriter()
writer.SetFileName ( sys.argv[3] )
writer.Execute ( image );


if ( not "SITK_NOSHOW" in os.environ ):
    sitk.Show( image, "Simple Gaussian" )