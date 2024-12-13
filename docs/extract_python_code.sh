#!/bin/zsh
for file in $(find . -name "*.md"); do
    echo "Extracting python code from $file"
    cat $file | grep -E '```python' -A 1000 | grep -E '```' -B 1000 | grep -v '```' > ../code/$file.py
done