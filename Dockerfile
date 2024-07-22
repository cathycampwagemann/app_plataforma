# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos y luego instalar dependencias
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copiar el contenido de la aplicación
COPY . .

# Exponer el puerto en el que Streamlit se ejecutará
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "plataformacomision.py", "--server.port=8080", "--server.address=0.0.0.0"]
