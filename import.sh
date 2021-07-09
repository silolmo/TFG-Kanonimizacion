#!/bin/bash
ruta_datos=$1
ruta_atributos=$2
delimitador=$3

#Leo la primera linea del fichero
read -r linea < $ruta_datos
read -r atributos < $ruta_atributos

#Separo por el delimitador la primera línea de los datos (nombres de los atributos)
name=${linea%%$delimitador*} 
resto=${linea#*$delimitador} 

#Guardo en un array los nombres de las columnas
lista_columnas=("$name") 

while [[ $resto == *$delimitador* ]]
do
	name=${resto%%$delimitador*}
	resto=${resto#*$delimitador} 
	lista_columnas=(${lista_columnas[@]} $name)
done
lista_columnas=(${lista_columnas[@]} $resto)

#Separo por el delimitador los tipos de los atributos
name=${atributos%%$delimitador*} 
resto=${atributos#*$delimitador} 

#Guardo en un array los nombres de las columnas
lista_atr=("$name") 
while [[ $resto == *$delimitador* ]]
do
	name=${resto%%$delimitador*}
	resto=${resto#*$delimitador} 
	lista_atr=(${lista_atr[@]} $name)
done
lista_atr=(${lista_atr[@]} $resto)

#Quito las carpetas de la ruta
tabla=${ruta_datos##*/} 

#Quito el .txt
tabla=${tabla%.*} 

#Compongo la secuencia SQL
columnas="${lista_columnas[0]} ${lista_atr[0]}"
i=1
while [[ $i -lt ${#lista_columnas[@]} ]]
do
	columnas="$columnas, ${lista_columnas[$i]} ${lista_atr[$i]}"
	i=$i+1
done

database=$(cut -d "=" -f 2 DBconnection.txt | tail -1)

#Crea la tabla
mysql -e "create table data($columnas) default character set = utf8" $database

#Importa los datos a la tabla
cp $ruta_datos data.txt
mysqlimport --local --fields-terminated-by="$delimitador" --lines-terminated-by='\n' --ignore-lines=1 $database data.txt
rm data.txt
