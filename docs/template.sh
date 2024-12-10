#!/bin/zsh
for i in {1..10}; do
    touch "lab$i.md"
    echo "lab$i.md created"
    echo "# Lab $i" > "lab$i.md"
    echo "## 实验介绍" >> "lab$i.md"
    echo "## 实验原理" >> "lab$i.md"
    echo "## 实验步骤" >> "lab$i.md"
done