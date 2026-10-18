#!/bin/sh
# Telecharge les livres Gutenberg utilises pour les tests et les benchmarks
mkdir -p tests/data
wget -nc -O tests/data/56667-0.txt https://www.gutenberg.org/files/56667/56667-0.txt