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

                    # even worse than parsing HTML with regex, but hopefully reliable
                    head, begin, body = content.partition("<body>")
                    body, end, tail = body.partition("</body>")

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
                    proc.stdin.write(body.encode())
                    proc.stdin.close()
                    body = proc.stdout.read().decode().strip()
                    f.seek(0)
                    f.write("".join([head, begin, body, end, tail]))
