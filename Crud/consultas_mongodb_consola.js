// Script de consultas MongoDB para Red Social
// Ejecutar desde mongosh: mongosh red_social < consultas_mongodb_consola.js
// O copiar y pegar los comandos directamente en mongosh

use red_social

print("=".repeat(60))
print("CONSULTAS MONGODB - BASE DE DATOS RED SOCIAL")
print("=".repeat(60))

// ============================================
// 4.2.2 CONSULTAS BASICAS (CRUD)
// ============================================

print("\n" + "=".repeat(60))
print("4.2.2 CONSULTAS BASICAS (Inserción, Selección, Actualización y Eliminación)")
print("=".repeat(60))

// --- INSERCIÓN ---
print("\n--- INSERCIÓN ---")
print("1. Insertar un nuevo usuario:")

db.usuarios.insertOne({
    "username": "pedro_sanchez",
    "email": "pedro.sanchez@email.com",
    "nombre_completo": "Pedro Sánchez",
    "fecha_registro": new Date(),
    "seguidores": 500,
    "siguiendo": 200,
    "ubicacion": {
        "ciudad": "Cartagena",
        "pais": "Colombia"
    },
    "activo": true
})

// --- SELECCIÓN ---
print("\n--- SELECCIÓN ---")
print("2. Seleccionar todos los usuarios:")
db.usuarios.find().limit(2).forEach(function(usuario) {
    print("  - " + usuario.username + ": " + usuario.nombre_completo)
})

print("\n3. Seleccionar un usuario específico por username:")
var usuario = db.usuarios.findOne({"username": "juan_perez"})
if (usuario) {
    print("  Usuario encontrado: " + usuario.nombre_completo + " (" + usuario.email + ")")
}

print("\n4. Seleccionar todos los posts:")
db.posts.find().forEach(function(post) {
    var contenidoCorto = post.contenido.substring(0, 50)
    print("  - Post de " + post.username + ": " + contenidoCorto + "...")
})

print("\n5. Seleccionar con proyección (solo campos específicos):")
db.usuarios.find({}, {"username": 1, "email": 1, "seguidores": 1}).forEach(function(u) {
    print("  - " + u.username + ": " + u.email + " (" + u.seguidores + " seguidores)")
})

// --- ACTUALIZACIÓN ---
print("\n--- ACTUALIZACIÓN ---")
print("6. Actualizar el número de seguidores de un usuario:")
var resultado = db.usuarios.updateOne(
    {"username": "juan_perez"},
    {"$set": {"seguidores": 1300}}
)
print("  Documentos actualizados: " + resultado.modifiedCount)

print("\n7. Actualizar múltiples campos de un post:")
var resultado2 = db.posts.updateOne(
    {"username": "juan_perez"},
    {
        "$set": {
            "estadisticas.likes": 50,
            "fecha_actualizacion": new Date()
        }
    }
)
print("  Documentos actualizados: " + resultado2.modifiedCount)

print("\n8. Incrementar el número de likes en un post:")
var resultado3 = db.posts.updateOne(
    {"username": "maria_garcia"},
    {"$inc": {"estadisticas.likes": 5}}
)
print("  Documentos actualizados: " + resultado3.modifiedCount)

// --- ELIMINACIÓN ---
print("\n--- ELIMINACIÓN ---")
print("9. Eliminar un documento (soft delete - marcar como inactivo):")
var resultado4 = db.comentarios.updateOne(
    {"username": "juan_perez", "activo": true},
    {"$set": {"activo": false}}
)
print("  Documentos actualizados: " + resultado4.modifiedCount)

print("\n10. Eliminar un documento completamente:")
// Descomentar para ejecutar:
// var resultado5 = db.comentarios.deleteOne({"username": "test_user"})
// print("  Documentos eliminados: " + resultado5.deletedCount)

// ============================================
// 4.2.3 CONSULTAS CON FILTROS Y OPERADORES
// ============================================

print("\n" + "=".repeat(60))
print("4.2.3 CONSULTAS CON FILTROS Y OPERADORES")
print("=".repeat(60))

// OPERADORES DE COMPARACIÓN
print("\n--- OPERADORES DE COMPARACIÓN ---")
print("11. Usuarios con más de 1000 seguidores ($gt):")
db.usuarios.find({"seguidores": {$gt: 1000}}).forEach(function(u) {
    print("  - " + u.username + ": " + u.seguidores + " seguidores")
})

print("\n12. Posts con menos de 50 likes ($lt):")
db.posts.find({"estadisticas.likes": {$lt: 50}}).forEach(function(p) {
    print("  - Post de " + p.username + ": " + p.estadisticas.likes + " likes")
})

print("\n13. Usuarios con seguidores entre 800 y 1500 ($gte, $lte):")
db.usuarios.find({"seguidores": {$gte: 800, $lte: 1500}}).forEach(function(u) {
    print("  - " + u.username + ": " + u.seguidores + " seguidores")
})

print("\n14. Posts de usuarios diferentes a juan_perez ($ne):")
db.posts.find({"username": {$ne: "juan_perez"}}).forEach(function(p) {
    print("  - Post de " + p.username)
})

// OPERADORES LÓGICOS
print("\n--- OPERADORES LÓGICOS ---")
print("15. Posts con más de 40 likes Y más de 10 comentarios ($and):")
db.posts.find({
    $and: [
        {"estadisticas.likes": {$gt: 40}},
        {"estadisticas.comentarios": {$gt: 10}}
    ]
}).forEach(function(p) {
    print("  - Post de " + p.username + ": " + p.estadisticas.likes + " likes, " + p.estadisticas.comentarios + " comentarios")
})

print("\n16. Usuarios de Bogotá O Medellín ($or):")
db.usuarios.find({
    $or: [
        {"ubicacion.ciudad": "Bogotá"},
        {"ubicacion.ciudad": "Medellín"}
    ]
}).forEach(function(u) {
    print("  - " + u.username + ": " + u.ubicacion.ciudad)
})

// OPERADORES DE ARRAY
print("\n--- OPERADORES DE ARRAY ---")
print("17. Posts con hashtag 'mongodb':")
db.posts.find({"hashtags": "mongodb"}).forEach(function(p) {
    print("  - Post de " + p.username + ": " + p.hashtags.join(", "))
})

print("\n18. Posts con hashtags 'programacion' O 'diseño' ($in):")
db.posts.find({"hashtags": {$in: ["programacion", "diseño"]}}).forEach(function(p) {
    print("  - Post de " + p.username + ": " + p.hashtags.join(", "))
})

print("\n19. Posts que contienen TODOS los hashtags 'mongodb' Y 'bigdata' ($all):")
db.posts.find({"hashtags": {$all: ["mongodb", "bigdata"]}}).forEach(function(p) {
    print("  - Post de " + p.username + ": " + p.hashtags.join(", "))
})

// ORDENAMIENTO Y LÍMITES
print("\n--- ORDENAMIENTO Y LÍMITES ---")
print("20. Usuarios ordenados por seguidores (descendente):")
db.usuarios.find().sort({"seguidores": -1}).limit(3).forEach(function(u) {
    print("  - " + u.username + ": " + u.seguidores + " seguidores")
})

print("\n21. Posts limitados a 5 resultados:")
db.posts.find().limit(5).forEach(function(p) {
    print("  - Post de " + p.username)
})

print("\n22. Paginación: saltar 10 documentos y mostrar 5:")
db.posts.find().skip(10).limit(5).forEach(function(p) {
    print("  - Post de " + p.username)
})

// ============================================
// 4.2.4 CONSULTAS DE AGREGACIÓN
// ============================================

print("\n" + "=".repeat(60))
print("4.2.4 CONSULTAS DE AGREGACIÓN PARA CALCULAR ESTADÍSTICAS")
print("=".repeat(60))

// PROMEDIO
print("\n--- PROMEDIO ($avg) ---")
print("23. Calcular el promedio de seguidores:")
var promedio = db.usuarios.aggregate([
    {
        $group: {
            _id: null,
            promedio_seguidores: {$avg: "$seguidores"},
            total_usuarios: {$sum: 1}
        }
    }
])
promedio.forEach(function(r) {
    print("  Promedio de seguidores: " + r.promedio_seguidores.toFixed(2))
    print("  Total de usuarios: " + r.total_usuarios)
})

// SUMA
print("\n--- SUMA ($sum) ---")
print("24. Calcular el total de likes de todos los posts:")
var suma = db.posts.aggregate([
    {
        $group: {
            _id: null,
            total_likes: {$sum: "$estadisticas.likes"},
            total_comentarios: {$sum: "$estadisticas.comentarios"},
            total_compartidos: {$sum: "$estadisticas.compartidos"}
        }
    }
])
suma.forEach(function(r) {
    print("  Total likes: " + r.total_likes)
    print("  Total comentarios: " + r.total_comentarios)
    print("  Total compartidos: " + r.total_compartidos)
})

// MÁXIMO Y MÍNIMO
print("\n--- MÁXIMO Y MÍNIMO ($max, $min) ---")
print("25. Encontrar usuario con más y menos seguidores:")
var maxMin = db.usuarios.aggregate([
    {
        $group: {
            _id: null,
            max_seguidores: {$max: "$seguidores"},
            min_seguidores: {$min: "$seguidores"}
        }
    }
])
maxMin.forEach(function(r) {
    print("  Máximo seguidores: " + r.max_seguidores)
    print("  Mínimo seguidores: " + r.min_seguidores)
})

// AGRUPACIÓN
print("\n--- AGRUPACIÓN ($group) ---")
print("26. Agrupar posts por usuario y calcular estadísticas:")
db.posts.aggregate([
    {
        $group: {
            _id: "$username",
            total_posts: {$sum: 1},
            total_likes: {$sum: "$estadisticas.likes"},
            total_comentarios: {$sum: "$estadisticas.comentarios"},
            promedio_likes: {$avg: "$estadisticas.likes"}
        }
    },
    {$sort: {"total_likes": -1}}
]).forEach(function(r) {
    print("  Usuario: " + r._id)
    print("    Total posts: " + r.total_posts)
    print("    Total likes: " + r.total_likes)
    print("    Promedio likes: " + r.promedio_likes.toFixed(2))
})

// FILTROS EN PIPELINE
print("\n--- FILTROS EN PIPELINE ($match) ---")
print("27. Calcular promedio solo para posts con más de 40 likes:")
db.posts.aggregate([
    {
        $match: {
            "estadisticas.likes": {$gt: 40}
        }
    },
    {
        $group: {
            _id: null,
            promedio_likes_filtrado: {$avg: "$estadisticas.likes"},
            total_posts_filtrados: {$sum: 1}
        }
    }
]).forEach(function(r) {
    print("  Promedio likes (filtrado): " + r.promedio_likes_filtrado.toFixed(2))
    print("  Total posts filtrados: " + r.total_posts_filtrados)
})

// UNWIND
print("\n--- UNWIND (Descomponer Arrays) ---")
print("28. Contar cuántas veces aparece cada hashtag:")
db.posts.aggregate([
    {$unwind: "$hashtags"},
    {
        $group: {
            _id: "$hashtags",
            total_apariciones: {$sum: 1}
        }
    },
    {$sort: {"total_apariciones": -1}}
]).forEach(function(r) {
    print("  Hashtag: " + r._id + " - Apariciones: " + r.total_apariciones)
})

// LOOKUP
print("\n--- LOOKUP (Join entre colecciones) ---")
print("29. Obtener posts con información del usuario:")
db.posts.aggregate([
    {
        $lookup: {
            from: "usuarios",
            localField: "usuario_id",
            foreignField: "_id",
            as: "usuario_info"
        }
    },
    {$unwind: "$usuario_info"},
    {
        $project: {
            username: 1,
            contenido: 1,
            likes: "$estadisticas.likes",
            ciudad_usuario: "$usuario_info.ubicacion.ciudad",
            seguidores_usuario: "$usuario_info.seguidores"
        }
    },
    {$limit: 2}
]).forEach(function(r) {
    print("  Post de " + r.username + " (" + r.ciudad_usuario + ")")
    print("    Likes: " + r.likes + ", Seguidores del usuario: " + r.seguidores_usuario)
})

print("\n" + "=".repeat(60))
print("✅ CONSULTAS COMPLETADAS")
print("=".repeat(60))

