#! /bin/bash
for i in ficeri_glb/*; do cat $i; echo -ne "\n"; done |tee baza.csv
