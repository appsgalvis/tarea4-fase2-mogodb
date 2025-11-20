// Script de comandos MongoDB para crear base de datos - Red Social
// Ejecutar desde mongosh: mongosh < comandos_mongodb_consola.js
// O copiar y pegar los comandos directamente en mongosh

// ============================================
// 0. LIMPIAR COLECCIONES (OPCIONAL)
// ============================================

// Descomentar las siguientes líneas si quieres eliminar todos los datos existentes
// use red_social
// db.usuarios.drop()
// db.posts.drop()
// db.comentarios.drop()
// print("Colecciones limpiadas")

// ============================================
// 1. CREAR/SELECCIONAR BASE DE DATOS
// ============================================

use red_social

// ============================================
// 2. COLECCIÓN: usuarios
// ============================================

// Insertar 2 usuarios de prueba
db.usuarios.insertMany([
    {
        "username": "juan_perez",
        "email": "juan.perez@email.com",
        "nombre_completo": "Juan Pérez",
        "fecha_registro": ISODate("2024-01-10T10:30:00Z"),
        "seguidores": 1250,
        "siguiendo": 450,
        "ubicacion": {
            "ciudad": "Bogotá",
            "pais": "Colombia"
        },
        "activo": true
    },
    {
        "username": "maria_garcia",
        "email": "maria.garcia@email.com",
        "nombre_completo": "María García",
        "fecha_registro": ISODate("2024-02-15T14:20:00Z"),
        "seguidores": 890,
        "siguiendo": 320,
        "ubicacion": {
            "ciudad": "Medellín",
            "pais": "Colombia"
        },
        "activo": true
    }
])

print("Usuarios insertados: 2")

// Obtener IDs de usuarios para usar en referencias
var juan = db.usuarios.findOne({"username": "juan_perez"})
var maria = db.usuarios.findOne({"username": "maria_garcia"})

// ============================================
// 3. COLECCIÓN: posts
// ============================================

// Insertar 2 posts de prueba
db.posts.insertMany([
    {
        "usuario_id": juan._id,
        "username": "juan_perez",
        "contenido": "Acabo de completar mi primera aplicación con MongoDB! 🎉 #programacion #mongodb #bigdata",
        "fecha_publicacion": ISODate("2024-12-15T14:30:00Z"),
        "fecha_actualizacion": ISODate("2024-12-15T14:30:00Z"),
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
                "usuario_id": maria._id,
                "tipo": "like",
                "fecha": ISODate("2024-12-15T14:35:00Z")
            }
        ],
        "activo": true
    },
    {
        "usuario_id": maria._id,
        "username": "maria_garcia",
        "contenido": "Compartiendo algunos tips de diseño UX para aplicaciones móviles 📱 #diseño #ux #mobile",
        "fecha_publicacion": ISODate("2024-12-16T09:15:00Z"),
        "fecha_actualizacion": ISODate("2024-12-16T09:15:00Z"),
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
                "usuario_id": juan._id,
                "tipo": "like",
                "fecha": ISODate("2024-12-16T09:20:00Z")
            }
        ],
        "activo": true
    }
])

print("Posts insertados: 2")

// Obtener IDs de posts para usar en referencias
var post1 = db.posts.findOne({"username": "juan_perez"})
var post2 = db.posts.findOne({"username": "maria_garcia"})

// ============================================
// 4. COLECCIÓN: comentarios
// ============================================

// Insertar 2 comentarios de prueba
db.comentarios.insertMany([
    {
        "post_id": post1._id,
        "usuario_id": maria._id,
        "username": "maria_garcia",
        "contenido": "Excelente trabajo! Me gustaría saber más sobre tu implementación.",
        "fecha_comentario": ISODate("2024-12-15T16:00:00Z"),
        "fecha_actualizacion": ISODate("2024-12-15T16:00:00Z"),
        "estadisticas": {
            "likes": 5,
            "respuestas": 2
        },
        "comentario_padre_id": null,
        "respuestas": [
            {
                "_id": ObjectId(),
                "usuario_id": juan._id,
                "username": "juan_perez",
                "contenido": "Gracias! Te puedo compartir el código si quieres",
                "fecha": ISODate("2024-12-15T16:30:00Z"),
                "likes": 1
            }
        ],
        "activo": true
    },
    {
        "post_id": post2._id,
        "usuario_id": juan._id,
        "username": "juan_perez",
        "contenido": "Muy útiles estos tips! Los aplicaré en mi próximo proyecto.",
        "fecha_comentario": ISODate("2024-12-16T10:00:00Z"),
        "fecha_actualizacion": ISODate("2024-12-16T10:00:00Z"),
        "estadisticas": {
            "likes": 8,
            "respuestas": 0
        },
        "comentario_padre_id": null,
        "respuestas": [],
        "activo": true
    }
])

print("Comentarios insertados: 2")

// ============================================
// 5. CREAR ÍNDICES
// ============================================

// Índices para usuarios
db.usuarios.createIndex({"username": 1}, {"unique": true})
db.usuarios.createIndex({"email": 1}, {"unique": true})
db.usuarios.createIndex({"fecha_registro": 1})

// Índices para posts
db.posts.createIndex({"usuario_id": 1})
db.posts.createIndex({"fecha_publicacion": -1})  // -1 = descendente
db.posts.createIndex({"hashtags": 1})
db.posts.createIndex({"visibilidad": 1})
db.posts.createIndex({"estadisticas.likes": -1})
db.posts.createIndex({"contenido": "text", "hashtags": "text"})

// Índices para comentarios
db.comentarios.createIndex({"post_id": 1})
db.comentarios.createIndex({"usuario_id": 1})
db.comentarios.createIndex({"fecha_comentario": -1})
db.comentarios.createIndex({"comentario_padre_id": 1})
db.comentarios.createIndex({"estadisticas.likes": -1})

print("Índices creados exitosamente")

// ============================================
// 6. VERIFICAR DATOS
// ============================================

print("\n=== RESUMEN DE DATOS INSERTADOS ===")
print("Usuarios: " + db.usuarios.countDocuments({}))
print("Posts: " + db.posts.countDocuments({}))
print("Comentarios: " + db.comentarios.countDocuments({}))
print("Total: " + (db.usuarios.countDocuments({}) + db.posts.countDocuments({}) + db.comentarios.countDocuments({})) + " documentos")

print("\n✅ Base de datos creada exitosamente")

