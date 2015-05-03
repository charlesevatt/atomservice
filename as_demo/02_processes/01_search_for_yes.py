#!/usr/bin/env python

# Atom Service, Simple Demo Script 01
# ------------

# asset filename: 01_search_for_yes.py
# asset version: 1.0.0
# asset summary: 'Ultra simple test script designed to look at text files in an input folder and move them to a particular output folder depending on finding a search word'

# Copyright (c) 2010, VIAVIA Solutions Ltd.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the name of the VIAVIA Solutions Ltd. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Please visit http://code.google.com/p/atomservice/ for further information about this project.

#-----------------------------------------------------------------------------------------------------------------------------------------


import glob
import os
import shutil

# Test root folder - change this path to something on your system, of course.

test_root_folder = "/home/charlie/automation/as_demo/watchfolders/"

# relative watch/output folders

inputfolder_relative = "input/"

yesfolder_relative = "yes/"
nofolder_relative = "no/"

inputfolder = os.path.join(test_root_folder, inputfolder_relative)
yesfolder = os.path.join(test_root_folder, yesfolder_relative)
nofolder = os.path.join(test_root_folder, nofolder_relative)

print "input: " + inputfolder
print "yes folder: " + yesfolder
print "no folder: " + nofolder

# Word to look for

searchword = "Yes"

# Begin process
# -------------

# Iterate through all .txt files in input folder
for infile in glob.glob(os.path.join(inputfolder, '*.txt')):
	fref=file(infile)
	found = False
	# Search through each file for the searchword
	for line in fref:
		if (searchword in line) and (line!=''):
			found = True
	# Drop into yesfolder or nofolder based on whether search word was found.
	if found == True:
		print "Found '"+searchword+"' in "+infile+" - moving to "+yesfolder
		print
		shutil.move(os.path.join(inputfolder, infile), yesfolder)
	else:
		print "Did not find '"+searchword+"' in "+infile+" - moving to "+nofolder+"\n"
		print
		shutil.move(os.path.join(inputfolder, infile), nofolder)

# -----------	
# End process	

