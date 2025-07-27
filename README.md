# Persona-Driven Document Intelligence

This project is a powerful, offline-first document analysis pipeline built to tackle information overload. It intelligently extracts, ranks, and summarizes the most relevant sections from a collection of PDF documents, tailored to a specific user persona and their unique "job-to-be-done."

The system operates entirely on a CPU, with no internet connection required during execution, and adheres to a strict sub-60-second processing time and a 1 GB model footprint. By "Connecting What Matters," this tool empowers knowledge workers to instantly find the insights they need, turning hours of manual document sifting into seconds of automated analysis.

---
## Key Features

* **Persona-Driven Analysis**: Delivers results that are semantically relevant to the user's specific role and task.
* **Offline & CPU-Only**: Runs anywhere without a GPU or internet connection, ensuring data privacy and accessibility.
* **Fast & Efficient**: Processes multiple large documents and delivers a complete analysis in under 60 seconds.
* **Lightweight AI Models**: Utilizes state-of-the-art, quantized models for semantic search and summarization, keeping the total footprint under 1 GB.
* **Containerized & Reproducible**: Packaged with Docker for a hassle-free, one-command setup and execution on any machine.

---
## Technology Stack

* **Language**: Python 3.10
* **Containerization**: Docker
* **PDF Parsing**: PyMuPDF
* **AI/ML**: PyTorch, Transformers, Sentence-Transformers, Scikit-learn
* **Core Libraries**: Loguru, NumPy

---
## Project Structure
├── documents/
│   └── README.md
├── src/
│   ├── utils.py
│   ├── extract_text.py
│   ├── segment_sections.py
│   ├── embed_and_rank.py
│   ├── summarize.py
│   └── generate_output.py
├── challenge_input.json
├── Dockerfile
├── download_models.py
├── main.py
├── requirements.txt
└── README.md


---
## How to Run

### Prerequisites
* Docker must be installed and running on your system.

### Steps

1.  **Add Documents**: Place your PDF files inside the `documents/` folder.

2.  **Configure Task**: Open and edit the `challenge_input.json` file to define the `documents`, `persona`, and `job_to_be_done`.

3.  **Build and Run**: Open your terminal in the project's root directory and execute the following commands.

    ```bash
    # Step 1: Build the Docker image (this will take a few minutes as it downloads the models)
    docker build -t doc-intel-challenge .

    # Step 2: Run the analysis
    # For Linux/macOS:
    docker run --rm -v "$(pwd)":/app doc-intel-challenge challenge_input.json documents

    # For Windows (Command Prompt):
    docker run --rm -v "%cd%":/app doc-intel-challenge challenge_input.json documents
    ```
The final analysis will be saved to a new file named `challenge1b_output.json`.

---
## System Architecture

The pipeline executes in a sequence of automated steps:

1.  **Text Extraction**: The system first parses each PDF using PyMuPDF to extract text blocks along with their metadata, such as font size and position.

2.  **Section Segmentation**: A fast, heuristic-based algorithm segments the raw text into logical sections by identifying titles based on font size changes. This avoids the overhead of a dedicated ML model for structuring the content.

3.  **Semantic Encoding**: The user's persona and task are combined into a single query. The `all-MiniLM-L6-v2` sentence-transformer model then converts this query and each extracted document section into high-dimensional vector embeddings.

4.  **Relevance Ranking**: Cosine similarity is calculated between the query vector and all section vectors. The sections are then ranked in descending order of their similarity score, placing the most relevant content at the top.

5.  **Summarization**: For the top 5 most relevant sections, a quantized `t5-small` model generates a concise, abstractive summary to distill the core insights for the user.

---
## Constraints and Limitations

This system is built to adhere to the following constraints:
* **CPU-Only Execution**: No GPU is required.
* **Model Footprint ≤ 1 GB**: The total size of the packaged AI models is approximately 350 MB.
* **Offline Execution**: After the one-time Docker build, the container runs without any internet access.
* **Performance**: Processes 15+ documents in ~20-30 seconds, well under the 60-second limit for 3-5 documents.

**Limitations**:
* The heuristic sectioning may perform poorly on PDFs with unconventional layouts or scanned, image-based documents.
* The semantic search may be less effective for highly niche domains with specialized jargon not
