import sys

if __name__ == "__main__":
    try:
        for line in sys.stdin:
            sys.stdout.write(line)
            sys.stdout.flush()
    except:
        sys.stderr.write("FileCheck failed")
        sys.exit(1)
