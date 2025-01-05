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
    proteins = []
    with open(hmm_results, 'r') as file:
        for line in file:
            if not line.startswith("#") and line.strip():
                proteins.append(line.split()[0])  # Extract matched protein ID

    try:
        # Load InterPro mapping file using the Python engine for better compatibility
        ipr_data = pd.read_csv(protein2ipr, sep="\t", header=None, names=["UniProt_ID", "InterPro_ID"], engine="python")
    except Exception as e:
        print(f"Error reading InterPro mapping file: {e}")
        return

    # Map proteins to InterPro IDs
    matched_ipr = ipr_data[ipr_data["UniProt_ID"].isin(proteins)]

    # Append results to the output file
    matched_ipr.to_csv(output_file, sep="\t", index=False, mode='a', header=not os.path.exists(output_file))

def main():
    # Paths configuration
    hmm_dir = "database/GyDB"               # Directory containing HMM files
    protein_db = "database/uniprot_sprot.fasta"   # Path to protein database
    output_dir = "results/hmmsearch"        # Directory for HMMER output
    protein2ipr = "database/protein2ipr.dat" # InterPro mapping file
    final_output = "results/interpro_ids.tsv"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Clear final output file if it already exists
    if os.path.exists(final_output):
        os.remove(final_output)

    # List all HMM files in the directory
    hmm_files = [f for f in os.listdir(hmm_dir) if f.endswith(".hmm")]
    print(f"Found {len(hmm_files)} HMM files to process.")

    # Process each HMM file
    for i, hmm_file in enumerate(hmm_files, start=1):
        print(f"Processing {i}/{len(hmm_files)}: {hmm_file}")
        hmm_path = os.path.join(hmm_dir, hmm_file)
        try:
            # Run HMMER search
            hmm_results = run_hmmsearch(hmm_path, protein_db, output_dir)
            # Map to InterPro IDs
            map_to_interpro(hmm_results, protein2ipr, final_output)
            print(f"Completed processing {hmm_file}")
        except Exception as e:
            print(f"Error processing {hmm_file}: {e}")

if __name__ == "__main__":
    main()
