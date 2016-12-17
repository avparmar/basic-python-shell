import sys				# used for system stuff
import shlex 			# used for the tokenize function
import os				# used for execution


SHELL_STATUS_RUN = 1	# variables for determining whether 
SHELL_STATUS_STOP = 0   # the loop should run or not

def main():
	shell_main()

def shell_main():
	status = SHELL_STATUS_RUN

	while status == SHELL_STATUS_RUN:
		sys.stdout.write('> ')				# The initial thingy
		sys.stdout.flush()

		nextIn = sys.stdin.readLine()  		# input, received as a line

		if nextIn.find('#') != -1:
			nextIn = nextIn[0:nextIn.find('#')]

		inputWords = tokenize(nextIn)		# tokenized form of the input,
											# allows quick entry to exec and stuff

		status = execute(inputWords)		# execute the input, receive new status

def execute(inputWords):
	pid = os.fork()							# fork!

	if pid == 0:							# if so, this is the child

		os.execvp(inputWords[0],inputWords)		# execute with the following args

	elif pid > 0:							# in the parent process, need to wait
		while True:
			wpid, status = os.waitpid(pid, 0)	# waitpid returns 2 vals, pid and status

			if os.WIFEXTIED(status):		# if weird stuff happens, break
				break

			if os.WIFSIGNALED(status):
				break

	return SHELL_STATUS_RUN					# continue running


def tokenize(inLine):
	return shlex.split(inLine)				# use shlex magic to tokenize


