FROM continuumio/miniconda3

COPY environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml && conda clean -a

ENV PATH=/opt/conda/envs/myenv/bin:$PATH

COPY src/main.py /app/main.py
WORKDIR /app

CMD ["python", "main.py"]

VOLUME ["/app/in", "/app/out"]