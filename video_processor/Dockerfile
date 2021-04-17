FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .

RUN conda env create -f environment.yml \
    && conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "vp", "/bin/bash", "-c"]

COPY . .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "vp", "python", "main.py"]