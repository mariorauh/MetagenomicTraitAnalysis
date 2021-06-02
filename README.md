# MetagenomicTraitAnalysis

Version: v0.0.1

## What to use it for?

The Metagenomic Trait Analysis can be used to analyse your Megan KEGG name to Count data. 

## Prerequisites

This program is written Python and requires Python 3.6+. Furthermore, the following packages are required:

```
setuptools~=49.6.0
pandas~=1.2.4
matplotlib~=3.4.1
numpy~=1.19.2
scipy~=1.6.2
```

## Options

No Internet connection is required to run the program.

### Input

```
-i INPUT [INPUT ...], --input INPUT [INPUT ...]
```

Use this to import your exported [Megan6](https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/lehrstuehle/algorithms-in-bioinformatics/software/megan6/) files. Export the required file from Megan6 by opening the KEGG viewer in the main panel. From there, uncollapse the annotation tree (Top-Panel => Tree => Uncollapse All) and select all nodes and leaves (Ctrl/Cmd + a). From the Top-Panel, choose *File* and move the cursor to *Export* and click on *Text (CSV) Format*. Export *eggnogName_to_count* and separator *comma*. The file that is then exported can be used for the analysis.

Multiple files can be added, only separated by a space.

### Output

```
-o OUTPUT, --output OUTPUT
```

Choose a valid output Path and name.

### Top N

```
-t TOP, --top TOP
```

Optional: Include this flag together with a positive number (Note: neg. numbers will be converted to pos) to choose your own top N annotations to be analyzed in the heatmap. Default is 10.

Note: For a better readability, the maximum depends on how many input files are given and how many high scoring traits they have in common. It is suggested to start with the default value and increase it with every run.
