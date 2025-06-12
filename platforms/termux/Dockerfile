FROM debian:bullseye

ARG python_version="3.6"
ARG pname="linux_aarch64"

RUN apt-get update && apt-get install -y \
    wget \
    tar \
    proot \
    qemu-user-static \
    python3 \
    python3-pip \
    clang \
    libffi-dev \
    libssl-dev \
    zlib1g-dev \
    build-essential \
    && apt-get clean

RUN wget https://github.com/termux/termux-packages/releases/download/bootstrap/termux-rootfs-21.08.tar.gz -O /termux-rootfs.tar.gz \
    && mkdir /termux \
    && tar -xzf /termux-rootfs.tar.gz -C /termux \
    && rm /termux-rootfs.tar.gz \
    && mkdir /termux/usr/bin/

COPY /usr/bin/qemu-aarch64-static /termux/usr/bin/

WORKDIR /mnt

COPY herokulls/ /mnt/hherokulls/
COPY src/ /mnt/src/
COPY package.json tsconfig.json setup.py LICENSE README.md requirements.txt .npmignore /mnt/

RUN chroot /termux /usr/bin/qemu-aarch64-static /bin/bash -c "\
    apt update && \
    apt install -y nodejs yarn && \
    pip install -U pip && \
    pip install pipenv && \
    npm install -g npm@^8 && \
    rm -rf /var/lib/apt/lists/*"

RUN chroot /termux /usr/bin/qemu-aarch64-static /bin/bash -c "\
    cd /mnt && \
    python${python_version} setup.py sdist bdist_wheel --plat-name ${pname}"

COPY platforms/linux/linux_mount.sh /mnt/installer/
RUN chmod +x /mnt/installer/linux_mount.sh

VOLUME ['/mnt/installer', '/mnt/herokulls']
