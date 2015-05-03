#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Atom Service
# ------------

# asset filename: atomservice.py
# asset version: 1.0.2
# asset summary: 'Python module which creates a custom named process, executes a sequence of processes in order, whilst creating its own audit log. All configurable by using a configuration file.'

# Aug 10, 2011: Removed deprecated os.spawnvp previously called to spawn sub-process. Now uses subprocess.call. Compatible with RHEL 6, Python 2.6.5

# Copyright (c) 2010, VIAVIA Solutions Ltd.
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the name of the VIAVIA Solutions Ltd. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Please visit http://code.google.com/p/atomservice/ for further information about this project.

#-----------------------------------------------------------------------------------------------------------------------------------------

import sys, os, time, atexit
from signal import SIGTERM,SIGUSR1,SIGUSR2 
import logging
#import proctitle
import procname
import signal,errno
import subprocess

def waitpid_nointr(pid,options):
	"""waitpid function in python gets interrupted and raises exception when a signal is received.
	for eg:- SIGTERM sent by stop command.
	This function restarts waitpid on interruption"""

	while True:
		try:
			return os.waitpid(pid,options)
		except OSError,e:
			if e.errno == errno.EINTR:
				continue
			elif e.errno == errno.ECHILD: #No Child process. waitpid is not needed. Return. 
				return 
			else:
				return #TO DECIDE: return or raise ?? 

class Daemon:
	def __init__(self, name='as.daemon', pidfile='/tmp/as.daemon.pid',logfile='/tmp/as.logfile.log',stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', logLevel=logging.DEBUG):
		self.name = name
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
		self.logfile=logfile

		format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
		logging.basicConfig(filename=self.logfile,level=logging.DEBUG,format=format)
		self.logger = logging.getLogger(self.name)

		self.logger.info("Setting Log Level to " + logging.getLevelName(logLevel) )
		self.logger.setLevel(logLevel)

#		Functions for proctitle
#		self.Argv = proctitle.ProcTitle()
#		self.Argv.save()


	
	def daemonize(self):
		"""
		do the UNIX double-fork magic,  
		"""
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit first parent
				sys.exit(0) 
		except OSError, e: 
			self.logger.error("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
			sys.exit(1)
	
		# decouple from parent environment
#		os.chdir("/") 
		os.setsid() 
		os.umask(0) 
	
		# do second fork
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit from second parent
				sys.exit(0) 
		except OSError, e: 
			self.logger.error("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
			sys.exit(1) 
	
		# redirect standard file descriptors
		procname.setprocname(self.name)
		#self.Argv[0:]=self.name #for proctitle module. 
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# write pidfile
		atexit.register(self.delpid) #Delete the pidfile on exit. 
		pid = str(os.getpid())
		file(self.pidfile,'w+').write("%s\n" % pid)
	
	def delpid(self):
		"""Deletes the pid file. Usually called on exit"""
		os.remove(self.pidfile)

	def start(self):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already runs
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if pid:
			message = "pidfile %s already exists. Is the Atom Service daemon already running?"
			self.logger.error(message % self.pidfile)
			sys.exit(1)
		self.logger.info("Started")	
		# Start the daemon
		self.daemonize()
		try:
			self.run()
		except SystemExit:
			"""Normal SystemExit called from one of the inner functions. Ignore"""
			pass
		except:
			"""Got an exception from the run function. Print the traceback and exit with value 1"""
			import traceback
			self.logger.error("Caught exception in run section.")
			type,value,error = sys.exc_info()
			error = traceback.extract_tb(error)
			self.logger.critical(" %s, %s "%(type.__name__, value))
			self.logger.critical(error)
			self.logger.error("Exiting...")
			sys.exit(1)

	def stop(self):
		"""
		Stop the daemon
		"""
		self.logger.info("Sending stop signal")	
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if not pid:
			message = "pidfile %s does not exist. Is the Atom Service daemon not running?"
			self.logger.error(message % self.pidfile)
			return # not an error in a restart

		# Try killing the daemon process	
		os.kill(pid, SIGTERM)
		try:
			while 1: #Now making sure the process to exit.
			# Sending an harmless SIGUSR1 signal to check the status. 
				os.kill(pid, SIGUSR1)
				self.logger.info("Waiting for %s to stop..."%self.name)
				time.sleep(5)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()

	def run(self):
		"""Default run function. Overload this for your purpose"""
		id = 1
		while id > 1 :
			time.sleep(15)
			self.logger.info("Polling - %d"%id)
			++id


class ProcDaemon(Daemon):
	"""Derived from Daemon class. 
	Parses a config file for a list of processes and executes them in loop"""

	def __init__(self, configfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null',logLevel='DEBUG'):

		self.configfile = os.path.abspath(configfile) #Create the absolute path from the config file given. 

		#Initialize default config values
		self.config = { 'NAME' : 'procdaemon', 'PROC_LIST' : [], 'PROC_INTERVAL' : 5, 'POLL_INTERVAL' : 60 , 'AUDIT_LEVEL' : logLevel,
                        'LOGFOLDER' : '/tmp', 'PIDFOLDER' : '/tmp'
		              } 

		self.runDaemon = True #Variable is set to false on reception of stop command. 
		self.currentProc=None #Information about current running process. 

		execfile(self.configfile, self.config) #Parse the config file and store in self.config. 

		self.name = self.config['NAME'].strip()
		self.logfolder = self.config['LOGFOLDER']
		self.pidfolder = self.config['PIDFOLDER']
		
		if not os.access( self.logfolder, os.W_OK ):
			sys.stderr.write("logfolder (%s) is not writable. Can't continue." % self.logfolder)
			sys.exit(1)

		if not os.access( self.logfolder, os.W_OK ):
			sys.stderr.write("pidfolder (%s) is not writable. Can't continue." % self.pidfolder)
			sys.exit(1)
		
		if self.name:
			pidfilename = self.name.split()[0]
			self.pidfile = os.path.join( self.pidfolder, pidfilename+'.pid' )
			self.logfile = os.path.join( self.logfolder, pidfilename+'.log' )
		else:
			self.name = "as.daemon"
			self.pidfile = os.path.join( self.pidfolder, 'as.daemon.pid' )
			self.logfile = os.path.join( self.logfolder, 'as.daemon.log' )
		Daemon.__init__(self,self.name,self.pidfile,self.logfile,stdin,stdout,stderr,self.config['AUDIT_LEVEL'])
		

	def quit(self):
		"""Handler for stop command"""
		self.runDaemon = False
		if self.currentProc == None : 
			#No processes are running. Call exit. 
			self.logger.info("Got Stop Command: Exiting ...")
			sys.exit(0)
		else:
			self.logger.info("Got Stop Command: Waiting for process %s to exit"%self.currentProc)

	def doNothing(self): #Handler for SIGUSR1 signal
		pass

	def run(self):
		"""Executes the processes in the self.config.PROC_LIST in a sequential manner.
		When stop command (SIGTERM) is received, it waits for the current process to exit, if any, is running"""

		signal.signal(signal.SIGTERM,  lambda *args: self.quit())
		signal.signal(signal.SIGUSR1,  lambda *args: self.doNothing())

		while True:
			for process in self.config['PROC_LIST']:
				self.logger.info("Executing %s"%process.name)
				self.currentProc=process.name #Set the current running process. 
#				subprocess.call([process.scriptpath] +  process.args)
				pid = os.fork()
				if pid == 0:
					if self.logger.getEffectiveLevel() <= logging.DEBUG:
						#cmdLine = process.scriptpath
						cmdLine = ''
						for arg in process.args:
							cmdLine += " " + str(arg)
						#self.logger.debug("Running command :- " + cmdLine)

					#os.spawnvp(os.P_WAIT,process.scriptpath, [process.scriptpath] +  process.args)
					self.logger.debug("CALLING COMMAND: "+process.scriptpath+" with ARGS: "+ cmdLine)
					subprocess.call(process.scriptpath+cmdLine, shell=True)
					os._exit(0)
				elif pid > 0:
					waitpid_nointr(pid,0) 
				else:
					raise OSError, "Fork failed"
				
				self.logger.info("Finished %s"%process.name)
				self.currentProc=None

				if not self.runDaemon: #Checking for a stop signal received while the process was running. 
				#runDaemon variable changed by quit() function.
					self.logger.info("Exiting ...")
					sys.exit(0)
				#Inter process sleep.
				self.logger.info("Sleeping %d seconds"%self.config['PROC_INTERVAL'])
				time.sleep(self.config['PROC_INTERVAL'])

			#Polling Interval.
			self.logger.info("All processes executed. Sleeping %d seconds"%self.config['POLL_INTERVAL'])	
			time.sleep(self.config['POLL_INTERVAL'])

			self.logger.info("Reloading configuration")
			execfile(self.configfile,self.config)
			if self.logger.getEffectiveLevel() != self.config['AUDIT_LEVEL']:
				self.logger.info("Setting Log Level " + logging.getLevelName(self.config['AUDIT_LEVEL']) )
				self.logger.setLevel( self.config['AUDIT_LEVEL'] )

			self.logger.info("Restarting execution loop")


