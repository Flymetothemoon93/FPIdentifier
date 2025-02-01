#!/bin/bash

# Check if input and output parameters are provided
if [ $# -lt 2 ]; then
    echo "Error: You must provide an input file and an output directory!"
    echo "Usage: ./run.sh your_input.fasta your_output_dir"
    exit 1
fi

# Read user input
INPUT_FILE="$1"
OUTPUT_DIR="$2"
USE_SINGULARITY=false

# Check if an optional third parameter (--use-singularity) is provided
if [ "$3" == "--use-singularity" ]; then
    USE_SINGULARITY=true
fi

# Validate that the input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found! Please check the path."
    exit 1
fi

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Run with Docker or Singularity
if [ "$USE_SINGULARITY" = true ]; then
    echo "Running with Singularity..."
    singularity run gmfpid.sif --input "$INPUT_FILE" --output "$OUTPUT_DIR"
else
    echo "Running with Docker..."
    docker run --rm \
        -v "$(pwd)/$INPUT_FILE:/app/input.fasta" \
        -v "$(pwd)/$OUTPUT_DIR:/app/output_data" \
        flymetothemoon93/gmfpid:latest \
        --input /app/input.fasta \
        --output /app/output_data
fi

echo "Process completed! Results are saved in '$OUTPUT_DIR'"

