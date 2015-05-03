#!/usr/bin/env python

# Atom Service, Monitor Yes Folder
# --------------------------------

# asset filename: 02_monitor_yes.py
# asset version: 1.0.0
# asset summary: 'Ultra simple test script designed to look at the Yes folder, take an action based on the contents, the drop the file back into the original input folder!!  However the scripts does not actually take any action but prints to stdout (invisible when running in service form). Depending on your configuration, you could run any event you want. Check the commented examples.'

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


# this is the 'Yes' folder we are monitoring
yesfolder_relative = "yes/"

# this is where the original file will get dropped after processing, in order to make the demo completely cyclic
original_inputfolder_relative = "input/" 

yesfolder = os.path.join(test_root_folder, yesfolder_relative)
original_inputfolder = os.path.join(test_root_folder, original_inputfolder_relative)

print "yes folder: " + yesfolder
print "original input folder: " + original_inputfolder

# Begin process
# -------------

# Iterate through all .txt files in the yes folder
for infile in glob.glob(os.path.join(yesfolder, '*.*')):
	splitname = os.path.split(infile)[1]
	print "--------------------------------------------"
	print infile+" requires processing"
	print
	print "Example action: You could run a SQL script like the following on a database: \"INSERT INTO yesfiles (YesFileName) VALUES ('"+splitname+"')\""
	print
	print "Or you could send an email with the subject '"+splitname+" contains the word you looked for', and any other information perhaps taken out of a database or the text file itself"
	print
	shutil.move(os.path.join(yesfolder, infile), original_inputfolder)
# -----------	
# End process	

