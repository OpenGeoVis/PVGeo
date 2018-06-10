from __future__ import print_function

__all__ = ['printProgressBar']

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='#'):
    """
    @desc: Call in a loop to create terminal progress bar
    @params:
        iteration: int : required : current iteration
        total : int : required : total iterations
        prefix : str : ptional  : prefix string
        suffix : str : optional  : suffix string
        decimals : int : optional  : positive number of decimals in percent complete
        length : int : optional  : character length of bar
        fill : str : optional  : bar fill character

    Example Use:
    printProgressBar(i, len(arr), prefix = 'Progress:', suffix = 'Complete', length = 50)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()
