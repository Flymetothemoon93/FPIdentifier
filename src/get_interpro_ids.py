import os
import subprocess
import pandas as pd

def run_hmmsearch(hmm_file, protein_db, output_dir):
    """
    Use HMMER to scan the protein database and output results to a file with 24 threads.
    """
    output_file = os.path.join(output_dir, os.path.basename(hmm_file).replace(".hmm", "_results.tbl"))
    cmd = f"hmmsearch --tblout {output_file} --cpu 24 {hmm_file} {protein_db}"
    subprocess.run(cmd, shell=True, check=True)
    return output_file

def map_to_interpro(hmm_results, protein2ipr, output_file):
    """
    Extract matched protein IDs from HMMER results and map them to InterPro IDs.
    """
    # Parse HMMER results and extract protein IDs
    proteins = []
    with open(hmm_results, 'r') as file:
        for line in file:
            if not line.startswith("#") and line.strip():
                proteins.append(line.split()[0])  # Extract matched protein ID

    # Load InterPro mapping file
    ipr_data = pd.read_csv(protein2ipr, sep="\t", header=None, names=["UniProt_ID", "InterPro_ID"])
    matched_ipr = ipr_data[ipr_data["UniProt_ID"].isin(proteins)]

    # Save results
    matched_ipr.to_csv(output_file, sep="\t", index=False)
    print(f"InterPro ID mapping results saved to {output_file}")

def main():
    # Configure paths
    hmm_dir = "database/GyDB"               # Directory containing HMM files
    protein_db = "database/uniprot_sprot.fasta"   # Path to protein database
    output_dir = "results/hmmsearch"        # Directory for HMMER output
    protein2ipr = "database/protein2ipr.dat" # InterPro mapping file
    final_output = "results/interpro_ids.tsv"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Run HMMER and map to InterPro IDs for each HMM file
    for hmm_file in os.listdir(hmm_dir):
        if hmm_file.endswith(".hmm"):
            hmm_path = os.path.join(hmm_dir, hmm_file)
            hmm_results = run_hmmsearch(hmm_path, protein_db, output_dir)
            map_to_interpro(hmm_results, protein2ipr, final_output)

if __name__ == "__main__":
    main()
