# Script para generar datos de prueba en formato JSON para MongoDB
# Genera al menos 100 documentos distribuidos en usuarios, posts y comentarios

import json
from datetime import datetime, timedelta
import random

ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Bucaramanga', 'Pereira', 'Santa Marta', 'Manizales', 'Armenia']
nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Laura', 'Pedro', 'Sofía', 'Diego', 'Valentina', 'Andrés', 'Camila', 'Sebastián', 'Isabella', 'Nicolás']
apellidos = ['Pérez', 'García', 'Rodríguez', 'López', 'Martínez', 'González', 'Fernández', 'Sánchez', 'Ramírez', 'Torres', 'Díaz', 'Moreno', 'Jiménez', 'Ruiz', 'Hernández']
hashtags_list = ['programacion', 'mongodb', 'bigdata', 'diseño', 'ux', 'mobile', 'web', 'javascript', 'python', 'desarrollo', 'tecnologia', 'innovacion', 'startup', 'emprendimiento', 'educacion']
contenidos_posts = [
    "Acabo de completar mi primera aplicación con MongoDB! 🎉",
    "Compartiendo algunos tips de diseño UX para aplicaciones móviles 📱",
    "Aprendiendo sobre BigData y sus aplicaciones prácticas",
    "Nuevo proyecto en desarrollo usando tecnologías modernas",
    "Tips útiles para desarrolladores principiantes",
    "Explorando las capacidades de MongoDB para proyectos escalables",
    "Diseño de interfaces intuitivas y accesibles",
    "Análisis de datos con herramientas modernas",
    "Compartiendo mi experiencia con bases de datos NoSQL",
    "Proyecto colaborativo en desarrollo"
]

# Generar usuarios (40 usuarios)
usuarios = []
base_date = datetime(2024, 1, 1)
for i in range(40):
    fecha = base_date + timedelta(days=i*3, hours=random.randint(8, 18), minutes=random.randint(0, 59))
    usuarios.append({
        "username": f"{nombres[i%15].lower()}_{apellidos[i%15].lower()}_{i}",
        "email": f"{nombres[i%15].lower()}.{apellidos[i%15].lower()}{i}@email.com",
        "nombre_completo": f"{nombres[i%15]} {apellidos[i%15]}",
        "fecha_registro": fecha.isoformat() + "Z",
        "seguidores": random.randint(100, 5000),
        "siguiendo": random.randint(50, 2000),
        "ubicacion": {
            "ciudad": ciudades[i%10],
            "pais": "Colombia"
        },
        "activo": True
    })

# Generar posts (40 posts)
posts = []
for i in range(40):
    usuario_idx = i % len(usuarios)
    fecha_post = base_date + timedelta(days=30+i*2, hours=random.randint(8, 20), minutes=random.randint(0, 59))
    hashtags = random.sample(hashtags_list, random.randint(2, 4))
    posts.append({
        "usuario_id": f"USER_ID_{usuario_idx}",
        "username": usuarios[usuario_idx]["username"],
        "contenido": f"{contenidos_posts[i%10]} #{' #'.join(hashtags)}",
        "fecha_publicacion": fecha_post.isoformat() + "Z",
        "fecha_actualizacion": fecha_post.isoformat() + "Z",
        "visibilidad": "publico",
        "estadisticas": {
            "likes": random.randint(10, 500),
            "comentarios": random.randint(2, 50),
            "compartidos": random.randint(1, 100),
            "visualizaciones": random.randint(100, 5000)
        },
        "hashtags": hashtags,
        "reacciones": [],
        "activo": True
    })

# Generar comentarios (30 comentarios)
comentarios = []
for i in range(30):
    post_idx = i % len(posts)
    usuario_idx = random.randint(0, len(usuarios)-1)
    fecha_comentario = base_date + timedelta(days=35+i*2, hours=random.randint(9, 21), minutes=random.randint(0, 59))
    comentarios.append({
        "post_id": f"POST_ID_{post_idx}",
        "usuario_id": f"USER_ID_{usuario_idx}",
        "username": usuarios[usuario_idx]["username"],
        "contenido": f"Excelente contenido! Muy útil para mi proyecto {i+1}.",
        "fecha_comentario": fecha_comentario.isoformat() + "Z",
        "fecha_actualizacion": fecha_comentario.isoformat() + "Z",
        "estadisticas": {
            "likes": random.randint(0, 50),
            "respuestas": random.randint(0, 5)
        },
        "comentario_padre_id": None,
        "respuestas": [],
        "activo": True
    })

# Guardar usuarios
with open('datos_usuarios.json', 'w', encoding='utf-8') as f:
    json.dump(usuarios, f, indent=2, ensure_ascii=False)

# Guardar posts
with open('datos_posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)

# Guardar comentarios
with open('datos_comentarios.json', 'w', encoding='utf-8') as f:
    json.dump(comentarios, f, indent=2, ensure_ascii=False)

print(f"Generados {len(usuarios)} usuarios, {len(posts)} posts y {len(comentarios)} comentarios")
print(f"Total: {len(usuarios) + len(posts) + len(comentarios)} documentos")
print(f"Archivos creados: datos_usuarios.json, datos_posts.json, datos_comentarios.json")

