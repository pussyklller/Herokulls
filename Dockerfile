# Установка базового образа и аргументов
ARG python_version="3.12"
ARG pname="manylinux2014_aarch64"

FROM python:${python_version}-bullseye

# Установка Node.js, Yarn и необходимых инструментов
RUN apt-get update && \
    apt-get install -yqq curl gnupg && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | gpg --dearmor -o /usr/share/keyrings/nodesource-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/nodesource-archive-keyring.gpg] https://deb.nodesource.com/node_18.x bullseye main" > /etc/apt/sources.list.d/nodesource.list && \
    curl -fsSL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor -o /usr/share/keyrings/yarn-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/yarn-archive-keyring.gpg] https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
    apt-get update && \
    apt-get install -yqq nodejs yarn && \
    pip install --no-cache-dir -U pip pipenv && \
    npm install -g npm@^8 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /usr/src/herokulls

# Копирование всех необходимых файлов
COPY herokulls/ ./herokulls/
COPY src/ ./src/
COPY .npmignore package.json tsconfig.json setup.py LICENSE README.md requirements.txt ./

# Установка переменной окружения для платформы manylinux2014_aarch64
ENV PYTHON_HOST_PLATFORM=manylinux2014_aarch64

# Сборка Python-пакета для manylinux2014_aarch64
RUN python${python_version} setup.py sdist bdist_wheel --plat-name ${pname}

# Подготовка скрипта для установки
WORKDIR /usr/src/installer
COPY platforms/linux/linux_mount.sh /usr/src/installer
RUN chmod +x /usr/src/installer/linux_mount.sh

# Объявление томов
VOLUME ["/usr/src/installer", "/usr/src/herokulls"]
