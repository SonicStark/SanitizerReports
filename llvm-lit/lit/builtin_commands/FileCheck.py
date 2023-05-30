import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-input-file",  type=str, required=False)
    parser.add_argument("--input-file", type=str, required=False)
    params,_ = parser.parse_known_args()

    try:
        if (params.input_file is None):
            for line in sys.stdin:
                sys.stdout.write(line)
                sys.stdout.flush()
        else:
            with open(params.input_file, mode="r") as f:
                sys.stdout.write(f.read())
                sys.stdout.flush()
    except:
        sys.stderr.write("FileCheck failed\n")
        sys.exit(1)
