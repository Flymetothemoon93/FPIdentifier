import subprocess
import os

def run_hmmer(protein_sequences, output_file, e_value_threshold=1e-5):
    """
    Runs the HMMER tool to scan the provided protein sequences using HMM models from GyDB.
    
    Parameters:
    - protein_sequences (str): Path to the input protein sequences in FASTA format.
    - output_file (str): Path where the hmmer_results.txt should be saved.
    
    Returns:
    - None: Outputs the results to a file in the specified output path.
    """

    # Define the HMM model directory
    hmm_model_dir = 'database/GyDB'

    # Ensure the output directory exists (from the file path)
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate through all .hmm files in the GyDB directory and run hmmpress first
    for hmm_file in os.listdir(hmm_model_dir):
        if hmm_file.endswith('.hmm'):
            hmm_file_path = os.path.join(hmm_model_dir, hmm_file)
            
            # Check if .h3m file (generated by hmmpress) exists, if not, run hmmpress
            h3m_file = hmm_file_path + ".h3m"
            if not os.path.exists(h3m_file):
                print(f"Running hmmpress on {hmm_file_path}")
                cmd_hmmpress = f"hmmpress {hmm_file_path}"
                try:
                    subprocess.run(cmd_hmmpress, shell=True, check=True)
                    print(f"hmmpress completed for {hmm_file_path}")
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"hmmpress failed with error: {e}")

    # Open the output file for writing results
    with open(output_file, 'w') as f_out:
        # Iterate through all .hmm files again to run hmmscan
        for hmm_file in os.listdir(hmm_model_dir):
            if hmm_file.endswith('.hmm'):
                hmm_file_path = os.path.join(hmm_model_dir, hmm_file)
                print(f"Processing HMM file: {hmm_file_path}")
                
                # Construct the HMMER command for each HMM file
                cmd = f"hmmscan --domtblout /dev/stdout {hmm_file_path} {protein_sequences}"
                try:
                    # Run HMMER and append the results to the output file
                    cmd = subprocess.run(cmd, shell=True, capture_output=True)
                    print(f"Completed HMM file: {hmm_file_path}")
                    for line in cmd.stdout.decode():
                        #####remember remove！！！！
                        if float(line.split()[6]) < e_value_threshold:
                        #####remember remove！！！！
                            output_file.write(line)
                            output_file.flush()
                except subprocess.CalledProcessError as e:
                    raise RuntimeError(f"HMMER failed with error: {e}")
    
    print(f"HMMER process for {protein_sequences} finished. Results saved to {output_file}")
