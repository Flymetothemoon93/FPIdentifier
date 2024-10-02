# FPIdentifier
This project focuses on identifying transposable elements (TEs) that are misidentified as genes in genomic annotations. The tool uses **HMMER** to compare protein sequences against the **REXdb** database and detects potential transposon-related domains.

## How to Use

1. Clone the repository:
```bash
git clone https://github.com/Flymetothemoon93/FPIdentifier.git
 ```bash

2. Install required Python packages:
 ```bash
pip install -r requirements.txt
 ```bash

3. Prepare your input protein sequence file in FASTA format.

4. Run the tool with your input file:
 ```bash
python src/main.py --input your_protein_sequences.fasta --output results
 ```bash
