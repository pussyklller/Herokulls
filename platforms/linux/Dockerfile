ARG python_version="3.6"
ARG dname="amd64"
ARG pname="manylinux2014_x86_64"
FROM ${dname}/python:${python_version}-bullseye
SHELL ["/bin/bash", "-c"]
RUN \
  apt-get update && apt-get install -y wget gpg curl && \
  wget -qO- https://deb.nodesource.com/gpgkey/nodesource.gpg.key | gpg --dearmor -o /usr/share/keyrings/nodesource-archive-keyring.gpg && \
  echo "deb [signed-by=/usr/share/keyrings/nodesource-archive-keyring.gpg] https://deb.nodesource.com/node_18.x buster main" > /etc/apt/sources.list.d/nodesource.list && \
  curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor -o /usr/share/keyrings/yarn-archive-keyring.gpg && \
  echo "deb [signed-by=/usr/share/keyrings/yarn-archive-keyring.gpg] https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list && \
  apt-get update && \
  apt-get install -yqq nodejs yarn && \
  node --version && npm --version && yarn --version && \
  pip install -U pip && pip install pipenv && \
  npm install -g npm@^8 && \
  rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/herokulls
WORKDIR herokulls/
COPY herokulls/ .
WORKDIR ../src/
COPY src/* .
WORKDIR ..
COPY .npmignore .
COPY package.json .
COPY tsconfig.json .
COPY setup.py .
COPY LICENSE .
COPY README.md .
COPY requirements.txt .
ARG pname
ARG python_version
RUN python${python_version} setup.py sdist bdist_wheel --plat-name ${pname}
WORKDIR /usr/src/installer
COPY platforms/linux/linux_mount.sh /usr/src/installer
RUN chmod +x /usr/src/installer/linux_mount.sh
VOLUME ['/usr/src/installer', '/usr/src/herokulls']
