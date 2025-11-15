# Script Python con consultas MongoDB - Red Social
# Incluye: Consultas basicas, filtros, operadores y agregaciones

from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['red_social']

usuarios = db['usuarios']
posts = db['posts']
comentarios = db['comentarios']

print("=" * 60)
print("CONSULTAS MONGODB - BASE DE DATOS RED SOCIAL")
print("=" * 60)

# ============================================
# 4.2.2 CONSULTAS BASICAS (CRUD)
# ============================================

print("\n" + "=" * 60)
print("4.2.2 CONSULTAS BASICAS (Insercion, Seleccion, Actualizacion y Eliminacion)")
print("=" * 60)

# --- INSERCION ---
print("\n--- INSERCION ---")
print("1. Insertar un nuevo usuario:")
nuevo_usuario = {
    "username": "pedro_sanchez",
    "email": "pedro.sanchez@email.com",
    "nombre_completo": "Pedro Sanchez",
    "fecha_registro": datetime.now(),
    "seguidores": 500,
    "siguiendo": 200,
    "ubicacion": {
        "ciudad": "Cartagena",
        "pais": "Colombia"
    }
}
# resultado_insert = usuarios.insert_one(nuevo_usuario)
# print(f"Usuario insertado con ID: {resultado_insert.inserted_id}")

# --- SELECCION ---
print("\n--- SELECCION ---")
print("2. Seleccionar todos los usuarios:")
todos_usuarios = list(usuarios.find())
print(f"Total de usuarios: {len(todos_usuarios)}")
for usuario in todos_usuarios[:2]:  # Mostrar solo los primeros 2
    print(f"  - {usuario['username']}: {usuario['nombre_completo']}")

print("\n3. Seleccionar un usuario especifico por username:")
usuario = usuarios.find_one({"username": "juan_perez"})
if usuario:
    print(f"  Usuario encontrado: {usuario['nombre_completo']} ({usuario['email']})")

print("\n4. Seleccionar todos los posts:")
todos_posts = list(posts.find())
print(f"Total de posts: {len(todos_posts)}")
for post in todos_posts:
    print(f"  - Post de {post['username']}: {post['contenido'][:50]}...")

print("\n5. Seleccionar todos los comentarios:")
todos_comentarios = list(comentarios.find())
print(f"Total de comentarios: {len(todos_comentarios)}")
for comentario in todos_comentarios:
    print(f"  - Comentario de {comentario['username']}: {comentario['contenido'][:40]}...")

# --- ACTUALIZACION ---
print("\n--- ACTUALIZACION ---")
print("6. Actualizar el numero de seguidores de un usuario:")
resultado_update = usuarios.update_one(
    {"username": "juan_perez"},
    {"$set": {"seguidores": 1300}}
)
print(f"  Documentos actualizados: {resultado_update.modified_count}")

print("\n7. Actualizar multiples campos de un post:")
resultado_update2 = posts.update_one(
    {"username": "juan_perez"},
    {
        "$set": {
            "estadisticas.likes": 50,
            "fecha_actualizacion": datetime.now()
        }
    }
)
print(f"  Documentos actualizados: {resultado_update2.modified_count}")

print("\n8. Incrementar el numero de likes en un post:")
resultado_increment = posts.update_one(
    {"username": "maria_garcia"},
    {"$inc": {"estadisticas.likes": 5}}
)
print(f"  Documentos actualizados: {resultado_increment.modified_count}")

# --- ELIMINACION ---
print("\n--- ELIMINACION ---")
print("9. Eliminar un comentario especifico (solo marcar como inactivo):")
resultado_delete = comentarios.update_one(
    {"username": "juan_perez", "activo": True},
    {"$set": {"activo": False}}
)
print(f"  Comentarios desactivados: {resultado_delete.modified_count}")

print("\n10. Eliminar un documento completamente (ejemplo - comentado para no perder datos):")
# resultado_delete_real = comentarios.delete_one({"username": "test_user"})
# print(f"  Documentos eliminados: {resultado_delete_real.deleted_count}")
print("  (Comentado para preservar datos)")

# ============================================
# 4.2.3 CONSULTAS CON FILTROS Y OPERADORES
# ============================================

print("\n" + "=" * 60)
print("4.2.3 CONSULTAS CON FILTROS Y OPERADORES")
print("=" * 60)

# --- Operadores de Comparacion ---
print("\n--- Operadores de Comparacion ---")
print("1. Usuarios con mas de 1000 seguidores:")
usuarios_populares = list(usuarios.find({"seguidores": {"$gt": 1000}}))
print(f"  Total: {len(usuarios_populares)}")
for u in usuarios_populares:
    print(f"  - {u['username']}: {u['seguidores']} seguidores")

print("\n2. Posts con menos de 50 likes:")
posts_pocos_likes = list(posts.find({"estadisticas.likes": {"$lt": 50}}))
print(f"  Total: {len(posts_pocos_likes)}")
for p in posts_pocos_likes:
    print(f"  - {p['username']}: {p['estadisticas']['likes']} likes")

print("\n3. Usuarios con seguidores entre 800 y 1500:")
usuarios_rango = list(usuarios.find({
    "seguidores": {"$gte": 800, "$lte": 1500}
}))
print(f"  Total: {len(usuarios_rango)}")
for u in usuarios_rango:
    print(f"  - {u['username']}: {u['seguidores']} seguidores")

# --- Operadores Logicos ---
print("\n--- Operadores Logicos ---")
print("4. Posts con mas de 40 likes Y mas de 10 comentarios:")
posts_populares = list(posts.find({
    "$and": [
        {"estadisticas.likes": {"$gt": 40}},
        {"estadisticas.comentarios": {"$gt": 10}}
    ]
}))
print(f"  Total: {len(posts_populares)}")
for p in posts_populares:
    print(f"  - {p['username']}: {p['estadisticas']['likes']} likes, {p['estadisticas']['comentarios']} comentarios")

print("\n5. Usuarios de Bogota O Medellin:")
usuarios_ciudades = list(usuarios.find({
    "$or": [
        {"ubicacion.ciudad": "Bogota"},
        {"ubicacion.ciudad": "Medellin"}
    ]
}))
print(f"  Total: {len(usuarios_ciudades)}")
for u in usuarios_ciudades:
    print(f"  - {u['username']}: {u['ubicacion']['ciudad']}")

print("\n6. Posts que NO son del usuario juan_perez:")
posts_otros = list(posts.find({"username": {"$ne": "juan_perez"}}))
print(f"  Total: {len(posts_otros)}")
for p in posts_otros:
    print(f"  - {p['username']}")

# --- Operadores de Array ---
print("\n--- Operadores de Array ---")
print("7. Posts que contienen el hashtag 'mongodb':")
posts_hashtag = list(posts.find({"hashtags": "mongodb"}))
print(f"  Total: {len(posts_hashtag)}")
for p in posts_hashtag:
    print(f"  - {p['username']}: {p['hashtags']}")

print("\n8. Posts que contienen CUALQUIERA de estos hashtags ['programacion', 'diseno']:")
posts_hashtags = list(posts.find({"hashtags": {"$in": ["programacion", "diseno"]}}))
print(f"  Total: {len(posts_hashtags)}")
for p in posts_hashtags:
    print(f"  - {p['username']}: {p['hashtags']}")

print("\n9. Posts con TODOS los hashtags especificados:")
posts_todos_hashtags = list(posts.find({"hashtags": {"$all": ["mongodb", "bigdata"]}}))
print(f"  Total: {len(posts_todos_hashtags)}")
for p in posts_todos_hashtags:
    print(f"  - {p['username']}: {p['hashtags']}")

# --- Operadores de Existencia ---
print("\n--- Operadores de Existencia ---")
print("10. Comentarios que tienen respuestas (array no vacio):")
comentarios_con_respuestas = list(comentarios.find({"respuestas": {"$exists": True, "$ne": []}}))
print(f"  Total: {len(comentarios_con_respuestas)}")
for c in comentarios_con_respuestas:
    print(f"  - {c['username']}: {len(c['respuestas'])} respuestas")

# --- Busqueda de Texto ---
print("\n--- Busqueda de Texto ---")
print("11. Buscar posts que contengan la palabra 'aplicacion' en el contenido:")
posts_busqueda = list(posts.find({"$text": {"$search": "aplicacion"}}))
print(f"  Total: {len(posts_busqueda)}")
for p in posts_busqueda:
    print(f"  - {p['username']}: {p['contenido'][:50]}...")

# --- Ordenamiento y Limites ---
print("\n--- Ordenamiento y Limites ---")
print("12. Top 3 usuarios con mas seguidores:")
top_usuarios = list(usuarios.find().sort("seguidores", -1).limit(3))
print("  Ranking:")
for i, u in enumerate(top_usuarios, 1):
    print(f"  {i}. {u['username']}: {u['seguidores']} seguidores")

print("\n13. Posts más recientes (ordenados por fecha):")
posts_recientes = list(posts.find().sort("fecha_publicacion", -1).limit(2))
print("  Posts más recientes:")
for p in posts_recientes:
    fecha = p['fecha_publicacion'].strftime("%Y-%m-%d")
    print(f"  - {p['username']} ({fecha}): {p['contenido'][:40]}...")

# ============================================
# 4.2.4 CONSULTAS DE AGREGACION
# ============================================

print("\n" + "=" * 60)
print("4.2.4 CONSULTAS DE AGREGACION PARA CALCULAR ESTADISTICAS")
print("=" * 60)

# --- Estadisticas Basicas ---
print("\n--- Estadisticas Basicas ---")
print("1. Contar total de documentos por coleccion:")
total_usuarios = usuarios.count_documents({})
total_posts = posts.count_documents({})
total_comentarios = comentarios.count_documents({})
print(f"  Usuarios: {total_usuarios}")
print(f"  Posts: {total_posts}")
print(f"  Comentarios: {total_comentarios}")

# --- Agregacion: Promedio ---
print("\n--- Agregacion: Promedio ---")
print("2. Calcular el promedio de seguidores de todos los usuarios:")
pipeline_promedio = [
    {
        "$group": {
            "_id": None,
            "promedio_seguidores": {"$avg": "$seguidores"},
            "total_usuarios": {"$sum": 1}
        }
    }
]
resultado_promedio = list(usuarios.aggregate(pipeline_promedio))
if resultado_promedio:
    print(f"  Promedio de seguidores: {resultado_promedio[0]['promedio_seguidores']:.2f}")
    print(f"  Total de usuarios: {resultado_promedio[0]['total_usuarios']}")

print("\n3. Calcular el promedio de likes por post:")
pipeline_promedio_likes = [
    {
        "$group": {
            "_id": None,
            "promedio_likes": {"$avg": "$estadisticas.likes"},
            "total_posts": {"$sum": 1}
        }
    }
]
resultado_likes = list(posts.aggregate(pipeline_promedio_likes))
if resultado_likes:
    print(f"  Promedio de likes: {resultado_likes[0]['promedio_likes']:.2f}")
    print(f"  Total de posts: {resultado_likes[0]['total_posts']}")

# --- Agregacion: Suma ---
print("\n--- Agregacion: Suma ---")
print("4. Calcular el total de likes de todos los posts:")
pipeline_suma = [
    {
        "$group": {
            "_id": None,
            "total_likes": {"$sum": "$estadisticas.likes"},
            "total_comentarios": {"$sum": "$estadisticas.comentarios"},
            "total_compartidos": {"$sum": "$estadisticas.compartidos"}
        }
    }
]
resultado_suma = list(posts.aggregate(pipeline_suma))
if resultado_suma:
    print(f"  Total de likes: {resultado_suma[0]['total_likes']}")
    print(f"  Total de comentarios: {resultado_suma[0]['total_comentarios']}")
    print(f"  Total de compartidos: {resultado_suma[0]['total_compartidos']}")

# --- Agregacion: Maximo y Minimo ---
print("\n--- Agregacion: Maximo y Minimo ---")
print("5. Encontrar el usuario con mas y menos seguidores:")
pipeline_max_min = [
    {
        "$group": {
            "_id": None,
            "max_seguidores": {"$max": "$seguidores"},
            "min_seguidores": {"$min": "$seguidores"},
            "usuario_max": {"$max": {"seguidores": "$seguidores", "username": "$username"}},
            "usuario_min": {"$min": {"seguidores": "$seguidores", "username": "$username"}}
        }
    }
]
resultado_max_min = list(usuarios.aggregate(pipeline_max_min))
if resultado_max_min:
    print(f"  Maximo de seguidores: {resultado_max_min[0]['max_seguidores']}")
    print(f"  Minimo de seguidores: {resultado_max_min[0]['min_seguidores']}")

# Mejor forma de obtener usuario con mas seguidores
usuario_max = usuarios.find_one(sort=[("seguidores", -1)])
usuario_min = usuarios.find_one(sort=[("seguidores", 1)])
if usuario_max and usuario_min:
    print(f"  Usuario con mas seguidores: {usuario_max['username']} ({usuario_max['seguidores']})")
    print(f"  Usuario con menos seguidores: {usuario_min['username']} ({usuario_min['seguidores']})")

# --- Agregacion: Agrupacion ---
print("\n--- Agregacion: Agrupacion ---")
print("6. Agrupar posts por usuario y calcular estadisticas:")
pipeline_grupo = [
    {
        "$group": {
            "_id": "$username",
            "total_posts": {"$sum": 1},
            "total_likes": {"$sum": "$estadisticas.likes"},
            "total_comentarios": {"$sum": "$estadisticas.comentarios"},
            "promedio_likes": {"$avg": "$estadisticas.likes"}
        }
    },
    {
        "$sort": {"total_likes": -1}
    }
]
resultado_grupo = list(posts.aggregate(pipeline_grupo))
print("  Estadisticas por usuario:")
for r in resultado_grupo:
    print(f"  - {r['_id']}:")
    print(f"    Posts: {r['total_posts']}, Total likes: {r['total_likes']}, Promedio likes: {r['promedio_likes']:.2f}")

# --- Agregacion: Filtros en Pipeline ---
print("\n--- Agregacion: Filtros en Pipeline ---")
print("7. Calcular promedio de likes solo para posts con mas de 40 likes:")
pipeline_filtrado = [
    {
        "$match": {
            "estadisticas.likes": {"$gt": 40}
        }
    },
    {
        "$group": {
            "_id": None,
            "promedio_likes_filtrado": {"$avg": "$estadisticas.likes"},
            "total_posts_filtrados": {"$sum": 1}
        }
    }
]
resultado_filtrado = list(posts.aggregate(pipeline_filtrado))
if resultado_filtrado:
    print(f"  Promedio de likes (posts > 40 likes): {resultado_filtrado[0]['promedio_likes_filtrado']:.2f}")
    print(f"  Total de posts filtrados: {resultado_filtrado[0]['total_posts_filtrados']}")

# --- Agregacion: Proyeccion y Calculos ---
print("\n--- Agregacion: Proyeccion y Calculos ---")
print("8. Calcular ratio de engagement (likes + comentarios / visualizaciones):")
pipeline_engagement = [
    {
        "$project": {
            "username": 1,
            "likes": "$estadisticas.likes",
            "comentarios": "$estadisticas.comentarios",
            "visualizaciones": "$estadisticas.visualizaciones",
            "engagement": {
                "$cond": {
                    "if": {"$gt": ["$estadisticas.visualizaciones", 0]},
                    "then": {
                        "$divide": [
                            {"$add": ["$estadisticas.likes", "$estadisticas.comentarios"]},
                            "$estadisticas.visualizaciones"
                        ]
                    },
                    "else": 0
                }
            }
        }
    },
    {
        "$sort": {"engagement": -1}
    }
]
resultado_engagement = list(posts.aggregate(pipeline_engagement))
print("  Ratio de engagement por post:")
for r in resultado_engagement:
    print(f"  - {r['username']}: {r['engagement']:.4f} (Likes: {r['likes']}, Comentarios: {r['comentarios']}, Visualizaciones: {r['visualizaciones']})")

# --- Agregacion: Unwind (Descomponer Arrays) ---
print("\n--- Agregacion: Unwind (Descomponer Arrays) ---")
print("9. Contar cuantas veces aparece cada hashtag:")
pipeline_hashtags = [
    {
        "$unwind": "$hashtags"
    },
    {
        "$group": {
            "_id": "$hashtags",
            "total_apariciones": {"$sum": 1}
        }
    },
    {
        "$sort": {"total_apariciones": -1}
    }
]
resultado_hashtags = list(posts.aggregate(pipeline_hashtags))
print("  Hashtags mas usados:")
for r in resultado_hashtags:
    print(f"  - #{r['_id']}: {r['total_apariciones']} veces")

# --- Agregacion: Lookup (Join entre colecciones) ---
print("\n--- Agregacion: Lookup (Join entre colecciones) ---")
print("10. Obtener posts con informacion del usuario (join):")
pipeline_lookup = [
    {
        "$lookup": {
            "from": "usuarios",
            "localField": "usuario_id",
            "foreignField": "_id",
            "as": "usuario_info"
        }
    },
    {
        "$unwind": "$usuario_info"
    },
    {
        "$project": {
            "username": 1,
            "contenido": 1,
            "likes": "$estadisticas.likes",
            "ciudad_usuario": "$usuario_info.ubicacion.ciudad",
            "seguidores_usuario": "$usuario_info.seguidores"
        }
    },
    {
        "$limit": 2
    }
]
resultado_lookup = list(posts.aggregate(pipeline_lookup))
print("  Posts con informacion del usuario:")
for r in resultado_lookup:
    print(f"  - {r['username']} ({r['ciudad_usuario']}, {r['seguidores_usuario']} seguidores): {r['contenido'][:40]}...")

print("\n" + "=" * 60)
print("FIN DE LAS CONSULTAS")
print("=" * 60)

# Cerrar conexión
client.close()

