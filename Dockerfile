# Usa una imagen base oficial de Python
FROM python:3.10

# Crea el usuario `dev`
RUN useradd -m dev

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación
COPY . /app

# Cambia el propietario de los archivos al usuario `dev`
RUN chown -R dev:dev /app

# Cambia al usuario `dev`
USER dev

# Expone el puerto en el que correrá la aplicación
EXPOSE 80

# Comando para correr la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
