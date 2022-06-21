#!/usr/bin/env bash

docker run -it -v $(pwd):/usr/src/myapp -w /usr/src/myapp python:3.2.6 python hfnsurf.py
