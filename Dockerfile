FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    linux-tools-common \
    linux-tools-generic \
    dmidecode \
    sysstat \
    net-tools \
    iproute2 \
    pciutils \
    intel-gpu-tools \
    coreutils \
    procps \
    upower \
    util-linux \
    python3-pip \
    python3-dev \
    && apt-get clean

RUN ubuntu-drivers autoinstall
COPY . /TechDisrupt
WORKDIR /TechDisrupt
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]