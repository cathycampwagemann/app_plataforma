import streamlit as st
import os
import sqlite3
from google.cloud import storage
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO
from datetime import datetime, timedelta,timezone
import pytz
import fitz
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, pkcs12
from cryptography.hazmat.backends import default_backend
import tempfile
import streamlit.components.v1 as components
import pandas as pd
import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import boto3
from botocore.client import Config
import mysql.connector
from mysql.connector import errorcode
import uuid

drive_image_url = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBw8NDg4NDQ0PDw8PERMQDxENDhEQEA8QFxEXGBgRFx8kHSggJBoxHhUTIT0tJTUrLjA6IyI/RD8sNygtLi0BCgoKDg0OGxAQGysgHh0vLzcvMSstLS4wLSstNy83LTYuKzUrLTUvMy4uLS03LS0tKy0tLS83LS0tNy0xLSstLf/AABEIAMgAyAMBIgACEQEDEQH/xAAbAAEAAgMBAQAAAAAAAAAAAAAABQYDBAcCAf/EADUQAAICAgEDAgQDBwQDAQAAAAABAgMEERIFEyEGMRQiQVEyYYEjNVJxdJGzFTNCYhbB0Qf/xAAYAQEBAQEBAAAAAAAAAAAAAAAAAgEDBP/EACQRAQACAQQCAgIDAAAAAAAAAAABEQITITFBAxJR8FJhocHx/9oADAMBAAIRAxEAPwDuIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMLyIdxU8l3HB2KP14JpOX92hHIg5yrVkXZFJygpJzin7Nr3SAyg0LetYkEpTy8eKk5KLlfWlJxepJefdPWz1/q2NzhX8VRzmouEO9DlNS/C0t7aZtSy4bp9NHO6rjYzisjJppcvwq62FfL+W2bDyK1DuuyCr48+bklDjrfLftr8zKkuGYGtbnUwrV87q41NJqyVkVW1L2ae9efB9py67Id2FsJ16b5wnGUNL3e/bXhipLhsAxY98LYqyucZwktxlCSlGS+6a8GUNAAAAAAAAADxOajrk0ttRW2ltt6S/mB6BrW59Ndkap3VQtnrhCdkYznt68Le39TxldUx6ZqF2RTXNpNRstjGTTet6b9hTLhug1czPpoSlfdXUpPUXZOMFJ/Zb92e6cqucO7CyEq2tqcZJw0vrv217ipLhnBq5edTRFTuuqqjJ6jK2yMIt63pNv7Jn342ntd/vV9nXLuc49vX35b1oUW2QaVPU8ecJ2wyKpV1/jmrIuMNL/k9+P1M+NkQugrKpxshL8MoSUovz9GvAotFWfvWv+is/wA9ZAevcizp19PU6IOUrKbMGxR87nJOdD/Saf8Acn5/vWv+is/z1nrq3qLCxLoY+VfGFs1GUIShOW05NJ+E17pnXGayja3PKImJ3pQ/UnTa8F9Exrb8elV0ZKssyqFkVOxqtybi35bk5Mj/AFJjqzM25U/C9np0b8iuiKlVXJvjdV/BHaS8eya9zo69S9PtyHh9+E8iEpwcHXNtSgm5rfHXji/7HzB9T9NyYXTpyapxprdl3yyTjVFfi01tpHaPLlG9T/rlPjxnv7CqZeTj42X1R59eNLLnOMsR9Q8UWYnGKUYS4vWvn2l7swZnUbL+lYeFVg9r4y5qOPjNpywq5Kdk48ta5fnrw/zL5LqOHasXc67FlecbceSsajy8ePHhP30Zl1LH+K+E7kPiVX3e3p8lXvW9+36EanG3H9K9P39lzS6+x9Gv6dZW67sTMx64V5GpNUWXxlTz09NabX6H3HvnT0e/EqTebnZtuPZj0wjX2J6XdhCO9KPbhvf/AGOi/wCrYknlftYN4i3lLi91JRck348+E34NPL9VdNx51d3JrhK2uN1blCXzVz3xnvXjen7lakzt692zTj8uqRP/AOdXyp+K6bZTZR2Z9/GqucXOONbJ/LtN7SkpefzRdSF6p6kwcPtSyMiEO9Fyqkoynzh4e04p+PKPH/l3T+/DG+KXem4KMO3ZuTmk4/8AH6qSOOcZZz7U64zjjFWngAc3QAAAAACueosC/NtjVVqEKI9xTsU0nkParlDXu4acvtuUfsWMGxNTbJi9lJ6o77pOfC+FksfH1THGnZVdkVX2t1Snx+WPLj824+Hv2JXHvjjPKryKbZTttsnyhj2XLIhL8EdpNbUeMNPX4ft5LACpz6TGCrdMqnhSrnk1T08auquUITv+HcZzbpfHbS1Kvz7Pj7+EeZRysimVHarisi5uU/h7MeM8eMYuyVkW21KUtw0/LT2WsD37PTpVKHbj/CV312NYt84c6abbVKl48+21pN+OSg/zX5iVLdry1j2fDLJja6+1JWSaolB5Kr1y/E4+Nb8b17FrA9z0VjP4ZNk7lVkdmNDrtnCmyFk5u6uVcoRa5S4cZy3p+/jflEr0C2c6N2x0+c0pOt1O2PN6tcX5TfuSQMnLamxjvaFn+9a/6Kz/AD1kP1PpduR1uM4XX0QjgR3ZTFam1ky/ZNtNez3r3Jiz961/0Vn+es9da9RU4U66pQuuvsTlCjFqdtrgnpz19I/myomb2+ETETG/yp/p9Shn59c7M6DszMycKVQ/hLYuL1OUuP5P6/REP0DpeRXi5ayYZErJ9Isjh/s2owhJS547Wv8Ac5cdb+h0FercT4aWVPu1qNnZdVlM439/S1So625eV7f+mMD1bjWu2NkL8Wymt3zrzKZVWdlb3Yl52vH0O2plXH2HP0x+VN6X0jJw8zpFfCcsL5smL4ybxrJYrVtUvtHk9r+bMFdHUFkLrjwnp5Xdk+UviPg5ap7Pb478R1IuEfW2P8NPLePmquDjveLLfCUXKNq+nDS99/Vfc2cv1XjUYMeoXRuqpnJRjGypxtbcml8r/k3/ACGpn+P6Z6YfKk9Z6Pk9zrOdi12OzuWUzr4y1k4tmPFPivq4v5lr7M3MXK+DyKJX4mTdCfR8WnhVjTt5WJy3U1rSf8zotNkZxjOLUoySlFr2aa8MjOl+o8TMutox7edlW3JcJRTipcXKLa1Jck1tbJ1ZmN44VpRE88ueS6ffiQ6Qr3mUOvHyecsKp3WVc7lKFT+V/RpfoT0uoRs6viK6vKlVi0wjROWNY1ZlXJJ2zajpajpefZt/YtPW+t04MISuc5Sslwqqpg7LbZfwxivLI+PrDG7N91lWVS8d1q2q/HlC2PcnwhLXs02/ozffLKLr5/k9McZq1jBHde6zT0/Hlk5Dari4r5VuUnJ6SS+/k1+q+o6MWijJkrbYZM4QpVFbsnNzg5R0vf2izzxjM9O05RHaZBAWersRY1WUnZNXyddVVdUpZFlkW1KtQ9+SaZsdE9QU5srK4Rtpuq13KMmt1XQi/aWvt+aNnDLmiM8Z7TAAJUAAAAAAAAAAAAAISf71r/orP89ZG9VryMPqT6hXi2ZdN2PGiyNHF3UyhNyTSbW4vf0LR2Y8+5xjzUeKlpcuLabjv7eEZCoypE42pvVI5uXDEz1gShZh5Ltji2Ww7l1Dhxcv4VZ5bSf2PE45Wfl15r6dZVVh0XxhVlOuFmXZbBLtNbaUNL3f3LqCtT9J077c3wOm5ksDquPXi5FONOnWJj5MoyshdKMuddb3/t71rf8A9N3rnRs3MswKK4VQpxcfnN5UXOqy+UO322k09qLk/wBS9grWm7NGKpXfRlGVj4KxcmH7XFlOiuTfy3Vxf7Oa/wCuml9/BUfR2J1HEzO5LAmo5M0syy2uC7EnOyUo0KM/9rcovejqAMjyzF7ck+LjfhWfU+LfDKweoY9Dyfhe7C2mEoqxwtjFc4b8bXH2+uyP9RX5nUenZcIdNvq+ah0xtlDvXON8JT+VPxpL6suwMjyVW3DZ8d3vyovXMfO6rbhqvF+Grp55FizoqcJWpuEINRltvTlL7eSNu9PZ9nT8Pp01ZGeL1BRjfS9axuFnG+L3vS5qP38HTAVHmmIqOkz4YnlzzA6VlYlXTMqGDKVmEr6snHU07LHZ+LJrbfltrl+uiZ6LTkZXUZ9Stxp4tUcb4Wqu5xV1u7FNzkk3pLWki1AnLyzk2PHEPoAObqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/9k="

# HTML y CSS para centrar el logo en la interfaz
logo_html = f"""
<div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
    <img src="{drive_image_url}" style="max-width: 100%; max-height: 100%;">
</div>
"""
# Insertar el HTML en la aplicación Streamlit
components.html(logo_html, height=150)

load_dotenv()

# Configurar las credenciales HMAC desde las variables de entorno
access_key = os.getenv('HMAC_ACCESS_KEY')
secret_key = os.getenv('HMAC_SECRET_KEY')

if not access_key or not secret_key:
    raise Exception("HMAC credentials not set in environment variables.")

# Configurar el cliente de boto3
storage_client = boto3.client(
    's3',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    endpoint_url='https://storage.googleapis.com',
    config=Config(signature_version='s3v4')
)

load_dotenv()

def connect_to_cloud_sql():
    try:
        conn = mysql.connector.connect(
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT'))
        )
        print("Conexión exitosa a la base de datos")
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu nombre de usuario o contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)
        return None

conn = connect_to_cloud_sql()
if conn:
    cursor = conn.cursor()

    try:

        # Creación de la tabla users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `users` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `username` VARCHAR(255) UNIQUE,
                `password` VARCHAR(255),
                `email` VARCHAR(255) UNIQUE,
                `role` VARCHAR(50)
            )
        ''')

        # Tablas comisión arbitral
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `user_permissions_com_arbitral` (
                `user_id_com_arbitral` INT,
                `bucket_name_com_arbitral` VARCHAR(255),
                FOREIGN KEY (`user_id_com_arbitral`) REFERENCES `users` (`id`)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `password_resets_com_arbitral` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id_com_arbitral` INT,
                `token_com_arbitral` VARCHAR(255),
                FOREIGN KEY (`user_id_com_arbitral`) REFERENCES `users` (`id`)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `main_files_com_arbitral` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name_com_arbitral` VARCHAR(255),
                `section_com_arbitral` VARCHAR(255),
                `stage_com_arbitral` VARCHAR(255),
                `gcs_path_com_arbitral` VARCHAR(255),
                `bucket_name_com_arbitral` VARCHAR(255),
                `file_url_com_arbitral` VARCHAR(255),
                `emisor_doc` VARCHAR(255),
                `uploaded_at_com_arbitral` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `proveido_com_arbitral` BOOLEAN DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `attached_files_com_arbitral` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `main_file_com_arbitral_id` INT,
                `name` VARCHAR(255),
                `gcs_path_com_arbitral` VARCHAR(255),
                `uploaded_at_com_arbitral` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`main_file_com_arbitral_id`) REFERENCES `main_files_com_arbitral` (`id`)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `causa_comision_arbitral` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `tribunal` VARCHAR(255),
                `demandante` VARCHAR(255),
                `demandado` VARCHAR(255),
                `fecha_inicio` DATE,
                `bucket_name_com_arbitral` VARCHAR(255)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `notifications_com_arbitral` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT,
                `message` TEXT,
                `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `notificaciones_com_arbitral` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `bucket_name_com_arbitral` VARCHAR(255),
                `archivo` VARCHAR(255),
                `fecha` DATE,
                `emails` TEXT
            )
        ''')

        # Tablas comisión conciliadora
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `user_permissions_com_conciliadora` (
                `user_id_com_conciliadora` INT,
                `bucket_name_com_conciliadora` VARCHAR(255),
                FOREIGN KEY (`user_id_com_conciliadora`) REFERENCES `users` (`id`)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `password_resets_com_conciliadora` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id_com_conciliadora` INT,
                `token_com_conciliadora` VARCHAR(255),
                FOREIGN KEY (`user_id_com_conciliadora`) REFERENCES `users` (`id`)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `main_files_com_conciliadora` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name_com_conciliadora` VARCHAR(255),
                `gcs_path_com_conciliadora` VARCHAR(255),
                `bucket_name_com_conciliadora` VARCHAR(255),
                `file_url_com_conciliadora` VARCHAR(255),
                `emisor_doc2` VARCHAR(255),
                `uploaded_at_com_conciliadora` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `proveido_com_conciliadora` BOOLEAN DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `attached_files_com_conciliadora` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `main_file_com_conciliadora_id` INT,
                `name` VARCHAR(255),
                `gcs_path_com_conciliadora` VARCHAR(255),
                `uploaded_at_com_conciliadora` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`main_file_com_conciliadora_id`) REFERENCES `main_files_com_conciliadora` (`id`)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `causa_comision_conciliadora` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `comision` VARCHAR(255),
                `requirente` VARCHAR(255),
                `requerido` VARCHAR(255),
                `fecha_inicio` DATE,
                `bucket_name_com_conciliadora` VARCHAR(255)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `notifications_com_conciliadora` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT,
                `message` TEXT,
                `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `notificaciones_com_conciliadora` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `bucket_name_com_conciliadora` VARCHAR(255),
                `archivo` VARCHAR(255),
                `fecha` DATE,
                `emails` TEXT
            )
        ''')

        conn.commit()
        print("Todas las tablas se han creado correctamente")
    except mysql.connector.Error as err:
        print(f"Error al crear las tablas: {err}")
    finally:
        cursor.close()
        conn.close()

# Función para crear bucket Comisión arbitral
def create_bucket_com_arbitral(bucket_name_com_arbitral):
    
    client = storage.Client()
    
    try:
        bucket = client.create_bucket(bucket_name_com_arbitral)
        st.success(f"Bucket '{bucket_name_com_arbitral}' creado exitosamente.")
        return bucket_name_com_arbitral
    except Exception as e:
        if "409" in str(e):
            st.warning(f"El bucket '{bucket_name_com_arbitral}' ya existe.")
            return bucket_name_com_arbitral
        else:
            st.error(f"Error al crear el bucket com arbitral: {e}")
            return None

# Función para crear bucket Comisión conciciliadora
def create_bucket_com_conciliadora(bucket_name_com_conciliadora):
    client = storage.Client()
    
    try:
        bucket = client.create_bucket(bucket_name_com_conciliadora)
        st.success(f"Bucket '{bucket_name_com_conciliadora}' creado exitosamente.")
        return bucket_name_com_conciliadora
    except Exception as e:
        if "409" in str(e):
            st.warning(f"El bucket '{bucket_name_com_conciliadora}' ya existe.")
            return bucket_name_com_conciliadora
        else:
            st.error(f"Error al crear el bucket com conciliadora: {e}")
            return None

# Función para autenticar comisión arbitral y conciliadora

def authenticate_com_conciliadora(username, password):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        # Usar %s como marcador de posición para los parámetros en MySQL
        c.execute('SELECT id, role FROM users WHERE username = %s AND password = %s', (username, password))
        user = c.fetchone()
        if user:
            st.session_state['user_id_com_conciliadora'] = user[0]
            st.session_state['username'] = username
            st.session_state['user_role'] = user[1]
            return True
        return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        c.close()
        conn.close()

def authenticate_com_arbitral(username, password):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        # Usar %s como marcador de posición para los parámetros en MySQL
        c.execute('SELECT id, role FROM users WHERE username = %s AND password = %s', (username, password))
        user = c.fetchone()
        if user:
            st.session_state['user_id_com_arbitral'] = user[0]
            st.session_state['username'] = username
            st.session_state['user_role'] = user[1]
            return True
        return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        c.close()
        conn.close()
# Interfaz principal comisión arbitral

def main_interface_com_arbitral():

    st.sidebar.write(f"Bienvenido/a la plataforma de la Comisión Arbitral")
    user_id_com_arbitral = st.session_state['user_id_com_arbitral']
    buckets_ca = get_user_buckets_com_arbitral(st.session_state['user_id_com_arbitral'])
    st.title("Selecciona una causa")
    st.sidebar.selectbox("SELECCIONA UNA CAUSA", buckets_ca, key="buckets_menu_ca")
    st.sidebar.button("Cerrar sesión", on_click=lambda: st.session_state.clear())

    if buckets_ca:
    
        selected_bucket = st.selectbox("_", buckets_ca,  key="select_bucket")
        if selected_bucket:
            st.session_state['selected_bucket_ca'] = selected_bucket
            info_causa = get_causa_info_com_arbitral(selected_bucket)
            if info_causa:
                tribunal, demandante, demandado, fecha_inicio = info_causa
                st.markdown("""
                    <style>
                        table.causa-table {
                            width: 100%;
                            border-collapse: collapse;
                        }
                        table.causa-table th, table.causa-table td {
                            border: 1px solid black;
                            padding: 10px;
                            text-align: center;
                        }
                        table.causa-table th:nth-child(1), table.causa-table td:nth-child(1) { width: 25%; }
                        table.causa-table th:nth-child(2), table.causa-table td:nth-child(2) { width: 25%; }
                        table.causa-table th:nth-child(3), table.causa-table td:nth-child(3) { width: 25%; }
                        table.causa-table th:nth-child(4), table.causa-table td:nth-child(4) { width: 25%; }
                        .causa-title {
                            font-weight: bold;
                            text-align: center;
                            margin-bottom: 10px;
                        }
                    </style>
                """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="causa-title">INFORMACIÓN DE LA CAUSA</div>
                    <table class="causa-table">
                        <thead>
                            <tr>
                                <th>Tribunal</th>
                                <th>Demandante</th>
                                <th>Demandado</th>
                                <th>Fecha de inicio</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{}</td>
                                <td>{}</td>
                                <td>{}</td>
                                <td>{}</td>
                            </tr>
                        </tbody>
                    </table>
                """.format(tribunal, demandante, demandado, fecha_inicio), unsafe_allow_html=True)

        if st.button("Visualizar archivos de la causa", key="archivos_causa_ca"):
            reset_modes_a('visualizar_mode_com_a')
            st.session_state['visualizar_mode_com_a']=True

        if st.button("Subir nuevo archivo", key="subir_archivo_com_arbitral"):
            reset_modes_a('upload_mode_com_a')
            st.session_state['upload_mode_com_a'] = True

        if st.button("Resoluciones notificadas", key="ver_resoluciones_ca"):
            reset_modes_a('ver_notificaciones_ca')
            st.session_state['ver_notificaciones_ca']=True

    if st.session_state.get('user_role') == 'admin':
        if st.button("Crear nuevas causas y usuarios", key="com_arb_new"):
            reset_modes_a('crear_nueva_causa_usuario')
            st.session_state['crear_nueva_causa_usuario']=True

        if st.button("Asignar nuevos permisos", key="com_arb_new_permisos"):
            reset_modes_a('asignar_nuevos_permisos_usuarios')
            st.session_state['asignar_nuevos_permisos_usuarios']=True

        if 'upload_mode_com_a' in st.session_state:
            upload_file_interface_com_arbitral()

        if 'visualizar_mode_com_a' in st.session_state:
            list_files_com_arbitral(selected_bucket)

        if 'ver_notificaciones_ca' in st.session_state:
            notificaciones_interface_com_arbitral()

        if 'crear_nueva_causa_usuario' in st.session_state:
            crear_nueva_causa()

        if 'asignar_nuevos_permisos_usuarios' in st.session_state:
            asignar_nuevos_permisos()

def reset_modes_a(except_key=None):
    keys_to_reset = ['upload_mode_com_a', 'visualizar_mode_com_a', 'ver_notificaciones_ca','crear_nueva_causa_usuario','asignar_nuevos_permisos_usuarios']
    for key in keys_to_reset:
        if key != except_key and key in st.session_state:
            del st.session_state[key]

# Interfaz principal comisión conciliadora

def main_interface_com_conciliadora():
    st.sidebar.write(f"Bienvenido/a la plataforma de la Comisión Conciliadora")
    user_id_com_conciliadora = st.session_state['user_id_com_conciliadora']
    buckets_cc = get_user_buckets_com_conciliadora(st.session_state['user_id_com_conciliadora'])
    st.title("Selecciona una causa")
    st.sidebar.selectbox("Selecciona una causa", buckets_cc, key="buckets_menu_cc")
    st.sidebar.button("Cerrar sesión", on_click=lambda: st.session_state.clear())

    if buckets_cc:

        selected_bucket2 = st.selectbox("_", buckets_cc,  key="select_bucket_com_con")
        if selected_bucket2:
            st.session_state['selected_bucket_cc'] = selected_bucket2
            info_causa2 = get_causa_info_com_conciliadora(selected_bucket2)
            if info_causa2:
                comision, requirente, requerido, fecha_inicio = info_causa2
                st.markdown("""
                    <style>
                        table.causa-table {
                            width: 100%;
                            border-collapse: collapse;
                        }
                        table.causa-table th, table.causa-table td {
                            border: 1px solid black;
                            padding: 10px;
                            text-align: center;
                        }
                        table.causa-table th:nth-child(1), table.causa-table td:nth-child(1) { width: 25%; }
                        table.causa-table th:nth-child(2), table.causa-table td:nth-child(2) { width: 25%; }
                        table.causa-table th:nth-child(3), table.causa-table td:nth-child(3) { width: 25%; }
                        table.causa-table th:nth-child(4), table.causa-table td:nth-child(4) { width: 25%; }
                        .causa-title {
                            font-weight: bold;
                            text-align: center;
                            margin-bottom: 10px;
                        }
                    </style>
                """, unsafe_allow_html=True)
                st.markdown("""
                    <div class="causa-title">INFORMACIÓN DE LA CAUSA</div>
                    <table class="causa-table">
                        <thead>
                            <tr>
                                <th>Comisión</th>
                                <th>Requirente</th>
                                <th>Requerido</th>
                                <th>Fecha de inicio</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{}</td>
                                <td>{}</td>
                                <td>{}</td>
                                <td>{}</td>
                            </tr>
                        </tbody>
                    </table>
                """.format(comision, requirente, requerido, fecha_inicio), unsafe_allow_html=True)

        if st.button("Visualizar archivos de la causa", key="archivos_causa_cc"):
            reset_modes('visualizar_mode_com_c')
            st.session_state['visualizar_mode_com_c']=True

        if st.button("Subir nuevo archivo", key="upload_file_conciliadora"):
            reset_modes('upload_mode_com_c')
            st.session_state['upload_mode_com_c'] = True

        if st.button("Resoluciones notificadas", key="ver_resoluciones_cc"):
            reset_modes('ver_notificaciones')
            st.session_state['ver_notificaciones']=True

        if 'upload_mode_com_c' in st.session_state:
            upload_file_interface_com_conciliadora()

        if 'visualizar_mode_com_c' in st.session_state:
            list_files_com_conciliadora(selected_bucket2)

        if 'ver_notificaciones' in st.session_state:
            notificaciones_interface_com_conciliadora()

        if st.session_state.get('user_role') == 'admin':
            if st.button("Crear nuevas causas", key="com_conc_new"):
                reset_modes('crear_causas')
                st.session_state['crear_causas']=True

            if st.button("Asignar nuevos permisos", key="com_conc_new_permisos"):
                reset_modes('asignar_permisos')
                st.session_state['asignar_permisos']=True

        if 'crear_causas' in st.session_state:
            crear_nueva_causa()

        if 'asignar_permisos' in st.session_state:
            asignar_nuevos_permisos()

def reset_modes(except_key=None):
    keys_to_reset = ['upload_mode_com_c', 'visualizar_mode_com_c', 'ver_notificaciones','asignar_permisos', 'crear_causas']
    for key in keys_to_reset:
        if key != except_key and key in st.session_state:
            del st.session_state[key]

def crear_nueva_causa():
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    st.header("Crear Nueva Causa")

    comision = st.radio("Selecciona el tipo de comisión", ("Comisión Arbitral", "Comisión Conciliadora"))

    nombre_causa = st.text_input("Nombre de la causa (bucket)")
    demandante = st.text_input("Demandante / Requirente")
    demandado = st.text_input("Demandado / Requerido")
    fecha_inicio = st.date_input("Fecha de inicio")
    
    if st.button("Crear causa"):
        if nombre_causa and demandante and demandado and fecha_inicio:
            try:
                if comision == "Comisión Arbitral":
                    bucket_name = create_bucket_com_arbitral(nombre_causa)
                    if bucket_name:
                        c.execute('INSERT INTO causa_comision_arbitral (tribunal, demandante, demandado, fecha_inicio, bucket_name_com_arbitral) VALUES (%s, %s, %s, %s, %s)',
                                  (comision, demandante, demandado, fecha_inicio.strftime('%Y-%m-%d'), nombre_causa))
                else:
                    bucket_name = create_bucket_com_conciliadora(nombre_causa)
                    if bucket_name:
                        c.execute('INSERT INTO causa_comision_conciliadora (comision, requirente, requerido, fecha_inicio, bucket_name_com_conciliadora) VALUES (%s, %s, %s, %s, %s)',
                                  (comision, demandante, demandado, fecha_inicio.strftime('%Y-%m-%d'), nombre_causa))

                conn.commit()
                st.success(f"Causa '{nombre_causa}' creada exitosamente.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al crear la causa: {e}")
        else:
            st.error("Por favor, completa todos los campos.")

    st.write("---")

    st.header("Registrar Nuevos Usuarios")

    comision = st.radio("Selecciona el tipo de comisión", ("Comisión Arbitral", "Comisión Conciliadora"),key="com2")

    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    email = st.text_input("Correo electrónico")
    role = st.selectbox("Rol", ["admin", "arbitro", "actuario", "abogado", "perito"])

    # Seleccionar causa para asignar permisos
    causas = []
    try:
        if comision == "Comisión Arbitral":
            causas = get_all_buckets_com_arbitral()
        else:
            causas = get_all_buckets_com_conciliadora()
    except Exception as e:
        st.error(f"Error al obtener las causas: {e}")

    causa_seleccionada = st.selectbox("Selecciona la causa para asignar permisos", causas, key="causa_seleccionada")

    if st.button("Registrar usuario"):
        if username and password and email and role and causa_seleccionada:
            try:
                c.execute('INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)', (username, password, email, role))
                user_id = c.lastrowid

                if comision == "Comisión Arbitral":
                    c.execute('INSERT INTO user_permissions_com_arbitral (user_id_com_arbitral, bucket_name_com_arbitral) VALUES (%s, %s)', (user_id, causa_seleccionada))
                else:
                    c.execute('INSERT INTO user_permissions_com_conciliadora (user_id_com_conciliadora, bucket_name_com_conciliadora) VALUES (%s, %s)', (user_id, causa_seleccionada))

                conn.commit()
                st.success(f"Usuario '{username}' registrado y asignado a la causa '{causa_seleccionada}'.")
            except Exception as e:
                st.error(f"Error al registrar usuario: {e}")
        else:
            st.error("Por favor, completa todos los campos.")
    
    conn.close()

def create_bucket_com_arbitral(bucket_name_com_arbitral):
    client = storage.Client()
    try:
        bucket = client.create_bucket(bucket_name_com_arbitral)
        return bucket
    except Exception as e:
        st.error(f"Error al crear el bucket com arbitral: {e}")
        return client.bucket(bucket_name_com_arbitral)

def create_bucket_com_conciliadora(bucket_name_com_conciliadora):
    client = storage.Client()
    try:
        bucket = client.create_bucket(bucket_name_com_conciliadora)
        return bucket
    except Exception as e:
        st.error(f"Error al crear el bucket com conciliadora: {e}")
        return client.bucket(bucket_name_com_conciliadora)

def asignar_nuevos_permisos():
    st.header("Usuarios y permisos")

    # List all users
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    c.execute("SELECT id, username, email, role FROM users")
    users = c.fetchall()

    if users:
        st.write("### Usuarios:")
        for user in users:
            user_id, username, email, role = user
            st.write(f"**Usuario:** {username}, **Email:** {email}, **Rol:** {role}")
            
            new_role = st.selectbox(f"Cambiar el rol de {username}", ["actuario", "perito", "abogado", "arbitro", "admin"], index=["actuario", "perito", "abogado", "arbitro", "admin"].index(role), key=f"role_{user_id}")
            if st.button(f"Actualizar rol para {username}", key=f"update_role_{user_id}"):
                update_user_role(user_id, new_role)
            
            st.write("Asignar Causas:")
            available_buckets_ca = get_all_buckets_com_arbitral()
            assigned_buckets_ca = get_user_buckets_com_arbitral(user_id)
            buckets_to_assign_ca = st.multiselect(f"Asignar causa (Comisión Arbitral) a {username}", available_buckets_ca, default=assigned_buckets_ca, key=f"buckets_ca_{user_id}")
            if st.button(f"Actualizar causas (Comisión Arbitral) para {username}", key=f"update_buckets_ca_{user_id}"):
                update_user_buckets_com_arbitral(user_id, buckets_to_assign_ca)

            available_buckets_cc = get_all_buckets_com_conciliadora()
            assigned_buckets_cc = get_user_buckets_com_conciliadora(user_id)
            buckets_to_assign_cc = st.multiselect(f"Asignar causa (Comisión Conciliadora) a {username}", available_buckets_cc, default=assigned_buckets_cc, key=f"buckets_cc_{user_id}")
            if st.button(f"Actualizar causas (Comisión Conciliadora) para {username}", key=f"update_buckets_cc_{user_id}"):
                update_user_buckets_com_conciliadora(user_id, buckets_to_assign_cc)
    else:
        st.write("No se encontraron usuarios.")

    conn.close()

#Función para subir archivos comisión arbitral

def upload_file_interface_com_arbitral():
    """Interfaz para subir archivos cuando el modo de subida está activo."""

    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    st.title("Subir archivos")
    uploaded_files = st.file_uploader("Selecciona un archivo (incluyendo adjuntos)", accept_multiple_files=True, key="upload_file_uploader1")
    buckets_ca = get_user_buckets_com_arbitral(st.session_state['user_id_com_arbitral'])
    selected_bucket_ca = st.selectbox("Selecciona una causa", buckets_ca,key="select_bucket1")
    section = st.selectbox("Selecciona el cuaderno", ["Principal", "Incidente"], key="select_section")
    stage = st.selectbox("Selecciona la etapa", ["Discusión", "Probatorio", "Conciliación", "Citación a oír Sentencia", "Terminado"], key="select_stage")

    if st.session_state['user_role'] in ["admin", "arbitro", "actuario"]:
        emisor_options = ["Tribunal"]
    else:
        emisor_options = ["Demandante", "Demandado"]

    emisor_doc = st.selectbox("Selecciona el emisor del documento", emisor_options, key="select_emisor")

    selected_users = []
    if emisor_doc == "Tribunal":
        c.execute('SELECT email FROM users INNER JOIN user_permissions_com_arbitral ON users.id = user_permissions_com_arbitral.user_id_com_arbitral WHERE bucket_name_com_arbitral = %s', (selected_bucket_ca,))
        users = c.fetchall()
        user_emails = [user[0] for user in users]
        selected_users = st.multiselect("Selecciona los usuarios a notificar", user_emails, key="select_users")

    if st.button("Guardar archivo", key="save_file"):
        if uploaded_files and section and stage and selected_bucket_ca and emisor_doc:
            save_uploaded_file_com_arbitral(uploaded_files, section, stage, selected_bucket_ca, emisor_doc)
            st.success("Archivo subido con éxito.")
            if emisor_doc=="Tribunal":
                notify_abogados_com_arbitral(selected_users, selected_bucket_ca, uploaded_files[0].name)
            else:
                notify_comision_arbitral(selected_bucket_ca, uploaded_files[0].name)
            # Limpia el modo de subida si necesario
            if 'upload_mode_com_a' in st.session_state:
                st.session_state.pop('upload_mode_com_a', None)
        else:
            st.error("Por favor, completa todos los campos necesarios para subir el archivo.")


    conn.close()

#Función para subir archivos comisión conciliadora

def upload_file_interface_com_conciliadora():
    """Interfaz para subir archivos cuando el modo de subida está activo."""
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    st.title("Subir archivos")
    uploaded_files = st.file_uploader("Selecciona un archivo (incluyendo adjuntos)", accept_multiple_files=True, key="upload_file_uploader2")
    buckets_cc = get_user_buckets_com_conciliadora(st.session_state['user_id_com_conciliadora'])
    selected_bucket_cc = st.selectbox("Selecciona una causa", buckets_cc,key="select_bucket2")
    
    if st.session_state['user_role'] in ["admin", "arbitro", "actuario"]:
        emisor_options = ["Comisión"]
    else:
        emisor_options = ["Requirente", "Requerido", "perito"]

    emisor_doc2 = st.selectbox("Selecciona el emisor del documento", emisor_options, key="select_emisor2")

    selected_users = []
    if emisor_doc2 == "Comisión":
        c.execute('SELECT email FROM users INNER JOIN user_permissions_com_conciliadora ON users.id = user_permissions_com_conciliadora.user_id_com_conciliadora WHERE bucket_name_com_conciliadora = %s', (selected_bucket_cc,))
        users = c.fetchall()
        user_emails = [user[0] for user in users]
        selected_users = st.multiselect("Selecciona los usuarios a notificar", user_emails, key="select_users")

    if st.button("Guardar archivo", key="save_file"):
        if uploaded_files and selected_bucket_cc and emisor_doc2:
            save_uploaded_file_com_conciliadora(uploaded_files, selected_bucket_cc, emisor_doc2)
            st.success("Archivo subido con éxito.")
            if emisor_doc2 == "Comisión":
                notify_abogados_com_conciliadora(selected_users, selected_bucket_cc, uploaded_files[0].name)
            else:
                notify_comision_conciliadora(selected_bucket_cc, uploaded_files[0].name)
            # Limpia el modo de subida si necesario
            if 'upload_mode_com_c' in st.session_state:
                st.session_state.pop('upload_mode_com_c', None)
        else:
            st.error("Por favor, completa todos los campos necesarios para subir el archivo.")

    conn.close()

# Función para guardar el archivo en GCS y registrar en la base de datos de com arbitral
def save_uploaded_file_com_arbitral(uploaded_files, section, stage, bucket_name_com_arbitral, emisor_doc):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        # Guardar en el bucket de prueba
        main_file_com_arbitral=uploaded_files[0]
        main_file_com_arbitral_path=f"{section}/{main_file_com_arbitral.name}"
        storage_client.upload_fileobj(main_file_com_arbitral, bucket_name_com_arbitral, main_file_com_arbitral_path)
        main_gcs_path_com_arbitral = f"gs://{bucket_name_com_arbitral}/{main_file_com_arbitral_path}"
        
        chile_tz = pytz.timezone('Chile/Continental')
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") 

        # Verificar si el archivo ya existe en la base de datos
        c.execute('SELECT id FROM main_files_com_arbitral WHERE name_com_arbitral = %s AND section_com_arbitral = %s AND stage_com_arbitral = %s AND bucket_name_com_arbitral = %s AND emisor_doc = %s', 
                  (main_file_com_arbitral.name, section, stage, bucket_name_com_arbitral, emisor_doc))
        existing_file = c.fetchone()
        
        if existing_file:
            return st.warning(f'El archivo "{main_file_com_arbitral.name}" ya existe.')
        else:
            # Registrar en la base de datos
            c.execute('INSERT INTO main_files_com_arbitral(name_com_arbitral, section_com_arbitral, stage_com_arbitral, gcs_path_com_arbitral, bucket_name_com_arbitral, uploaded_at_com_arbitral, emisor_doc) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                  (main_file_com_arbitral.name, section, stage, main_gcs_path_com_arbitral, bucket_name_com_arbitral, current_time, emisor_doc))
        main_file_com_arbitral_id = c.lastrowid

        for attached_file in uploaded_files[1:]:
            attached_file_path=f"attachments/{attached_file.name}"
            storage_client.upload_fileobj(attached_file, bucket_name_com_arbitral, attached_file_path)
            attached_gcs_path_com_arbitral = f"gs://{bucket_name_com_arbitral}/{attached_file_path}"

            c.execute('INSERT INTO attached_files_com_arbitral (main_file_com_arbitral_id, name, gcs_path_com_arbitral, uploaded_at_com_arbitral) VALUES (%s,%s,%s,%s)',
                       (main_file_com_arbitral_id, attached_file.name, attached_gcs_path_com_arbitral, current_time))

        conn.commit()
        st.success(f'Archivos subidos y registrados con éxito.')

    except Exception as e:
        return st.error(f'Error al subir el archivo: {e}')

    finally:
        c.close()
        conn.close()

def notify_abogados_com_arbitral(selected_users, bucket_name_com_arbitral, main_file_name):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        if selected_users:
            subject = "Notificación de nueva resolución"
            message = f"Se ha dictado una nueva resolución: {main_file_name}. Puedes acceder a la resolución a través del Sistema electrónico de resolución de conflictos, Plataforma Comisión Arbitral."
            for user in selected_users:
                send_email(user, subject, message)

                # Registrar la notificación en la base de datos
                chile_tz = pytz.timezone('Chile/Continental')
                current_time = datetime.now(chile_tz).strftime("%Y-%m-%d %H:%M:%S")
                c.execute('INSERT INTO notificaciones_com_arbitral(bucket_name_com_arbitral, archivo, fecha, emails) VALUES (%s, %s, %s, %s)',
                          (bucket_name_com_arbitral, main_file_name, current_time, ', '.join(selected_users)))
                conn.commit()

                st.success("Notificaciones enviadas y registradas con éxito.")
        else:
            st.warning("No se encontraron usuarios para notificar.")
    except Exception as e:
        st.error(f'Error al enviar notificaciones: {e}')
    finally:
        c.close()
        conn.close()

def get_notificaciones_com_arbitral():
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute('SELECT bucket_name_com_arbitral, archivo, fecha, emails FROM notificaciones_com_arbitral ORDER BY fecha DESC')
        notificaciones = c.fetchall()
        return notificaciones
    except Exception as e:
        st.error(f"Error al obtener las notificaciones: {e}")
        return []
    finally:
        c.close()
        conn.close()

def notify_comision_arbitral(bucket_name_com_arbitral, main_file_name):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        # Obtener los correos electrónicos de los arbitros 
        c.execute('SELECT email FROM users INNER JOIN user_permissions_com_arbitral ON users.id = user_permissions_com_arbitral.user_id_com_arbitral WHERE bucket_name_com_arbitral = %s AND role IN ("admin", "arbitro", "actuario")', (bucket_name_com_arbitral,))
        emails = c.fetchall()
        email_list = [email[0] for email in emails]

        if email_list:
            subject = "Se ha subido un nuevo archivo"
            message = f"Se ha subido un nuevo archivo: Se ha subido un nuevo archivo: {main_file_name}. Puedes acceder al documento a través del Sistema electrónico de resolución de conflictos, Plataforma Comisión Arbitral."

            for email in email_list:
                send_email(email, subject, message)

            st.success("Notificaciones enviadas al Tribunal.")
        else:
            st.warning("No se encontraron correos para notificar.")
    except Exception as e:
        st.error(f'Error al enviar notificaciones: {e}')

    finally:
        c.close()
        conn.close()

def notificaciones_interface_com_arbitral():
    st.title("Resoluciones notificadas")

    notificaciones = get_notificaciones_com_arbitral()

    if notificaciones:
        # Crear DataFrame a partir de las notificaciones
        df = pd.DataFrame(notificaciones, columns=["Causa", "Nombre de la resolución", "Fecha de notificación", "Correos a los que se notificó"])
        
        df["Fecha de notificación"] = pd.to_datetime(df["Fecha de notificación"])

        df["Fecha de notificación"] = df["Fecha de notificación"].dt.strftime("%d-%m-%Y")

        # Crear una tabla HTML con estilos CSS para los anchos de las columnas
        table_html = df.to_html(index=False, classes='not-table')

        st.markdown("""
            <style>
                .not-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .not-table th, .not-table td {
                    border: 1px solid black;
                    padding: 10px;
                    text-align: center;
                    word-wrap: break-word;
                }
                .not-table th:nth-child(1), .not-table td:nth-child(1) { width: 226px; }
                .not-table th:nth-child(2), .not-table td:nth-child(2) { width: 272px; }
                .not-table th:nth-child(3), .not-table td:nth-child(3) { width: 225px; }
            </style>
            """, unsafe_allow_html=True)

        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.write("No hay notificaciones registradas.")


# Función para guardar el archivo en GCS y registrar en la base de datos de com conciliadora
def save_uploaded_file_com_conciliadora(uploaded_files, bucket_name_com_conciliadora, emisor_doc2):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        # Guardar en el bucket de prueba
        main_file_com_conciliadora=uploaded_files[0]
        main_file_com_conciliadora_path = main_file_com_conciliadora.name
        storage_client.upload_fileobj(main_file_com_conciliadora, bucket_name_com_conciliadora, main_file_com_conciliadora_path)
        main_gcs_path_com_conciliadora = f"gs://{bucket_name_com_conciliadora}/{main_file_com_conciliadora_path}"

        chile_tz = pytz.timezone('Chile/Continental')
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") 

        # Verificar si el archivo ya existe en la base de datos
        c.execute('SELECT id FROM main_files_com_conciliadora WHERE name_com_conciliadora = %s AND bucket_name_com_conciliadora = %s AND emisor_doc2 = %s', 
                  (main_file_com_conciliadora.name, bucket_name_com_conciliadora, emisor_doc2))
        existing_file = c.fetchone()
        
        if existing_file:
            return st.warning(f'El archivo "{main_file_com_conciliadora.name}" ya existe.')
        else:
            # Registrar en la base de datos
            c.execute('INSERT INTO main_files_com_conciliadora(name_com_conciliadora, gcs_path_com_conciliadora, bucket_name_com_conciliadora, uploaded_at_com_conciliadora, emisor_doc2) VALUES (%s, %s, %s, %s, %s)', 
                  (main_file_com_conciliadora.name, main_gcs_path_com_conciliadora, bucket_name_com_conciliadora, current_time, emisor_doc2))

        main_file_com_conciliadora_id=c.lastrowid

        for attached_file in uploaded_files[1:]:
            attached_file_path=f"attachments/{attached_file.name}"
            storage_client.upload_fileobj(attached_file, bucket_name_com_conciliadora, attached_file_path)
            attached_gcs_path_com_conciliadora = f"gs://{bucket_name_com_conciliadora}/{attached_file_path}"

            c.execute('INSERT INTO attached_files_com_conciliadora(main_file_com_conciliadora_id, name, gcs_path_com_conciliadora, uploaded_at_com_conciliadora) VALUES (%s,%s,%s,%s)',
                       (main_file_com_conciliadora_id, attached_file.name, attached_gcs_path_com_conciliadora, current_time))
        conn.commit()
        st.success(f'Archivos subidos y registrados con éxito.')

    except Exception as e:
        return st.error(f'Error al subir el archivo: {e}')
    
    finally:
        c.close()
        conn.close()

def notify_abogados_com_conciliadora(selected_users, bucket_name_com_conciliadora, main_file_name):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        if selected_users:
            subject = "Notificación de nueva resolución"
            message = f"Se ha dictado una nueva resolución: {main_file_name}. Puedes acceder a la resolución a través del Sistema electrónico de resolución de conflictos, Plataforma Comisión Conciliadora."

            for user in selected_users:
                send_email(user, subject, message)

            # Registrar la notificación en la base de datos
            chile_tz = pytz.timezone('Chile/Continental')
            current_time = datetime.now(chile_tz).strftime("%Y-%m-%d %H:%M:%S")
            c.execute('INSERT INTO notificaciones_com_conciliadora(bucket_name_com_conciliadora, archivo, fecha, emails) VALUES (%s, %s, %s, %s)',
                      (bucket_name_com_conciliadora, main_file_name, current_time, ', '.join(selected_users)))
            conn.commit()

            st.success("Notificaciones enviadas y registradas con éxito.")
        else:
            st.warning("No se encontraron abogados para notificar.")
    except Exception as e:
        st.error(f'Error al enviar notificaciones: {e}')
    finally:
        c.close()
        conn.close()

def get_notificaciones_com_conciliadora():
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()
    try:
        c.execute('SELECT bucket_name_com_conciliadora, archivo, fecha, emails FROM notificaciones_com_conciliadora ORDER BY fecha DESC')
        notificaciones = c.fetchall()
        return notificaciones
    except Exception as e:
        st.error(f"Error al obtener las notificaciones: {e}")
        return []
    finally:
        c.close()
        conn.close()

def notificaciones_interface_com_conciliadora():

    st.title("Resoluciones notificadas")

    notificaciones = get_notificaciones_com_conciliadora()

    if notificaciones:
        # Crear DataFrame a partir de las notificaciones
        df = pd.DataFrame(notificaciones, columns=["Causa", "Nombre de la resolución", "Fecha de notificación", "Correos a los que se notificó"])
        
        df["Fecha de notificación"] = pd.to_datetime(df["Fecha de notificación"])

        df["Fecha de notificación"] = df["Fecha de notificación"].dt.strftime("%d-%m-%Y")

        # Crear una tabla HTML con estilos CSS para los anchos de las columnas
        table_html = df.to_html(index=False, classes='not-table')

        st.markdown("""
            <style>
                .not-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .not-table th, .not-table td {
                    border: 1px solid black;
                    padding: 10px;
                    text-align: center;
                    word-wrap: break-word;
                }
                .not-table th:nth-child(1), .not-table td:nth-child(1) { width: 226px; }
                .not-table th:nth-child(2), .not-table td:nth-child(2) { width: 272px; }
                .not-table th:nth-child(3), .not-table td:nth-child(3) { width: 225px; }
            </style>
            """, unsafe_allow_html=True)

        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.write("No hay notificaciones registradas.")


    conn.close()

def notify_comision_conciliadora(bucket_name_com_conciliadora, main_file_name):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        # Obtener los correos electrónicos de los arbitros 
        c.execute('SELECT email FROM users INNER JOIN user_permissions_com_conciliadora ON users.id = user_permissions_com_conciliadora.user_id_com_conciliadora WHERE bucket_name_com_conciliadora = %s AND role In ("admin", "arbitro", "actuario")', (bucket_name_com_conciliadora,))
        emails = c.fetchall()
        email_list = [email[0] for email in emails]

        if email_list:
            subject = "Se ha subido un nuevo archivo"
            message = f"Se ha subido un nuevo archivo: {main_file_name}. Puedes acceder al documento a través de la plataforma."

            for email in email_list:
                send_email(email, subject, message)

            st.success("Notificaciones enviadas y registradas con éxito.")
        else:
            st.warning("No se encontraron correos para notificar.")
    except Exception as e:
        st.error(f'Error al enviar notificaciones: {e}')

    finally:
        c.close()
        conn.close()

def update_user_role(user_id, role):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute("UPDATE users SET role = %s WHERE id = %s", (role, user_id))
        conn.commit()
        st.success("Rol del usuario actualizado.")
    except Exception as e:
        st.error(f"Error en actualizar rol del usuario: {e}")

    finally:
        c.close()
        conn.close()

def get_all_buckets_com_arbitral():
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute("SELECT DISTINCT bucket_name_com_arbitral FROM user_permissions_com_arbitral")
        bucketsca = [row[0] for row in c.fetchall()]
        return bucketsca
    except Exception as e:
        st.error(f"Error en obtener buckets de Comisión Arbitral: {e}")
        return []
    finally:
        c.close()
        conn.close()

def get_all_buckets_com_conciliadora():
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute("SELECT DISTINCT bucket_name_com_conciliadora FROM user_permissions_com_conciliadora")
        bucketscc = [row[0] for row in c.fetchall()]
        return bucketscc
    except Exception as e:
        st.error(f"Error en obtener buckets de Comisión Conciliadora: {e}")
        return []
    finally:
        c.close()
        conn.close()

def update_user_buckets_com_arbitral(user_id, buckets_com_arbitral):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute("DELETE FROM user_permissions_com_arbitral WHERE user_id_com_arbitral = %s", (user_id,))
        for bucket1 in buckets_com_arbitral:
            c.execute("INSERT INTO user_permissions_com_arbitral (user_id_com_arbitral, bucket_name_com_arbitral) VALUES (%s, %s)", (user_id, bucket1))
        conn.commit()
        st.success("Causas del usuario actualizadas.")
    except Exception as e:
        st.error(f"Error en actualizar las causas del usuario: {e}")
    finally:
        c.close()
        conn.close()

def update_user_buckets_com_conciliadora(user_id, buckets_com_conciliadora):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute("DELETE FROM user_permissions_com_conciliadora WHERE user_id_com_conciliadora = %s", (user_id,))
        for bucket2 in buckets_com_conciliadora:
            c.execute("INSERT INTO user_permissions_com_conciliadora (user_id_com_conciliadora, bucket_name_com_conciliadora) VALUES (%s, %s)", (user_id, bucket2))
        conn.commit()
        st.success("Causas del usuario actualizadas.")
    except Exception as e:
        st.error(f"Error en actualizar las causas del usuario: {e}")

    finally:
        c.close()
        conn.close()

def generate_signed_url(bucket_name, blob_name, expiration=3600):
    """Genera una URL firmada para acceder a un archivo en Google Cloud Storage."""
    try:
        url = storage_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': blob_name},
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        print(f"Error al generar la URL firmada: {e}")
        return None

def get_public_url_com_arbitral(bucket_name_com_arbitral, gcs_path_com_arbitral, expiration=3600):
    try:
        # Verificar y limpiar la ruta de Google Cloud Storage si es necesario
        if gcs_path_com_arbitral.startswith("gs://"):
            gcs_path_com_arbitral = gcs_path_com_arbitral[5:]  # Eliminar "gs://" del inicio
        
        # Verificar y limpiar la ruta dentro del bucket si es necesario
        if gcs_path_com_arbitral.startswith(f"{bucket_name_com_arbitral}/"):
            gcs_path_com_arbitral = gcs_path_com_arbitral[len(bucket_name_com_arbitral) + 1:]  # Eliminar "{bucket_name}/" del inicio
        
        # Construir la URL pública del archivo
        url = generate_signed_url(bucket_name_com_arbitral,gcs_path_com_arbitral, expiration)
        return url
    except Exception as e:
        print(f"Error al obtener enlace público: {e}")
        return None

def get_public_url_com_conciliadora(bucket_name_com_conciliadora, gcs_path_com_conciliadora, expiration=3600):
    try:
        # Verificar y limpiar la ruta de Google Cloud Storage si es necesario
        if gcs_path_com_conciliadora.startswith("gs://"):
            gcs_path_com_conciliadora = gcs_path_com_conciliadora[5:]  # Eliminar "gs://" del inicio
        
        # Verificar y limpiar la ruta dentro del bucket si es necesario
        if gcs_path_com_conciliadora.startswith(f"{bucket_name_com_conciliadora}/"):
            gcs_path_com_conciliadora = gcs_path_com_conciliadora[len(bucket_name_com_conciliadora) + 1:]  # Eliminar "{bucket_name}/" del inicio
        
        # Construir la URL pública del archivo
        url2 = generate_signed_url(bucket_name_com_conciliadora, gcs_path_com_conciliadora, expiration)
        return url2
    except Exception as e:
        print(f"Error al obtener enlace público: {e}")
        return None

# Función para listar archivos subidos com arbitral
def list_files_com_arbitral(bucket_name_com_arbitral):

    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    st.title("Visualizar los archivos de la causa")
    chile_tz = pytz.timezone('Chile/Continental')
    st.write("")
    section_com_arbitral = st.selectbox("Selecciona el cuaderno", ["Principal", "Incidente"], key="select_section_list")

    try:
    
        # Utiliza una consulta diferente según el rol del usuario
        if st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
            query = '''
                SELECT id, name_com_arbitral, stage_com_arbitral, gcs_path_com_arbitral, emisor_doc, uploaded_at_com_arbitral, proveido_com_arbitral
                FROM main_files_com_arbitral 
                WHERE bucket_name_com_arbitral = %s AND section_com_arbitral = %s
                ORDER BY id
            '''
        else:
            query = '''
                SELECT id, name_com_arbitral, stage_com_arbitral, gcs_path_com_arbitral, emisor_doc, uploaded_at_com_arbitral
                FROM main_files_com_arbitral 
                WHERE bucket_name_com_arbitral = %s AND section_com_arbitral = %s AND proveido_com_arbitral = 1
                ORDER BY id
            '''

        c.execute(query, (bucket_name_com_arbitral, section_com_arbitral))
        main_files_com_arbitral = c.fetchall()
        
        if main_files_com_arbitral:
            # Ajuste de CSS para columnas y filas de la tabla
            st.markdown("""
                <style>
                    table { width: 150%; border-collapse: collapse}            
                    th, td { border: 1px solid black; border: padding: 10px; text-align: center; }
                    th:nth-child(1), td:nth-child(1) { width: 40px; }  /* Columna de números */
                    th:nth-child(2), td:nth-child(2) { width: 100px; }  /* Columna de etapa */
                    th:nth-child(3), td:nth-child(3) { width: 130px; }  /* Columna de nombre del archivo */
                    th:nth-child(4), td:nth-child(4) { width: 120px; }  /* Columna de emisor */                
                    th:nth-child(5), td:nth-child(5) { width: 100px; }  /* Columna de fecha de subida */
                    th:nth-child(6), td:nth-child(6) { width: 70px; }  /* Columna de visualizar */
                    th:nth-child(7), td:nth-child(7) { width: 70px; }  /* Columna de adjuntos */
                    th:nth-child(8), td:nth-child(8) { width: 65px; }  /* Columna de proveído */
                    .custom-select { width: 85px; }
                    ul.no-bullets { list-style-type: none; text-align: left; }
                </style>
                """, unsafe_allow_html=True)
            st.markdown("<table>", unsafe_allow_html=True)

            if st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
                st.markdown("<tr> <th>#</th> <th>Etapa</th> <th>Nombre del archivo</th> <th>Emisor</th> <th>Fecha</th> <th>Doc.</th> <th>Adj.</th> <th>Prov.</th> </tr>", unsafe_allow_html=True)
            else:
                st.markdown("<tr> <th>#</th> <th>Etapa</th> <th>Nombre del archivo</th> <th>Emisor</th> <th>Fecha</th> <th>Doc.</th> <th>Adj.</th> </tr>", unsafe_allow_html=True)      

            for idx, main_file_com_arbitral in enumerate(main_files_com_arbitral, start=1):
                if st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
                    main_file_com_arbitral_id, name_com_arbitral, stage_com_arbitral, main_gcs_path_com_arbitral, emisor_doc, uploaded_at_com_arbitral, proveido_com_arbitral = main_file_com_arbitral
                else:
                    main_file_com_arbitral_id, name_com_arbitral, stage_com_arbitral, main_gcs_path_com_arbitral, emisor_doc, uploaded_at_com_arbitral = main_file_com_arbitral

                if uploaded_at_com_arbitral:

                    if uploaded_at_com_arbitral.tzinfo is None:
                        utc_uploaded_at_com_arbitral = uploaded_at_com_arbitral.replace(tzinfo=timezone.utc)
                    else:
                        utc_uploaded_at_com_arbitral = uploaded_at_com_arbitral.astimezone(timezone.utc)
                    local_uploaded_at_com_arbitral = utc_uploaded_at_com_arbitral.astimezone(chile_tz)
                    # Cambiado para mostrar día, mes y año en ese orden
                    formatted_date = local_uploaded_at_com_arbitral.strftime("%d-%m-%y %H:%M")
                else:
                    formatted_date = "N/A"

                main_file_url = get_public_url_com_arbitral(bucket_name_com_arbitral, main_gcs_path_com_arbitral)

                c.execute('SELECT name, gcs_path_com_arbitral FROM attached_files_com_arbitral WHERE main_file_com_arbitral_id=%s', (main_file_com_arbitral_id,))
                attached_files=c.fetchall()
                attached_files_html=""
                for attached_file in attached_files:
                    attached_file_name, attached_gcs_path_com_arbitral=attached_file
                    attached_file_url=get_public_url_com_arbitral(bucket_name_com_arbitral, attached_gcs_path_com_arbitral)
                    attached_files_html += f"<div><a href='{attached_file_url}' target='_blank'>Adj.</a></div>"
                attached_files_html+="</ul>"

                if st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
                    st.markdown(f"<tr> <td>{idx}</td> <td>{stage_com_arbitral or 'N/A'}</td> <td>{name_com_arbitral}</td> <td>{emisor_doc or 'N/A'}</td> <td>{formatted_date}</td> <td><a href='{main_file_url}' target='_blank'>Doc. {idx}</a></td> <td>{attached_files_html}</td> <td>{proveido_com_arbitral}</td> </tr>", unsafe_allow_html=True)
                    
                    # Agregar opción para marcar como proveído
                    if not proveido_com_arbitral and st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
                        if st.button(f"Marcar como proveído - {name_com_arbitral}", key=f"proveido_{main_file_com_arbitral_id}"):
                            c.execute('UPDATE main_files_com_arbitral SET proveido_com_arbitral = 1 WHERE id = %s', (main_file_com_arbitral_id,))
                            conn.commit()
                            st.success(f"El archivo '{name_com_arbitral}' ha sido marcado como proveído.")
                            st.rerun()
                else:
                    st.markdown(f"<tr> <td>{idx}</td> <td>{stage_com_arbitral or 'N/A'}</td> <td>{name_com_arbitral}</td> <td>{emisor_doc or 'N/A'}</td> <td>{formatted_date}</td> <td><a href='{main_file_url}' target='_blank'>Doc. {idx}</a></td> <td>{attached_files_html}</td> </tr>", unsafe_allow_html=True)
                
            st.markdown("</table>", unsafe_allow_html=True)
        else:
            st.write("No hay archivos subidos.")
    except Exception as e:
        st.error(f'Error al listar archivos: {e}')

    finally:
        c.close()
        conn.close()


# Función para listar archivos subidos com conciliadora
def list_files_com_conciliadora(bucket_name_com_conciliadora):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    st.title("Visualizar archivos de la causa")
    chile_tz = pytz.timezone('Chile/Continental')

    try:
    
        # Utiliza una consulta diferente según el rol del usuario
        if st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
            query = '''
                SELECT id, name_com_conciliadora, gcs_path_com_conciliadora, emisor_doc2, uploaded_at_com_conciliadora, proveido_com_conciliadora
                FROM main_files_com_conciliadora
                WHERE bucket_name_com_conciliadora = %s
                ORDER BY id
            '''
        else:
            query = '''
                SELECT id, name_com_conciliadora, gcs_path_com_conciliadora, emisor_doc2, uploaded_at_com_conciliadora
                FROM main_files_com_conciliadora 
                WHERE bucket_name_com_conciliadora = %s AND proveido_com_conciliadora = 1
                ORDER BY id
            '''

        c.execute(query, (bucket_name_com_conciliadora,))
        main_files_com_conciliadora = c.fetchall()
        
        if main_files_com_conciliadora:
            # Ajuste de CSS para columnas y filas de la tabla
            st.markdown("""
                <style>
                    table { width: 150%; border-collapse: collapse; table-layout: fixed;}  /* Ajuste de ancho de tabla a 100% */
                    th, td { border: 1px solid black; padding: 10px; text-align: center; }
                    th:nth-child(1), td:nth-child(1) { width: 60px; }  /* Columna de números */
                    th:nth-child(2), td:nth-child(2) { width: 145px; }  /* Columna de nombre del archivo */
                    th:nth-child(3), td:nth-child(3) { width: 140px; }  /* Columna de emisor */
                    th:nth-child(4), td:nth-child(4) { width: 110px; }  /* Columna de fecha de subida */
                    th:nth-child(5), td:nth-child(5) { width: 90px; }  /* Columna de visualizar */                    
                    th:nth-child(6), td:nth-child(6) { width: 90px; }  /* Columna de adjuntos */
                    th:nth-child(7), td:nth-child(7) { width: 65px; }  /* Columna de proveído */
                    .custom-select { width: 85px; }
                    ul.no-bullets { list-style-type: none; text-align: left; }
                </style>
                """, unsafe_allow_html=True)
            st.markdown("<table>", unsafe_allow_html=True)

            if st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
                st.markdown("<tr> <th>#</th> <th>Nombre del archivo</th> <th>Emisor</th> <th>Fecha y hora</th> <th>Doc.</th> <th>Adj.</th> <th>Prov.</th> </tr>", unsafe_allow_html=True)
            else:
                st.markdown("<tr> <th>#</th> <th>Nombre del archivo</th> <th>Emisor</th> <th>Fecha y hora</th> <th>Doc.</th> <th>Adj.</th> </tr>", unsafe_allow_html=True)     

            for idx, main_file_com_conciliadora in enumerate(main_files_com_conciliadora, start=1):
                if st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
                    main_file_com_conciliadora_id, name_com_conciliadora, main_gcs_path_com_conciliadora, emisor_doc2, uploaded_at_com_conciliadora, proveido_com_conciliadora = main_file_com_conciliadora
                else:
                    main_file_com_conciliadora_id, name_com_conciliadora, main_gcs_path_com_conciliadora, emisor_doc2, uploaded_at_com_conciliadora = main_file_com_conciliadora

                if uploaded_at_com_conciliadora:
                    if uploaded_at_com_conciliadora.tzinfo is None:
                        utc_uploaded_at_com_conciliadora = uploaded_at_com_conciliadora.replace(tzinfo=timezone.utc)
                    else:
                        utc_uploaded_at_com_conciliadora = uploaded_at_com_conciliadora.astimezone(timezone.utc)
                    local_uploaded_at_com_conciliadora = utc_uploaded_at_com_conciliadora.astimezone(chile_tz)
                    # Cambiado para mostrar día, mes y año en ese orden
                    formatted_date = local_uploaded_at_com_conciliadora.strftime("%d-%m-%y %H:%M")
                else:
                    formatted_date = "N/A"

                main_file_url = get_public_url_com_conciliadora(bucket_name_com_conciliadora, main_gcs_path_com_conciliadora)

                c.execute('SELECT name, gcs_path_com_conciliadora FROM attached_files_com_conciliadora WHERE main_file_com_conciliadora_id=%s', (main_file_com_conciliadora_id,))
                attached_files=c.fetchall()
                attached_files_html=""
                for attached_file in attached_files:
                    attached_file_name, attached_gcs_path_com_conciliadora=attached_file
                    attached_file_url=get_public_url_com_conciliadora(bucket_name_com_conciliadora, attached_gcs_path_com_conciliadora)
                    attached_files_html += f"<div><a href='{attached_file_url}' target='_blank'>Adj.</a></div>"
                attached_files_html+="</ul>"


                if st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
                    st.markdown(f"<tr> <td>{idx}</td> <td>{name_com_conciliadora}</td> <td>{emisor_doc2 or 'N/A'}</td> <td>{formatted_date}</td> <td><a href='{main_file_url}' target='_blank'>Doc. {idx}</a></td> <td>{attached_files_html}</td> <td>{proveido_com_conciliadora}</td> </tr>", unsafe_allow_html=True)
                    
                    # Agregar opción para marcar como proveído
                    if not proveido_com_conciliadora and st.session_state['user_role'] in ['admin', 'arbitro', 'actuario']:
                        if st.button(f"Marcar como proveído - {name_com_conciliadora}", key=f"proveido_{main_file_com_conciliadora_id}"):
                            c.execute('UPDATE main_files_com_conciliadora SET proveido_com_conciliadora = 1 WHERE id = %s', (main_file_com_conciliadora_id,))
                            conn.commit()
                            st.success(f"El archivo '{name_com_conciliadora}' ha sido marcado como proveído.")
                            st.rerun()
                else:
                    st.markdown(f"<tr> <td>{idx}</td> <td>{name_com_conciliadora}</td> <td>{emisor_doc2 or 'N/A'}</td> <td>{formatted_date}</td> <td><a href='{main_file_url}' target='_blank'>Doc. {idx}</a></td> <td>{attached_files_html}</td> </tr>", unsafe_allow_html=True)
            
            st.markdown("</table>", unsafe_allow_html=True)
        else:
            st.write("No hay archivos subidos.")
    except Exception as e:
        st.error(f'Error al listar archivos: {e}')

    finally:
        c.close()
        conn.close()

#PENDIENTE

load_dotenv()
# Obtener las variables de entorno
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')
from_email = os.getenv('FROM_EMAIL')
from_password = os.getenv('FROM_PASSWORD')

# Función para enviar correo electrónico
def send_email(to_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Correo enviado a", to_email)
    except Exception as e:
        print("Error al enviar correo:", e)


def save_temp_uploaded_file(uploaded_file):
    temp_file_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_file_path


# Obtener bukets
def get_user_buckets_com_arbitral(user_id):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute('SELECT bucket_name_com_arbitral FROM user_permissions_com_arbitral WHERE user_id_com_arbitral = %s', (user_id,))
        buckets = [row[0] for row in c.fetchall()]
        return buckets
    except Exception as e:
        st.error(f'Error al obtener buckets del usuario (Comisión Arbitral): {e}')
        return []
    finally:
        c.close()
        conn.close()

def get_user_buckets_com_conciliadora(user_id):

    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute('SELECT bucket_name_com_conciliadora FROM user_permissions_com_conciliadora WHERE user_id_com_conciliadora = %s', (user_id,))
        buckets = [row[0] for row in c.fetchall()]
        return buckets
    except Exception as e:
        st.error(f'Error al obtener buckets del usuario (Comisión Conciliadora): {e}')
        return []
    finally:
        c.close()
        conn.close()

def get_causa_info_com_arbitral(bucket_name_com_arbitral):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute('SELECT tribunal, demandante, demandado, fecha_inicio FROM causa_comision_arbitral WHERE bucket_name_com_arbitral = %s', (bucket_name_com_arbitral,))
        return c.fetchone()
    finally:
        c.close()
        conn.close()

def get_causa_info_com_conciliadora(bucket_name_com_conciliadora):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()
    try:
        c.execute('SELECT comision, requirente, requerido, fecha_inicio FROM causa_comision_conciliadora WHERE bucket_name_com_conciliadora = %s', (bucket_name_com_conciliadora,))
        return c.fetchone()
    finally:
        c.close()
        conn.close()

# PENDIENTE

def send_password_reset_email(email, temp_password):

    subject = 'Restablecimiento de contraseña'
    message = f'Haga clic en el siguiente enlace para restablecer su contraseña: {reset_link}'
    send_email(email, subject, message)

# PENDIENTE
def request_password_reset(email):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute('SELECT id FROM users WHERE email = %s', (email,))
        user = c.fetchone()
        if user:
            token = secrets.token_urlsafe(16)  # Generar un token seguro
            c.execute('INSERT INTO password_resets (user_id, token) VALUES (%s, %s)', (user[0], token))
            conn.commit()
            reset_link = f"http://localhost:8501?token={token}"  # Cambia a tu URL de producción
            send_password_reset_email(email, reset_link)
            return True
        else:
            return False
    except Exception as e:
        st.error(f'Error al solicitar restablecimiento de contraseña: {e}')
    finally:
        c.close()
        conn.close()


# # PENDIENTE
def change_password(user_id, new_password):
    conn = connect_to_cloud_sql()
    if conn is None:
        return

    c = conn.cursor()

    try:
        c.execute('UPDATE users SET password = %s WHERE id = %s', (new_password, user_id))
        conn.commit()
        st.success('Contraseña actualizada exitosamente.')
    except Exception as e:
        st.error(f'Error al actualizar la contraseña: {e}')
    finally:
        c.close()
        conn.close()

def reset_password_interface():
    st.header('Cambiar Contraseña')

    user_id = st.session_state.get('user_id')
    if not user_id:
        st.error('No se encontró información del usuario. Inicie sesión nuevamente.')
        return

    new_password = st.text_input('Nueva Contraseña', type='password')
    confirm_password = st.text_input('Confirmar Nueva Contraseña', type='password')

    if st.button('Cambiar Contraseña'):
        if new_password != confirm_password:
            st.error('Las contraseñas no coinciden.')
        else:
            if change_password(user_id, new_password):
                st.success('Contraseña actualizada exitosamente.')


def login(email, password):
    conn = connect_to_cloud_sql()
    if conn is None:
        return False

    c = conn.cursor()
    try:
        c.execute('SELECT id FROM users WHERE email = %s AND password = %s', (email, password))
        user = c.fetchone()
        if user:
            st.session_state['user_id'] = user[0]
            st.session_state['email'] = email
            return True
        return False
    except Exception as e:
        st.error(f'Error al iniciar sesión: {e}')
        return False
    finally:
        c.close()
        conn.close()

def login_interface():
    st.header('Iniciar Sesión')

    email = st.text_input('Correo Electrónico')
    password = st.text_input('Contraseña', type='password')

    if st.button('Iniciar Sesión'):
        if login(email, password):
            st.success('Inicio de sesión exitoso.')
            st.experimental_rerun()  # Recarga la página para mostrar la interfaz de cambio de contraseña
        else:
            st.error('Correo electrónico o contraseña incorrectos.')
# Inicio de la aplicación

st.markdown(
    """
    <style>
    .app-header {
        background-color: #00236F;
        padding: 10px;
        text-align: center;
        font-size: 24px;
        color: white;
    }
    </style>
    <div class="app-header">Sistema electrónico de resolución de conflictos</div>
    """,
    unsafe_allow_html=True
)

# Opciones de autenticación
st.write("")
st.write("")
st.write("")

st.markdown("""
    <style>
    .stButton > button {
        background-color: #DCEAF7;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)


def main():

    if 'user_id_com_arbitral' in st.session_state:
        main_interface_com_arbitral()

    elif 'user_id_com_conciliadora' in st.session_state:
        main_interface_com_conciliadora()

    elif 'user_id' in st.session_state:
        reset_password_interface()

    else:
        st.markdown("**SELECCIONA UNA PLATAFORMA:**")

        auth_option = st.radio("_", ("Plataforma Comisión Conciliadora", "Plataforma Comisión Arbitral"))

        if auth_option == "Plataforma Comisión Conciliadora":
            username = st.text_input("Usuario (Plataforma Comisión Conciliadora)")
            password = st.text_input("Contraseña (Plataforma Comisión Conciliadora)", type="password")

            if st.button("Iniciar sesión en plataforma de Comisión Conciliadora"):
                    if authenticate_com_conciliadora(username, password):
                        st.success("Inicio de sesión exitoso")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos en plataforma de Comisión Conciliadora")

            if st.button("Solicitar restablecimiento de contraseña"):
                reset_email = st.text_input("Correo electrónico para recuperación", key="reset_email_conciliadora")
                if request_password_reset(reset_email):
                    st.success("Correo de restablecimiento enviado")
                else:
                    st.error("Correo no encontrado")

        elif auth_option == "Plataforma Comisión Arbitral":
            username = st.text_input("Usuario (Plataforma Comisión Arbitral)")
            password = st.text_input("Contraseña (Plataforma Comisión Arbitral)", type="password")

            if st.button("Iniciar sesión en plataforma de Comisión Arbitral"):
                    if authenticate_com_arbitral(username, password):
                        st.success("Inicio de sesión exitoso")
                        st.rerun()
                    else:
                        st.error("Usuario o contraseña incorrectos en plataforma de Comisión Arbitral")
            
            if st.button("Recuperar contraseña"):
                reset_email = st.text_input("Correo electrónico para recuperación")
                if st.button("Solicitar restablecimiento de contraseña"):
                    if request_password_reset(reset_email):
                        st.success("Correo de restablecimiento enviado")
                    else:
                        st.error("Correo no encontrado")        


if __name__ == "__main__":
    main()