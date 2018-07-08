if __name__ == '__main__':
    import sys
    from .__tester__ import test
    arg = sys.argv[1]
    if arg.lower() == 'test':
        test(True)
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
