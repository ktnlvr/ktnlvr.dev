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
                    begins = (b.end() for b in re.finditer("<p>\[", content))
                    ends = (e.start() for e in re.finditer("\]</p>", content))
                    substrings = list(zip(begins, ends))
                    d = 0

                    for s in substrings:
                        slice = (
                            "$$"
                            + (
                                content[s[0] : s[1]]
                                .replace("<p>", "")
                                .replace("</p>", "")
                                .strip()
                            )
                            + "$$"
                        )

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
                        proc.stdin.write(slice.encode())
                        proc.stdin.close()
                        replacement = proc.stdout.read().decode().strip()

                        new_content = content[:s[0] + d - 1] + replacement + content[s[1] + d + 1:]
                        d += len(replacement) - len(slice)
                        f.seek(0)
                        f.write(new_content)
