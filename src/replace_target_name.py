import re

def replace_target_with_contig(hmmer_results_file, output_file, fasta_file):
    """
    Replaces the target name in the HMMER results file with the corresponding contig name from the FASTA headers.

    Parameters:
    - hmmer_results_file (str): Path to the HMMER output results (domtblout format).
    - output_file (str): Path to save the modified results.
    - fasta_file (str): Path to the input FASTA file containing contig information.

    Returns:
    - None
    """
    # Step 1: Create a dictionary to map query names to contig names from the FASTA file
    query_to_contig = {}
    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            if line.startswith('>'):
                header = line.strip().split()[0][1:]  # Remove '>' and keep the sequence ID
                match = re.search(r'chr=(\S+)', line)  # Extract contig name
                if match:
                    contig_name = match.group(1)
                    query_to_contig[header] = contig_name

    # Step 2: Process the HMMER results and replace the target name
    with open(hmmer_results_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            if line.startswith('#'):  # Keep comment lines as is
                outfile.write(line)
            else:
                fields = line.strip().split()
                if len(fields) > 3:
                    query_name = fields[3]  # Get the query name from the 4th column
                    if query_name in query_to_contig:
                        contig_name = query_to_contig[query_name]
                        fields[0] = contig_name  # Replace the first field with the contig name
                    else:
                        print(f"Warning: Query name {query_name} not found in the FASTA file.")
                    outfile.write("\t".join(fields) + "\n")
                else:
                    outfile.write(line)

    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python replace_target_name.py <hmmer_results.txt> <output.txt> <input.fasta>")
        sys.exit(1)
    
    hmmer_results_file = sys.argv[1]
    output_file = sys.argv[2]
    fasta_file = sys.argv[3]
    
    replace_target_with_contig(hmmer_results_file, output_file, fasta_file)