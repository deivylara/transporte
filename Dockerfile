# Usa una imagen base de Python
FROM python:3.9-slim

# Crear un usuario no root
RUN useradd -m dev

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app/

# Establecer permisos para el directorio de trabajo
RUN chown -R dev:dev /app

# Instalar las dependencias como el usuario no root
USER myuser
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el archivo .env al contenedor (asegúrate de que tiene los permisos adecuados)
COPY .env /app/.env

# Exponer el puerto en el que correrá Django
EXPOSE 80

# Ejecutar el servidor Django como el usuario no root
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]