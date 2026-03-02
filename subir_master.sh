#!/bin/bash

echo "Subiendo a master..."

git add .

git commit -m "Actualización de archivos"

git push -u origin master

echo "¡Subida a master completada!"