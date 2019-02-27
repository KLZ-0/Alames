#!/bin/bash

pip install --user -r ./requirements.txt

cp Alames.desktop ~/.local/share/applications/
sed -i -e "s?\\.\\/?`pwd`\\/?g" ~/.local/share/applications/Alames.desktop
