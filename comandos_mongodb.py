# Script Python para crear base de datos MongoDB - Red Social
# Requiere: pip install pymongo

from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')
# O para MongoDB Atlas:
# client = MongoClient('mongodb+srv://usuario:password@cluster.mongodb.net/')

# Crear/seleccionar base de datos
db = client['red_social']

# ============================================
# 0. LIMPIAR COLECCIONES (OPCIONAL - Descomentar si necesitas empezar desde cero)
# ============================================

# Descomentar las siguientes líneas si quieres eliminar todos los datos existentes
# db['usuarios'].drop()
# db['posts'].drop()
# db['comentarios'].drop()
# print("Colecciones limpiadas")

# ============================================
# 1. COLECCIÓN: usuarios
# ============================================

usuarios = db['usuarios']

# Insertar 2 usuarios de prueba
usuarios_data = [
    {
        "username": "juan_perez",
        "email": "juan.perez@email.com",
        "nombre_completo": "Juan Pérez",
        "fecha_registro": datetime(2024, 1, 10, 10, 30, 0),
        "seguidores": 1250,
        "siguiendo": 450,
        "ubicacion": {
            "ciudad": "Bogotá",
            "pais": "Colombia"
        }
    },
    {
        "username": "maria_garcia",
        "email": "maria.garcia@email.com",
        "nombre_completo": "María García",
        "fecha_registro": datetime(2024, 2, 15, 14, 20, 0),
        "seguidores": 890,
        "siguiendo": 320,
        "ubicacion": {
            "ciudad": "Medellín",
            "pais": "Colombia"
        }
    }
]

resultado_usuarios = usuarios.insert_many(usuarios_data)
print(f"Usuarios insertados: {len(resultado_usuarios.inserted_ids)}")

# Obtener IDs de usuarios
juan = usuarios.find_one({"username": "juan_perez"})
maria = usuarios.find_one({"username": "maria_garcia"})

# ============================================
# 2. COLECCIÓN: posts
# ============================================

posts = db['posts']

# Insertar 2 posts de prueba
posts_data = [
    {
        "usuario_id": juan["_id"],
        "username": "juan_perez",
        "contenido": "Acabo de completar mi primera aplicación con MongoDB! 🎉 #programacion #mongodb #bigdata",
        "fecha_publicacion": datetime(2024, 12, 15, 14, 30, 0),
        "fecha_actualizacion": datetime(2024, 12, 15, 14, 30, 0),
        "visibilidad": "publico",
        "estadisticas": {
            "likes": 45,
            "comentarios": 12,
            "compartidos": 8,
            "visualizaciones": 320
        },
        "hashtags": ["programacion", "mongodb", "bigdata"],
        "reacciones": [
            {
                "usuario_id": maria["_id"],
                "tipo": "like",
                "fecha": datetime(2024, 12, 15, 14, 35, 0)
            }
        ],
        "activo": True
    },
    {
        "usuario_id": maria["_id"],
        "username": "maria_garcia",
        "contenido": "Compartiendo algunos tips de diseño UX para aplicaciones móviles 📱 #diseño #ux #mobile",
        "fecha_publicacion": datetime(2024, 12, 16, 9, 15, 0),
        "fecha_actualizacion": datetime(2024, 12, 16, 9, 15, 0),
        "visibilidad": "publico",
        "estadisticas": {
            "likes": 78,
            "comentarios": 15,
            "compartidos": 12,
            "visualizaciones": 450
        },
        "hashtags": ["diseño", "ux", "mobile"],
        "reacciones": [
            {
                "usuario_id": juan["_id"],
                "tipo": "like",
                "fecha": datetime(2024, 12, 16, 9, 20, 0)
            }
        ],
        "activo": True
    }
]

resultado_posts = posts.insert_many(posts_data)
print(f"Posts insertados: {len(resultado_posts.inserted_ids)}")

# Obtener IDs de posts
post1 = posts.find_one({"username": "juan_perez"})
post2 = posts.find_one({"username": "maria_garcia"})

# ============================================
# 3. COLECCIÓN: comentarios
# ============================================

comentarios = db['comentarios']

# Insertar 2 comentarios de prueba
comentarios_data = [
    {
        "post_id": post1["_id"],
        "usuario_id": maria["_id"],
        "username": "maria_garcia",
        "contenido": "Excelente trabajo! Me gustaría saber más sobre tu implementación.",
        "fecha_comentario": datetime(2024, 12, 15, 16, 0, 0),
        "fecha_actualizacion": datetime(2024, 12, 15, 16, 0, 0),
        "estadisticas": {
            "likes": 5,
            "respuestas": 2
        },
        "comentario_padre_id": None,
        "respuestas": [
            {
                "_id": ObjectId(),
                "usuario_id": juan["_id"],
                "username": "juan_perez",
                "contenido": "Gracias! Te puedo compartir el código si quieres",
                "fecha": datetime(2024, 12, 15, 16, 30, 0),
                "likes": 1
            }
        ],
        "activo": True
    },
    {
        "post_id": post2["_id"],
        "usuario_id": juan["_id"],
        "username": "juan_perez",
        "contenido": "Muy útiles estos tips! Los aplicaré en mi próximo proyecto.",
        "fecha_comentario": datetime(2024, 12, 16, 10, 0, 0),
        "fecha_actualizacion": datetime(2024, 12, 16, 10, 0, 0),
        "estadisticas": {
            "likes": 8,
            "respuestas": 0
        },
        "comentario_padre_id": None,
        "respuestas": [],
        "activo": True
    }
]

resultado_comentarios = comentarios.insert_many(comentarios_data)
print(f"Comentarios insertados: {len(resultado_comentarios.inserted_ids)}")

# ============================================
# 4. CREAR ÍNDICES
# ============================================

# Índices para usuarios
usuarios.create_index("username", unique=True)
usuarios.create_index("email", unique=True)
usuarios.create_index("fecha_registro")

# Índices para posts
posts.create_index("usuario_id")
posts.create_index([("fecha_publicacion", -1)])  # -1 = descendente
posts.create_index("hashtags")
posts.create_index("visibilidad")
posts.create_index([("estadisticas.likes", -1)])
posts.create_index([("contenido", "text"), ("hashtags", "text")])

# Índices para comentarios
comentarios.create_index("post_id")
comentarios.create_index("usuario_id")
comentarios.create_index([("fecha_comentario", -1)])
comentarios.create_index("comentario_padre_id")
comentarios.create_index([("estadisticas.likes", -1)])

print("Índices creados exitosamente")

# ============================================
# 5. VERIFICAR DATOS
# ============================================

print(f"\n=== RESUMEN DE DATOS INSERTADOS ===")
print(f"Usuarios: {usuarios.count_documents({})}")
print(f"Posts: {posts.count_documents({})}")
print(f"Comentarios: {comentarios.count_documents({})}")
print(f"Total: {usuarios.count_documents({}) + posts.count_documents({}) + comentarios.count_documents({})} documentos")

# Cerrar conexión
client.close()
print("\nConexión cerrada")

