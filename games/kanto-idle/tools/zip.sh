#!/bin/sh
# Empaqueta la carpeta publicable para arrastrarla a https://app.netlify.com/drop
cd "$(dirname "$0")/../public" && rm -f ../kanto-idle-netlify.zip && zip -qr ../kanto-idle-netlify.zip . -x '.*' && echo "creado kanto-idle-netlify.zip"
