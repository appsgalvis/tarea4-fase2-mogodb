# Esquema de Base de Datos MongoDB - Redes Sociales

## Caso de Uso Seleccionado
**Almacenamiento de datos de redes sociales (posts, comentarios, usuarios)**

## Justificación

MongoDB es ideal para este caso de uso porque:
- Los datos de redes sociales son semiestructurados y pueden variar
- Necesidad de escalabilidad horizontal para manejar millones de usuarios
- Consultas rápidas de lectura para feeds y búsquedas
- Estructura de documentos anidados permite almacenar comentarios y reacciones dentro de posts
- Flexibilidad para agregar nuevos campos sin migraciones costosas

---

## Diagrama del Esquema

```
┌─────────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS: red_social                    │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   usuarios   │    │    posts     │    │  comentarios │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                    (Referencias)
```

---

## Estructura de Colecciones

### 1. Colección: `usuarios`

**Propósito:** Almacenar información de los usuarios de la red social.

**Estructura del Documento:**

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "username": "juan_perez",
  "email": "juan.perez@email.com",
  "nombre_completo": "Juan Pérez",
  "fecha_nacimiento": ISODate("1990-05-15"),
  "biografia": "Desarrollador de software apasionado por la tecnología",
  "foto_perfil": "https://ejemplo.com/fotos/juan_perez.jpg",
  "fecha_registro": ISODate("2024-01-10T10:30:00Z"),
  "activo": true,
  "seguidores": 1250,
  "siguiendo": 450,
  "ubicacion": {
    "ciudad": "Bogotá",
    "pais": "Colombia",
    "coordenadas": {
      "latitud": 4.6097,
      "longitud": -74.0817
    }
  },
  "preferencias": {
    "idioma": "es",
    "notificaciones_email": true,
    "perfil_publico": true
  },
  "tags_interes": ["tecnologia", "programacion", "bigdata", "mongodb"]
}
```

**Campos:**
- `_id`: ObjectId - Identificador único (generado automáticamente)
- `username`: String - Nombre de usuario único
- `email`: String - Correo electrónico único
- `nombre_completo`: String - Nombre completo del usuario
- `fecha_nacimiento`: Date - Fecha de nacimiento
- `biografia`: String - Biografía del usuario (opcional)
- `foto_perfil`: String - URL de la foto de perfil
- `fecha_registro`: Date - Fecha de registro en la plataforma
- `activo`: Boolean - Si el usuario está activo
- `seguidores`: Number - Contador de seguidores
- `siguiendo`: Number - Contador de usuarios que sigue
- `ubicacion`: Object - Información de ubicación (anidado)
  - `ciudad`: String
  - `pais`: String
  - `coordenadas`: Object
    - `latitud`: Number
    - `longitud`: Number
- `preferencias`: Object - Preferencias del usuario (anidado)
  - `idioma`: String
  - `notificaciones_email`: Boolean
  - `perfil_publico`: Boolean
- `tags_interes`: Array - Array de strings con intereses

**Índices sugeridos:**
- `username` (único)
- `email` (único)
- `fecha_registro`
- `tags_interes` (texto)

---

### 2. Colección: `posts`

**Propósito:** Almacenar los posts/publicaciones de los usuarios.

**Estructura del Documento:**

```json
{
  "_id": ObjectId("507f191e810c19729de860ea"),
  "usuario_id": ObjectId("507f1f77bcf86cd799439011"),
  "username": "juan_perez",
  "contenido": "Acabo de completar mi primera aplicación con MongoDB! 🎉 #programacion #mongodb",
  "tipo": "texto",
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
  "menciones": ["@maria_garcia", "@carlos_lopez"],
  "multimedia": [
    {
      "tipo": "imagen",
      "url": "https://ejemplo.com/imagenes/post1.jpg",
      "descripcion": "Captura de pantalla de la aplicación"
    }
  ],
  "reacciones": [
    {
      "usuario_id": ObjectId("507f1f77bcf86cd799439012"),
      "tipo": "like",
      "fecha": ISODate("2024-12-15T14:35:00Z")
    },
    {
      "usuario_id": ObjectId("507f1f77bcf86cd799439013"),
      "tipo": "love",
      "fecha": ISODate("2024-12-15T14:40:00Z")
    }
  ],
  "comentarios_embebidos": [
    {
      "_id": ObjectId("507f191e810c19729de860eb"),
      "usuario_id": ObjectId("507f1f77bcf86cd799439012"),
      "username": "maria_garcia",
      "contenido": "¡Felicitaciones! Muy buen trabajo",
      "fecha": ISODate("2024-12-15T15:00:00Z"),
      "likes": 3
    }
  ],
  "activo": true
}
```

**Campos:**
- `_id`: ObjectId - Identificador único del post
- `usuario_id`: ObjectId - Referencia al usuario que creó el post
- `username`: String - Username del autor (denormalizado para consultas rápidas)
- `contenido`: String - Contenido del post
- `tipo`: String - Tipo de post (texto, imagen, video, enlace)
- `fecha_publicacion`: Date - Fecha de publicación
- `fecha_actualizacion`: Date - Fecha de última actualización
- `visibilidad`: String - Nivel de visibilidad (publico, privado, solo_seguidores)
- `estadisticas`: Object - Estadísticas del post (anidado)
  - `likes`: Number
  - `comentarios`: Number
  - `compartidos`: Number
  - `visualizaciones`: Number
- `hashtags`: Array - Array de hashtags
- `menciones`: Array - Array de usuarios mencionados
- `multimedia`: Array - Array de objetos multimedia (anidado)
  - `tipo`: String (imagen, video, audio)
  - `url`: String
  - `descripcion`: String
- `reacciones`: Array - Array de reacciones (anidado)
  - `usuario_id`: ObjectId
  - `tipo`: String (like, love, haha, wow, sad, angry)
  - `fecha`: Date
- `comentarios_embebidos`: Array - Comentarios embebidos (opcional, para posts recientes)
  - `_id`: ObjectId
  - `usuario_id`: ObjectId
  - `username`: String
  - `contenido`: String
  - `fecha`: Date
  - `likes`: Number
- `activo`: Boolean - Si el post está activo

**Índices sugeridos:**
- `usuario_id`
- `fecha_publicacion` (descendente)
- `hashtags`
- `visibilidad`
- `estadisticas.likes` (descendente)
- Texto en `contenido` y `hashtags`

---

### 3. Colección: `comentarios`

**Propósito:** Almacenar comentarios de los posts (para posts antiguos o cuando hay muchos comentarios).

**Estructura del Documento:**

```json
{
  "_id": ObjectId("507f191e810c19729de860ec"),
  "post_id": ObjectId("507f191e810c19729de860ea"),
  "usuario_id": ObjectId("507f1f77bcf86cd799439012"),
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
      "_id": ObjectId("507f191e810c19729de860ed"),
      "usuario_id": ObjectId("507f1f77bcf86cd799439011"),
      "username": "juan_perez",
      "contenido": "Gracias! Te puedo compartir el código si quieres",
      "fecha": ISODate("2024-12-15T16:30:00Z"),
      "likes": 1
    }
  ],
  "menciones": ["@carlos_lopez"],
  "activo": true
}
```

**Campos:**
- `_id`: ObjectId - Identificador único del comentario
- `post_id`: ObjectId - Referencia al post comentado
- `usuario_id`: ObjectId - Referencia al usuario que comentó
- `username`: String - Username del autor (denormalizado)
- `contenido`: String - Contenido del comentario
- `fecha_comentario`: Date - Fecha del comentario
- `fecha_actualizacion`: Date - Fecha de última actualización
- `estadisticas`: Object - Estadísticas del comentario (anidado)
  - `likes`: Number
  - `respuestas`: Number
- `comentario_padre_id`: ObjectId - Si es respuesta a otro comentario (null si es comentario principal)
- `respuestas`: Array - Respuestas embebidas (anidado)
  - `_id`: ObjectId
  - `usuario_id`: ObjectId
  - `username`: String
  - `contenido`: String
  - `fecha`: Date
  - `likes`: Number
- `menciones`: Array - Array de usuarios mencionados
- `activo`: Boolean - Si el comentario está activo

**Índices sugeridos:**
- `post_id`
- `usuario_id`
- `fecha_comentario` (descendente)
- `comentario_padre_id`
- `estadisticas.likes` (descendente)

---

## Relaciones entre Colecciones

### Estrategia de Diseño

1. **Denormalización selectiva:**
   - Se almacena `username` en posts y comentarios para evitar joins frecuentes
   - Se almacenan estadísticas (contadores) para consultas rápidas

2. **Embebido vs Referencias:**
   - **Embebido:** Comentarios recientes en posts (para acceso rápido)
   - **Referencias:** Comentarios antiguos en colección separada (para escalabilidad)
   - **Embebido:** Reacciones en posts (para acceso rápido)
   - **Embebido:** Respuestas en comentarios (para threads cortos)

3. **Patrón de Referencias:**
   - `posts.usuario_id` → `usuarios._id`
   - `posts.comentarios_embebidos[].usuario_id` → `usuarios._id`
   - `comentarios.post_id` → `posts._id`
   - `comentarios.usuario_id` → `usuarios._id`

---

## Diagrama de Relaciones Detallado

```
usuarios
  │
  │ (1:N)
  │
  ├───► posts
  │      │
  │      │ (1:N)
  │      │
  │      └───► comentarios
  │             │
  │             │ (1:N - respuestas)
  │             │
  │             └───► respuestas (embebidas)
  │
  └───► reacciones (embebidas en posts)
```

---

## Casos de Uso de Consultas

### Consultas Principales:

1. **Obtener feed de un usuario:**
   - Posts de usuarios que sigue
   - Ordenados por fecha descendente
   - Con comentarios recientes embebidos

2. **Buscar posts por hashtag:**
   - Búsqueda en array de hashtags
   - Ordenados por popularidad (likes)

3. **Obtener comentarios de un post:**
   - Comentarios embebidos (recientes)
   - Comentarios de colección separada (antiguos)
   - Ordenados por fecha

4. **Estadísticas de usuario:**
   - Total de posts
   - Total de likes recibidos
   - Total de comentarios

---

## Consideraciones de Escalabilidad

1. **Sharding:**
   - Shard por `usuario_id` en posts
   - Shard por `post_id` en comentarios

2. **Índices:**
   - Índices compuestos para consultas frecuentes
   - Índices de texto para búsquedas

3. **TTL (Time To Live):**
   - Considerar TTL para posts antiguos si se requiere archivado

4. **Caché:**
   - Caché de feeds populares
   - Caché de estadísticas de usuarios

---

## Ejemplo de Datos de Prueba

Se recomienda crear al menos:
- 50 usuarios
- 200 posts (distribuidos entre usuarios)
- 500 comentarios (distribuidos entre posts)
- Variedad de hashtags, menciones y reacciones

---

## Herramientas para Visualizar el Esquema

### Opción 1: MongoDB Compass
- Abre MongoDB Compass
- Conecta a tu base de datos
- Visualiza las colecciones y documentos
- Exporta diagramas

### Opción 2: Draw.io / Diagrams.net
- Crea diagramas ER personalizados
- Exporta como imagen PNG/SVG

### Opción 3: dbdiagram.io
- Crea diagramas de base de datos online
- Soporte para MongoDB

### Opción 4: PlantUML
- Código para generar diagramas
- Integración con documentación

---

## Próximos Pasos

1. Crear la base de datos `red_social`
2. Crear las colecciones
3. Insertar datos de prueba (al menos 100 documentos)
4. Crear índices
5. Implementar consultas según la guía

