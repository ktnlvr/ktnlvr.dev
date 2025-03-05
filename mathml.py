#!/usr/bin/python
import os
import re

import subprocess

if __name__ == "__main__":
    for root, dirs, files in os.walk("./public"):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                with open(path, "r+") as f:
                    content = f.read()

                    pandoc = [
                        "pandoc",
                        "-f",
                        "html+tex_math_dollars",
                        "-t",
                        "html",
                        "--mathml",
                    ]
                    proc = subprocess.Popen(
                        pandoc, stdout=subprocess.PIPE, stdin=subprocess.PIPE
                    )
                    proc.stdin.write(content.encode())
                    proc.stdin.close()
                    replacement = proc.stdout.read().decode().strip()
                    f.seek(0)
                    f.write(replacement)
