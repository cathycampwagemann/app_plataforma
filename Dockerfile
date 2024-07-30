# Usar una imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos y luego instalar dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido de la aplicación
COPY . .

# Exponer el puerto en el que Streamlit se ejecutará
EXPOSE 8080

ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "plataformacomision.py"]
