# Fase 2: MongoDB - Red Social

Este repositorio contiene la implementación de una base de datos MongoDB para gestionar datos de una red social, incluyendo usuarios, posts y comentarios. Este proyecto forma parte de la Tarea 4 sobre Almacenamiento y Consultas de Datos en BigData.

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
4. [Diseño de la Base de Datos](#diseño-de-la-base-de-datos)
5. [Ejecución Paso a Paso](#ejecución-paso-a-paso)
6. [Estructura del Proyecto](#estructura-del-proyecto)
7. [Consultas Implementadas](#consultas-implementadas)
8. [Documentación Adicional](#documentación-adicional)

---

## 📝 Descripción del Proyecto

Este proyecto implementa una base de datos NoSQL utilizando MongoDB para almacenar y gestionar datos de una red social. El caso de uso seleccionado es ideal para MongoDB debido a:

- **Naturaleza semiestructurada de los datos**: Los datos de redes sociales pueden variar en estructura
- **Escalabilidad horizontal**: Necesidad de manejar grandes volúmenes de datos
- **Flexibilidad de esquema**: Permite agregar nuevos campos sin migraciones costosas
- **Consultas rápidas**: Optimizado para lectura de feeds y búsquedas

### Caso de Uso

**Almacenamiento de datos de redes sociales (posts, comentarios, usuarios)**

---

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.7 o superior**
- **MongoDB Community Server 8.2.1 o superior**
- **pip** (gestor de paquetes de Python)

---

## 💾 Instalación

### Paso 1: Instalar MongoDB

1. Descarga MongoDB Community Server desde el [sitio oficial de MongoDB](https://www.mongodb.com/try/download/community)
2. Ejecuta el instalador MSI para Windows
3. Durante la instalación, **no configures autenticación** (para este ejercicio se permite conexión local sin credenciales)
4. Verifica la instalación ejecutando en la terminal:

```bash
mongosh
```

O si usas una versión anterior:

```bash
mongo
```

### Paso 2: Instalar PyMongo

PyMongo es el driver oficial de Python para MongoDB. Instálalo usando pip:

```bash
pip install pymongo
```

### Paso 3: Verificar la Conexión

Asegúrate de que MongoDB esté ejecutándose. Por defecto, MongoDB se ejecuta en `localhost:27017`.

---

## 🗄️ Diseño de la Base de Datos

### Base de Datos: `red_social`

La base de datos está compuesta por tres colecciones principales:

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
```

### Colecciones

#### 1. **usuarios**
Almacena información de los usuarios de la red social.

**Campos principales:**
- `username` (String, único)
- `email` (String, único)
- `nombre_completo` (String)
- `fecha_registro` (Date)
- `seguidores` (Number)
- `siguiendo` (Number)
- `ubicacion` (Object: ciudad, pais)
- `activo` (Boolean)

#### 2. **posts**
Almacena las publicaciones de los usuarios.

**Campos principales:**
- `usuario_id` (ObjectId, referencia a usuarios)
- `username` (String, denormalizado)
- `contenido` (String)
- `fecha_publicacion` (Date)
- `estadisticas` (Object: likes, comentarios, compartidos, visualizaciones)
- `hashtags` (Array)
- `reacciones` (Array)
- `activo` (Boolean)

#### 3. **comentarios**
Almacena los comentarios de los posts.

**Campos principales:**
- `post_id` (ObjectId, referencia a posts)
- `usuario_id` (ObjectId, referencia a usuarios)
- `username` (String, denormalizado)
- `contenido` (String)
- `fecha_comentario` (Date)
- `estadisticas` (Object: likes, respuestas)
- `respuestas` (Array, comentarios anidados)
- `activo` (Boolean)

### Estrategia de Diseño

- **Denormalización selectiva**: Se almacena `username` en posts y comentarios para evitar joins frecuentes
- **Embebido vs Referencias**: Comentarios recientes y reacciones se almacenan embebidos en posts para acceso rápido
- **Índices**: Se crean índices en campos frecuentemente consultados para optimizar el rendimiento

Para más detalles sobre el esquema, consulta [ESQUEMA_REDES_SOCIALES.md](ESQUEMA_REDES_SOCIALES.md).

---

## 🚀 Ejecución Paso a Paso

### Paso 1: Crear la Base de Datos e Insertar Datos

Ejecuta el script `comandos_mongodb.py` para crear la base de datos, las colecciones y los datos de prueba:

```bash
python comandos_mongodb.py
```

**¿Qué hace este script?**

1. **Conecta a MongoDB**: Establece conexión con MongoDB en `localhost:27017`
2. **Crea/selecciona la base de datos**: Crea la base de datos `red_social`
3. **Inserta usuarios**: Crea 2 usuarios de prueba (Juan Pérez y María García)
4. **Inserta posts**: Crea 2 posts asociados a los usuarios
5. **Inserta comentarios**: Crea 2 comentarios con respuestas anidadas
6. **Crea índices**: Crea índices para optimizar las consultas
7. **Muestra resumen**: Imprime el total de documentos insertados

**Salida esperada:**

```
Usuarios insertados: 2
Posts insertados: 2
Comentarios insertados: 2
Índices creados exitosamente

=== RESUMEN DE DATOS INSERTADOS ===
Usuarios: 2
Posts: 2
Comentarios: 2
Total: 6 documentos

Conexión cerrada
```

### Paso 2: Ejecutar Consultas

Ejecuta el script `consultas_mongodb.py` para ver todas las consultas implementadas:

```bash
python consultas_mongodb.py
```

Este script ejecuta y muestra los resultados de:

1. **Consultas básicas CRUD** (Inserción, Selección, Actualización, Eliminación)
2. **Consultas con filtros y operadores** (Comparación, Lógicos, Arrays)
3. **Consultas de agregación** (Promedios, Sumas, Agrupaciones, Joins)

**Salida esperada:**

El script mostrará en consola todos los resultados de las consultas organizadas por categorías.

---

## 📁 Estructura del Proyecto

```
fase2-mongodb/
│
├── README.md                      # Este archivo
├── ESQUEMA_REDES_SOCIALES.md      # Documentación detallada del esquema
├── comandos_mongodb.py            # Script para crear BD e insertar datos
└── consultas_mongodb.py           # Script con todas las consultas
```

---

## 🔍 Consultas Implementadas

### 4.2.2 Consultas Básicas (CRUD)

#### Inserción
```python
nuevo_usuario = {
    "username": "pedro_sanchez",
    "email": "pedro.sanchez@email.com",
    "nombre_completo": "Pedro Sánchez",
    "fecha_registro": datetime.now(),
    "seguidores": 500,
    "siguiendo": 200,
    "ubicacion": {"ciudad": "Cartagena", "pais": "Colombia"}
}
resultado = usuarios.insert_one(nuevo_usuario)
```

#### Selección
```python
# Todos los usuarios
todos_usuarios = list(usuarios.find())

# Usuario específico
usuario = usuarios.find_one({"username": "juan_perez"})

# Con proyección (solo campos específicos)
usuarios = list(usuarios.find({}, {"username": 1, "email": 1, "seguidores": 1}))
```

#### Actualización
```python
# Actualizar un campo
usuarios.update_one(
    {"username": "juan_perez"},
    {"$set": {"seguidores": 1300}}
)

# Incrementar un valor
posts.update_one(
    {"username": "maria_garcia"},
    {"$inc": {"estadisticas.likes": 5}}
)
```

#### Eliminación
```python
# Soft delete (marcar como inactivo)
comentarios.update_one(
    {"username": "juan_perez", "activo": True},
    {"$set": {"activo": False}}
)
```

### 4.2.3 Consultas con Filtros y Operadores

#### Operadores de Comparación
```python
# Mayor que
usuarios.find({"seguidores": {"$gt": 1000}})

# Menor que
posts.find({"estadisticas.likes": {"$lt": 50}})

# Rango
usuarios.find({"seguidores": {"$gte": 800, "$lte": 1500}})

# Diferente
posts.find({"username": {"$ne": "juan_perez"}})
```

#### Operadores Lógicos
```python
# AND
posts.find({
    "$and": [
        {"estadisticas.likes": {"$gt": 40}},
        {"estadisticas.comentarios": {"$gt": 10}}
    ]
})

# OR
usuarios.find({
    "$or": [
        {"ubicacion.ciudad": "Bogotá"},
        {"ubicacion.ciudad": "Medellín"}
    ]
})
```

#### Operadores de Array
```python
# Buscar en array
posts.find({"hashtags": "mongodb"})

# Contiene cualquiera de los valores
posts.find({"hashtags": {"$in": ["programacion", "diseño"]}})

# Debe contener todos los valores
posts.find({"hashtags": {"$all": ["mongodb", "bigdata"]}})
```

### 4.2.4 Consultas de Agregación

#### Promedio
```python
pipeline = [
    {
        "$group": {
            "_id": None,
            "promedio_seguidores": {"$avg": "$seguidores"},
            "total_usuarios": {"$sum": 1}
        }
    }
]
resultado = list(usuarios.aggregate(pipeline))
```

#### Suma
```python
pipeline = [
    {
        "$group": {
            "_id": None,
            "total_likes": {"$sum": "$estadisticas.likes"},
            "total_comentarios": {"$sum": "$estadisticas.comentarios"}
        }
    }
]
resultado = list(posts.aggregate(pipeline))
```

#### Agrupación
```python
pipeline = [
    {
        "$group": {
            "_id": "$username",
            "total_posts": {"$sum": 1},
            "total_likes": {"$sum": "$estadisticas.likes"},
            "promedio_likes": {"$avg": "$estadisticas.likes"}
        }
    },
    {"$sort": {"total_likes": -1}}
]
resultado = list(posts.aggregate(pipeline))
```

#### Unwind (Descomponer Arrays)
```python
pipeline = [
    {"$unwind": "$hashtags"},
    {
        "$group": {
            "_id": "$hashtags",
            "total_apariciones": {"$sum": 1}
        }
    },
    {"$sort": {"total_apariciones": -1}}
]
resultado = list(posts.aggregate(pipeline))
```

#### Lookup (Join entre colecciones)
```python
pipeline = [
    {
        "$lookup": {
            "from": "usuarios",
            "localField": "usuario_id",
            "foreignField": "_id",
            "as": "usuario_info"
        }
    },
    {"$unwind": "$usuario_info"},
    {
        "$project": {
            "username": 1,
            "contenido": 1,
            "likes": "$estadisticas.likes",
            "ciudad_usuario": "$usuario_info.ubicacion.ciudad",
            "seguidores_usuario": "$usuario_info.seguidores"
        }
    }
]
resultado = list(posts.aggregate(pipeline))
```

---

## 📚 Documentación Adicional

Para más información sobre:

- **Esquema detallado**: Consulta [ESQUEMA_REDES_SOCIALES.md](ESQUEMA_REDES_SOCIALES.md)
- **Código de consultas**: Revisa el archivo `consultas_mongodb.py` con comentarios explicativos
- **Script de creación**: Revisa el archivo `comandos_mongodb.py` para entender la estructura de datos

---

## 🔐 Notas de Seguridad

⚠️ **Importante**: Para este ejercicio educativo, MongoDB se configuró **sin autenticación** para facilitar el desarrollo y las pruebas. En un entorno de producción, siempre se debe configurar autenticación con usuario y contraseña.

Para configurar autenticación en MongoDB:

1. Crear un usuario administrador
2. Habilitar autenticación en el archivo de configuración
3. Modificar la cadena de conexión en los scripts para incluir credenciales

---

## 👥 Autores

- ALBEIRO MANUEL BAENA TOVAR
- SERGIO ALEJANDRO ENRIQUE CABALLERO LEON
- CRISTIAN JOHAN GALVIS BERNAL
- JULIAN DARIO GONZALEZ TOLEDO
- WILLIAM ANDRES RINCON RODRIGUEZ

**Curso**: BigData - Universidad Nacional Abierta y a Distancia (UNAD)  
**Año**: 2025

---

## 📄 Licencia

Este proyecto es parte de una tarea académica y se proporciona únicamente con fines educativos.

---

## 🔗 Enlaces Útiles

- [Documentación oficial de MongoDB](https://www.mongodb.com/docs/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB University](https://university.mongodb.com/)
- [MongoDB Compass](https://www.mongodb.com/products/compass)

---

## 📝 Notas Finales

- Los scripts están comentados para facilitar la comprensión
- Se recomienda ejecutar primero `comandos_mongodb.py` y luego `consultas_mongodb.py`
- Para empezar desde cero, descomenta las líneas de limpieza en `comandos_mongodb.py`
- Los datos de prueba pueden expandirse para cumplir con el requisito de 100+ documentos

