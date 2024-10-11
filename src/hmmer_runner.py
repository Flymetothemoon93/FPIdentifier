import subprocess
import os

def extract_contig_name(fasta_file):
    """
    Extracts the contig or chromosome name from the input FASTA file by parsing 'chr=' field in the header.
    
    Parameters:
    - fasta_file (str): Path to the input FASTA file.
    
    Returns:
    - str: Contig or chromosome name extracted from the first sequence header.
    """
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                contig_name = line.split()[2]
                if contig_name.startswith("chr="):
                    contig_name = contig_name.split("=")[-1]
                    return contig_name

    return None

def run_hmmer(protein_sequences, output_file, contig_name):
    """
    Runs the HMMER tool to scan the provided protein sequences using HMM models from GyDB.
    
    Parameters:
    - protein_sequences (str): Path to the input protein sequences in FASTA format.
    - output_file (str): Path where the hmmer_results.txt should be saved.
    - contig_name (str): Contig or chromosome name extracted from the input file.
    
    Returns:
    - None: Outputs the results to a file in the specified output path.
    """
    # Define the HMM model directory
    hmm_model_dir = 'database/GyDB'

    # Ensure the output directory exists (from the file path)
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the output file for writing results
    with open(output_file, 'w') as f_out:
        # Iterate through all .hmm files again to run hmmscan
        for hmm_file in os.listdir(hmm_model_dir):
            if hmm_file.endswith('.hmm'):
                hmm_file_path = os.path.join(hmm_model_dir, hmm_file)
                
                # Print both processing and completed status
                print(f"Processing HMM file: {hmm_file_path}")
                
                # Construct the HMMER command for each HMM file
                cmd = f"hmmscan --domtblout /dev/stdout {hmm_file_path} {protein_sequences}"
                try:
                    # Run HMMER and capture the results
                    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                    for line in result.stdout.splitlines():
                        # Filter the actual data lines, skipping comments
                        if not line.startswith('#'):
                            fields = line.strip().split()
                            # Ensure the line has enough fields to replace
                            if len(fields) > 0:
                                # Replace the first column (target name) with the extracted contig name
                                fields[0] = contig_name
                                # Write the modified result to the output file
                                f_out.write("\t".join(fields) + "\n")
                    
                    # Print completion message
                    print(f"Completed HMM file: {hmm_file_path}")
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"HMMER failed with error: {e}")
    
    print(f"HMMER process for {protein_sequences} finished. Results saved to {output_file}")
