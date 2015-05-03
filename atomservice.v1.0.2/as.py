#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Atom Service
# ------------

# asset filename: as.py
# asset version: 1.0.2
# asset summary: 'This is the script called to control an Atom Service instance. Example: python as.py as.config.py start'

# Copyright (c) 2010, VIAVIA Solutions Ltd.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the name of the VIAVIA Solutions Ltd. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Please visit http://code.google.com/p/atomservice/ for further information about this project.

#-----------------------------------------------------------------------------------------------------------------------------------------

import sys, time
from atomservice import ProcDaemon

if __name__ == "__main__":
	if len(sys.argv) == 3:
		atomservice_instance = ProcDaemon(sys.argv[1])
		if 'start' == sys.argv[2]:
			atomservice_instance.start()
		elif 'stop' == sys.argv[2]:
			atomservice_instance.stop()
		elif 'restart' == sys.argv[2]:
			atomservice_instance.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage:"
		print "\t%s configfile start|stop|restart" % sys.argv[0]
		sys.exit(2)
