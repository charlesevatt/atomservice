#!/usr/bin/env python

# Atom Service
# ------------

# asset filename: as.democonfig.py
# asset version: 1.0.0
# asset summary: 'Part of a demonstration configuration showing a very simple example usage of the Atom Service daemon. Includes some customisations to the configuration file.'

# Copyright (c) 2010, VIAVIA Solutions Ltd.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the name of the VIAVIA Solutions Ltd. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Please visit http://code.google.com/p/atomservice/ for further information about this project.

#-----------------------------------------------------------------------------------------------------------------------------------------

import os
from logging import DEBUG,INFO,WARNING,ERROR,CRITICAL

class AtomExe:
	"""Class : Exe

	name - set the process name.
	scriptpath - Full path to an executable. If a script , it should be executable by itself. 
			 Can be given paths to binaries too.
	args - array of arguments for eg :- ['-l','/tmp']

	"""
	def __init__(self,name,filename,args):
		self.name = name
		self.scriptpath = filename
		self.args = args

##################  USER CONFIGURATION STARTS #########################################

#POLL_INTERVAL :- Atom Service daemon sleeps for POLL_INTERVAL seconds, once all processes 
#are executed. Set this to a non-negative value. Use zero to disable sleep.
POLL_INTERVAL = 5

#PROC_INTERVAL : Similar to POLL_INTERVAL, this value specifies the 
# inter-process sleep.
PROC_INTERVAL = 15

# AUDIT_LEVEL : Set the level of logging. 
# DEBUG > INFO > WARNING > ERROR > CRITICAL
#NB: No quotes needed around the logging level name. 

AUDIT_LEVEL = DEBUG 

#Set the name of the created Atom Service daemon. This will appear in the process list. 
NAME='atomservice.demo'

#Array containing the list of processes to execute in order. 
PROC_LIST=[]

# for the purpose of the demo, we've included a root path here. Change this to the path into which you unpacked the demo scripts/folders

demo_root_process_path = '/home/charlie/automation/as_demo/02_processes/'

# Importantly, note if you call scripts directly without calling their executing application (e.g. python or bash) then the scripts need to have executable permissions.

PROC_LIST.append( AtomExe('as.01_searchforyes',os.path.abspath(demo_root_process_path+'01_search_for_yes.py'), []) )
PROC_LIST.append( AtomExe('as.02_monitoryes',os.path.abspath(demo_root_process_path+'02_monitor_yes.py'), []) )
PROC_LIST.append( AtomExe('as.03_monitorno',os.path.abspath(demo_root_process_path+'03_monitor_no.py'), []) )

###############################################################################################
