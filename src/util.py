from termcolor import cprint
import sys

def print_error(msg):
    '''
    Prints error without shutting down
    Parameters:
        msg (string): Error message to print
    Returns:
        None
    '''
    cprint(f'\n{msg}\n', 'red')


def shut_down(msg):
    ''' 
    Shuts down the script.
    Parameters:
        msg (string): Message to print before printing 'Shutting down...' and exiting the script.
    Returns:
        None
    '''
    cprint(f'\n{msg}\n', 'red')
    print('Shutting down...')
    sys.exit()

def print_success(msg):
    '''
    Prints success message
    Parameters:
        msg (string): Success message to print
    Returns:
        None
    '''
    cprint(f'\n{msg}\n', 'green')
