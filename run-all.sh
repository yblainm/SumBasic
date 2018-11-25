#!/usr/bin/env bash

parallel py sumbasic.py {1} ./docs/doc{2}-*.txt > {1}-{2}.txt :::: methods ::: seq 1 4
