# Persona-Driven Document Intelligence

This system extracts and prioritizes the most relevant sections from a collection of PDF documents based on a specific persona and their job-to-be-done.

## Prerequisites
- Docker must be installed and running.

## How to Run

1.  **Add Documents**: Place your test PDF files inside the `documents/` folder.

2.  **Configure Task**: Open the `challenge_input.json` file and edit the following:
    -   `documents`: List the filenames of the PDFs you added.
    -   `persona`: Define the user's role.
    -   `job_to_be_done`: Describe the user's task.

3.  **Build and Run**: Open your terminal in this directory and run the following commands.

    ```bash
    # Step 1: Build the Docker image (this will take a few minutes)
    docker build -t doc-intel-challenge .

    # Step 2: Run the analysis
    docker run --rm -v "$(pwd)":/app doc-intel-challenge challenge_input.json documents
    ```

The output will be saved to a new file named `challenge1b_output.json` in this directory.