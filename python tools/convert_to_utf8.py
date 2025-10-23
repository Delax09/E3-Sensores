import os, sys

def try_convert(path, src_encs=("utf-8","cp1252","latin-1")):
    for enc in src_encs:
        try:
            with open(path, "r", encoding=enc) as r:
                data = r.read()
            with open(path, "w", encoding="utf-8") as w:
                w.write(data)
            print("Converted", path, "from", enc, "-> utf-8")
            return True
        except Exception:
            continue
    print("Failed to convert", path)
    return False

root = sys.argv[1] if len(sys.argv) > 1 else "."
for dirpath, _, files in os.walk(root):
    for f in files:
        if f.endswith((".py", ".csv", ".txt")):
            try_convert(os.path.join(dirpath,f))