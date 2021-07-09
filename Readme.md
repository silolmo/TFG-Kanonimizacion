Para instalar la aplicación se requiere contar con:
	Base de datos MySQL o MariaDB
	Python

Se deben instalar los siguientes paquetes:
	Qt5: sudo apt install qt5-default
	PyQt5: pip install PyQt5
	PyMySQL: pip install PyMySQL

Es necesario tener una base de datos en el servidor MySQL o MariaDB. Se recomienda también crear un usuario específico para la aplicación que   ́unicamente tenga acceso a esta base de datos. Para ello accedemos al servidor con el usuario ’root’ y realizamos los siguientes pasos:
	1.  Creamos un usuario:CREATE USER ’user’@’localhost’ IDENTIFIED BY ’password’;
	2.  Creamos la base de datos:CREATE DATABASE ’database’;
	3.  Otorgamos al usuario todos los privilegios hacia esa base de datos:GRANT ALL PRIVILE-GES ON ’database’.* TO ’user’@’localhost’;

Por  ́ultimo modificamos el fichero DBconnection.txt con los datos correspondientes para conectarsea la base de datos que acabamos de crear. Este fichero contiene el siguiente formato:
	host=’localhost’
	user=’annon’
	passwd=’password’
	database=’TFG’

Para iniciar la aplicación sólamente habrá que ejecutar el archivo start.sh
