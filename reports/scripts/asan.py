import io
import json
import os

REPORT_ENV_NAME = "SANREPORT"
OUTPUT_ENV_NAME = "SANOUTPUT"

def asan_go():
    report_path = os.getenv(REPORT_ENV_NAME)
    if report_path and os.path.isfile(report_path):
        report_path = os.path.abspath(report_path)
    else:
        raise IOError("Invalid file: '%r'"%report_path)
    
    output_path = os.getenv(OUTPUT_ENV_NAME);
    if output_path and os.path.isdir(output_path):
        output_path = os.path.abspath(output_path)
    else:
        raise IOError("Invalid dir: '%r'"%report_path)
    
    results = []
    with open(report_path, mode="r") as f:
        big_guy = json.load(f)
        for d in big_guy["tests"]:
            results.append([d["name"], d["output"]])

    for r in results:
        if  (len(r[0]) == 0) or \
            (r[1] == "Test is unsupported") or \
            ("-Unit " in r[0]) :
            continue

        out_dst = os.path.join(output_path,
                    r[0].split("::")[1].strip().lstrip("TestCases/") + ".txt")
        out_dir = os.path.dirname(out_dst)

        os.makedirs(out_dir, exist_ok=True)

        with io.StringIO() as ibuf, open(out_dst, mode="w") as obuf:
            ibuf.write(r[1])
            ibuf.seek(0)

            state = 0
            for line in ibuf:
                if   (state == 0):
                    if (line[:16] == "Command Output ("):
                        state = 1
                elif (state == 1):
                    if (line[:2] == "--"):
                        state = 2
                        obuf.write("\n\n>>HEAD>> %s <<HEAD<<\n\n"%r[0])
                elif (state == 2):
                    if (line[:2] == "--"):
                        state = 0
                        obuf.write("\n\n>>TAIL>> %s <<TAIL<<\n"%r[0])
                    else:
                        obuf.write(line)

        print("[*] Write %s"%out_dst)

if __name__ == "__main__":
    asan_go()