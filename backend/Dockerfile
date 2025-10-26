# 1️⃣ Usamos una imagen base de Python
FROM python:3.11-slim

# 2️⃣ Evita archivos temporales innecesarios
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3️⃣ Creamos una carpeta dentro del contenedor
WORKDIR /app

# 4️⃣ Copiamos los requisitos e instalamos dependencias
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5️⃣ Copiamos todo el proyecto dentro del contenedor
COPY . /app/

# 6️⃣ Exponemos el puerto que usará Django
EXPOSE 8000

# 7️⃣ Comando para ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
