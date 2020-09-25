from termcolor import cprint

'''
	Prints error without shutting down
	Parameters:
		msg (string): Error message to print
	Returns:
		None
'''
def print_error(msg):
    cprint(f'\n{msg}\n', 'red')

''' 
	Shuts down the script.
	Parameters:
		msg (string): Message to print before printing 'Shutting down...' and exiting the script.
	Returns:
		None
'''
def shut_down(msg):

    cprint(f'\n{msg}\n', 'red')
    print('Shutting down...')
    sys.exit()