FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "vp", "/bin/bash", "-c"]

COPY . .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "vp", "python", "main.py"]