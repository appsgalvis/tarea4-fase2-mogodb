# Fase 2: MongoDB - Red Social

Este repositorio contiene la implementación de una base de datos MongoDB para gestionar datos de una red social, incluyendo usuarios, posts y comentarios. Este proyecto forma parte de la Tarea 4 sobre Almacenamiento y Consultas de Datos en BigData.

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación](#instalación)
4. [Diseño de la Base de Datos](#diseño-de-la-base-de-datos)
5. [Implementación en MongoDB](#implementación-en-mongodb)
6. [Consultas Implementadas](#consultas-implementadas)
7. [Documentación](#documentación)
8. [Estructura del Proyecto](#estructura-del-proyecto)

---

## 📝 Descripción del Proyecto

Para esta fase se ha seleccionado el caso de uso de almacenamiento de datos de redes sociales, específicamente para gestionar posts, comentarios y usuarios. Este caso de uso es ideal para MongoDB debido a la naturaleza semiestructurada de los datos, la necesidad de escalabilidad horizontal y la flexibilidad para agregar nuevos campos sin migraciones costosas.

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

Para la implementación de este proyecto, se descargó e instaló MongoDB Community Server versión 8.2.1 desde el sitio oficial de MongoDB. La instalación se realizó en Windows utilizando el instalador MSI proporcionado. Para este ejercicio, no se configuró autenticación con usuario y contraseña, permitiendo conexiones locales sin credenciales para facilitar el desarrollo y las pruebas.

1. Descarga MongoDB Community Server desde el [sitio oficial de MongoDB](https://www.mongodb.com/try/download/community)

![Descarga de MongoDB](Imagenes/descargando%20mogo.png)

*Figura 1. Descarga de MongoDB Community Server 8.2.1 para Windows desde el sitio oficial de MongoDB*

2. Ejecuta el instalador MSI para Windows

![Instalación de MongoDB](Imagenes/instalador%20terminando%20la%20intalcion.png)

*Figura 2. Proceso de instalación de MongoDB 8.2.1 en Windows, mostrando la copia de archivos durante la instalación*

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

A continuación se presenta el diseño del esquema de la base de datos MongoDB para el caso de uso seleccionado:

![Esquema de la Base de Datos](Imagenes/red_social_esquema_compass.png)

*Figura 3. Esquema de la base de datos MongoDB para almacenamiento de datos de redes sociales (generado con MongoDB Compass)*

El esquema diseñado contempla tres colecciones principales: usuarios, posts y comentarios. La colección de usuarios almacena la información básica de los usuarios, incluyendo datos de perfil, ubicación y estadísticas de seguidores. La colección de posts contiene las publicaciones de los usuarios con sus respectivas estadísticas, hashtags, reacciones y comentarios embebidos para acceso rápido. La colección de comentarios almacena los comentarios de los posts, permitiendo respuestas anidadas y manteniendo referencias tanto al post como al usuario que comentó.

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

## 🚀 Implementación en MongoDB

Para crear la base de datos y cargar los datos de prueba en MongoDB, se utilizó el método de importación desde archivos JSON. Se generaron archivos JSON con al menos 100 documentos distribuidos en las tres colecciones (usuarios, posts y comentarios) y se importaron utilizando MongoDB Compass o la herramienta mongoimport.

### Paso 1: Generar los archivos JSON de datos

Primero, ejecutamos nuestro script de Python (`generar_datos_json.py`) para generar los archivos JSON con los datos de prueba. El script crea tres archivos: `datos_usuarios.json`, `datos_posts.json` y `datos_comentarios.json`.

#### Código Python: `generar_datos_json.py`

```python
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
```

**Ejecutar el script:**

```bash
python generar_datos_json.py
```

**Salida esperada:**

```
Generados 40 usuarios, 40 posts y 30 comentarios
Total: 110 documentos
Archivos creados: datos_usuarios.json, datos_posts.json, datos_comentarios.json
```

![Carpeta con script y archivos JSON](Imagenes/carpeta%20con%20script%20y%20archivos%20json%20generados.png)

*Figura 4. Carpeta con el script generar_datos_json.py y los archivos JSON generados (datos_usuarios.json, datos_posts.json, datos_comentarios.json)*

### Paso 2: Crear la base de datos en MongoDB Compass

Abre MongoDB Compass y conéctate a tu instancia local (mongodb://localhost:27017). Luego crea o selecciona la base de datos 'red_social' desde el panel izquierdo.

![Creando base de datos red_social](Imagenes/creando%20base%20red_social%20compass.png)

*Figura 5. Creación de la base de datos red_social en MongoDB Compass*

**Comando de consola:**

```bash
red_social> use red_social
```

### Paso 3: Importar los datos JSON

Tienes dos opciones para importar los datos:

#### Opción 1: Importar datos usando MongoDB Compass

Para importar los datos directamente desde MongoDB Compass, sigue estos pasos:

**Archivos JSON disponibles para importar:**

![Archivos JSON disponibles](Imagenes/carpeta%20con%20script%20y%20archivos%20json%20generados.png)

*Figura 6. Archivos JSON disponibles para importar: datos_usuarios.json, datos_posts.json y datos_comentarios.json*

1. Abre MongoDB Compass y conéctate a tu instancia local (mongodb://localhost:27017).
2. Crea o selecciona la base de datos 'red_social' desde el panel izquierdo.
3. Para cada colección (usuarios, posts, comentarios):
   - Haz clic en 'Add Data' → 'Import File'
   - Selecciona el archivo JSON correspondiente (datos_usuarios.json, datos_posts.json o datos_comentarios.json)
   - Asegúrate de que el formato esté en 'JSON' y haz clic en 'Import'

![Importar JSON en MongoDB Compass](Imagenes/importar%20json%20a%20mongo%20compass.png)

*Figura 7. Proceso de importación de archivos JSON en MongoDB Compass usando la opción 'Add Data' → 'Import File'*

![Vista de colecciones importadas](Imagenes/vista%20de%20coleciones%20ya%20importadas%20en%20mongo%20compass.png)

*Figura 8. Vista de las colecciones usuarios, posts y comentarios ya importadas en MongoDB Compass*

#### Opción 2: Importar datos usando mongoimport desde la consola

Alternativamente, puedes importar los datos usando la herramienta mongoimport desde la línea de comandos. Los archivos JSON que debes importar son los siguientes:

![Archivos JSON para mongoimport](Imagenes/carpeta%20con%20script%20y%20archivos%20json%20generados.png)

*Figura 9. Archivos JSON disponibles para importar con mongoimport: datos_usuarios.json, datos_posts.json y datos_comentarios.json*

Ejecuta los siguientes comandos desde la terminal para importar cada archivo JSON a su colección correspondiente:

```bash
red_social> mongoimport --db red_social --collection usuarios --file "fase2-mongodb/Generar Datos Iniciales/datos_usuarios.json" --jsonArray

red_social> mongoimport --db red_social --collection posts --file "fase2-mongodb/Generar Datos Iniciales/datos_posts.json" --jsonArray

red_social> mongoimport --db red_social --collection comentarios --file "fase2-mongodb/Generar Datos Iniciales/datos_comentarios.json" --jsonArray
```

### Paso 4: Verificar la inserción de datos

Una vez importados los datos, puedes verificar que se hayan insertado correctamente ejecutando los siguientes comandos:

```bash
red_social> print("\n=== RESUMEN DE DATOS INSERTADOS ===")
red_social> print("Usuarios: " + db.usuarios.countDocuments({}))
red_social> print("Posts: " + db.posts.countDocuments({}))
red_social> print("Comentarios: " + db.comentarios.countDocuments({}))
red_social> print("Total: " + (db.usuarios.countDocuments({}) + db.posts.countDocuments({}) + db.comentarios.countDocuments({})) + " documentos")
```

---

## 🔍 Consultas Implementadas

A continuación se presentan ejemplos de las operaciones CRUD (Create, Read, Update, Delete) básicas y consultas avanzadas en MongoDB utilizando comandos de consola:

### 4.2.2 Consultas básicas (inserción, selección, actualización y eliminación)

#### INSERCIÓN:

```javascript
red_social> db.usuarios.insertOne({
    "username": "pedro_sanchez",
    "email": "pedro.sanchez@email.com",
    "nombre_completo": "Pedro Sánchez",
    "fecha_registro": new Date(),
    "seguidores": 500,
    "siguiendo": 200,
    "ubicacion": {"ciudad": "Cartagena", "pais": "Colombia"}
})
```

#### SELECCIÓN:

```javascript
red_social> db.usuarios.find()

red_social> db.usuarios.findOne({"username": "juan_perez"})

red_social> db.usuarios.find({}, {"username": 1, "email": 1, "seguidores": 1})
```

#### ACTUALIZACIÓN:

```javascript
red_social> db.usuarios.updateOne(
    {"username": "juan_perez"},
    {"$set": {"seguidores": 1300}}
)

red_social> db.posts.updateOne(
    {"username": "juan_perez"},
    {"$set": {
        "estadisticas.likes": 50,
        "fecha_actualizacion": new Date()
    }}
)

red_social> db.posts.updateOne(
    {"username": "maria_garcia"},
    {"$inc": {"estadisticas.likes": 5}}
)
```

#### ELIMINACIÓN:

```javascript
red_social> db.comentarios.updateOne(
    {"username": "juan_perez", "activo": true},
    {"$set": {"activo": false}}
)

red_social> db.comentarios.deleteOne({"username": "test_user"})
```

### 4.2.3 Consultas con filtros y operadores

MongoDB ofrece una amplia variedad de operadores para realizar consultas más complejas y específicas. A continuación se muestran ejemplos de los principales operadores:

#### OPERADORES DE COMPARACIÓN:

```javascript
red_social> db.usuarios.find({"seguidores": {$gt: 1000}})

red_social> db.posts.find({"estadisticas.likes": {$lt: 50}})

red_social> db.usuarios.find({"seguidores": {$gte: 800, $lte: 1500}})

red_social> db.posts.find({"username": {$ne: "juan_perez"}})
```

#### OPERADORES LÓGICOS:

```javascript
red_social> db.posts.find({
    $and: [
        {"estadisticas.likes": {$gt: 40}},
        {"estadisticas.comentarios": {$gt: 10}}
    ]
})

red_social> db.usuarios.find({
    $or: [
        {"ubicacion.ciudad": "Bogotá"},
        {"ubicacion.ciudad": "Medellín"}
    ]
})

red_social> db.posts.find({"username": {$not: {$eq: "juan_perez"}}})
```

#### OPERADORES DE ARRAY:

```javascript
red_social> db.posts.find({"hashtags": {$in: ["programacion", "diseño"]}})

red_social> db.posts.find({"hashtags": {$all: ["mongodb", "bigdata"]}})

red_social> db.posts.find({"hashtags": "mongodb"})

red_social> db.comentarios.find({"respuestas": {$size: 2}})
```

#### ORDENAMIENTO Y LÍMITES:

```javascript
red_social> db.usuarios.find().sort({"seguidores": -1})

red_social> db.posts.find().limit(5)

red_social> db.usuarios.find().sort({"seguidores": -1}).limit(3)

red_social> db.posts.find().skip(10).limit(5)
```

### 4.2.4 Consultas de agregación para calcular estadísticas

Las consultas de agregación permiten procesar documentos y realizar cálculos estadísticos complejos. MongoDB utiliza pipelines de agregación compuestos por diferentes etapas:

#### PROMEDIO ($avg):

```javascript
red_social> db.usuarios.aggregate([
    {
        $group: {
            _id: null,
            promedio_seguidores: {$avg: "$seguidores"},
            total_usuarios: {$sum: 1}
        }
    }
])
```

#### SUMA ($sum):

```javascript
red_social> db.posts.aggregate([
    {
        $group: {
            _id: null,
            total_likes: {$sum: "$estadisticas.likes"},
            total_comentarios: {$sum: "$estadisticas.comentarios"},
            total_compartidos: {$sum: "$estadisticas.compartidos"}
        }
    }
])
```

#### AGRUPACIÓN ($group):

```javascript
red_social> db.posts.aggregate([
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
])
```

#### FILTROS EN PIPELINE ($match):

```javascript
red_social> db.posts.aggregate([
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
])
```

---

## 📚 Documentación

### 4.3.1 Documentación del diseño de la base de datos

La base de datos MongoDB diseñada para este proyecto se denomina 'red_social' y está orientada al almacenamiento de datos de redes sociales, específicamente para gestionar posts, comentarios y usuarios. Esta selección se justifica por la naturaleza semiestructurada de los datos, la necesidad de escalabilidad horizontal y la flexibilidad para agregar nuevos campos sin migraciones costosas.

La base de datos está compuesta por tres colecciones principales: usuarios, posts y comentarios. La colección de usuarios almacena información básica de los usuarios, incluyendo datos de perfil (username, email, nombre_completo), estadísticas de seguidores y siguiendo, ubicación geográfica (ciudad, país) y preferencias. Los campos principales incluyen identificadores únicos como username y email, ambos indexados para garantizar unicidad y optimizar búsquedas.

La colección de posts contiene las publicaciones de los usuarios con sus respectivas estadísticas (likes, comentarios, compartidos, visualizaciones), hashtags, reacciones y comentarios embebidos para acceso rápido. Esta estructura permite almacenar información relacionada directamente en el documento, reduciendo la necesidad de múltiples consultas. Los posts incluyen referencias al usuario mediante usuario_id y también almacenan el username de forma denormalizada para optimizar consultas frecuentes.

La colección de comentarios almacena los comentarios de los posts, permitiendo respuestas anidadas y manteniendo referencias tanto al post como al usuario que comentó. Esta estructura soporta threads de comentarios mediante el campo comentario_padre_id y respuestas embebidas para threads cortos, optimizando el acceso a conversaciones recientes.

Se implementó una estrategia de denormalización selectiva, almacenando username en posts y comentarios para evitar joins frecuentes, y se utilizó un enfoque híbrido de embebido y referencias: comentarios recientes y reacciones se almacenan embebidos en posts para acceso rápido, mientras que comentarios antiguos se mantienen en una colección separada para escalabilidad. Los índices creados optimizan consultas frecuentes: índices únicos en username y email de usuarios, índices en usuario_id y fecha_publicacion de posts, índices de texto para búsquedas en contenido y hashtags, e índices en post_id y usuario_id de comentarios para acelerar las consultas de relaciones.

### 4.3.2 Explicación del código de las consultas

Las consultas implementadas se organizan en tres categorías principales: consultas básicas CRUD, consultas con filtros y operadores, y consultas de agregación. Todas las consultas fueron implementadas utilizando Python con el driver PyMongo, conectándose a MongoDB mediante MongoClient('mongodb://localhost:27017/').

Las consultas básicas CRUD incluyen operaciones de inserción (insert_one, insert_many), selección (find, find_one), actualización (update_one con operadores $set e $inc) y eliminación (delete_one, o soft delete mediante update_one estableciendo activo: False). Por ejemplo, la inserción de un nuevo usuario utiliza insert_one() con un diccionario Python que se convierte automáticamente a BSON, mientras que las actualizaciones utilizan el operador $set para modificar campos específicos o $inc para incrementar valores numéricos.

Las consultas con filtros utilizan operadores de comparación ($gt, $lt, $gte, $lte, $ne), operadores lógicos ($and, $or, $not) y operadores de array ($in, $all). Un ejemplo es la consulta de usuarios con más de 1000 seguidores: usuarios.find({"seguidores": {"$gt": 1000}}), donde $gt filtra documentos donde el campo seguidores es mayor que 1000. Los operadores de array permiten buscar documentos que contengan elementos específicos en arrays, como posts.find({"hashtags": "mongodb"}) para encontrar posts con ese hashtag, o posts.find({"hashtags": {"$in": ["programacion", "diseno"]}}) para encontrar posts con cualquiera de esos hashtags.

Las consultas de agregación utilizan pipelines compuestos por múltiples etapas. La etapa $match filtra documentos antes del procesamiento, similar a WHERE en SQL. La etapa $group agrupa documentos y calcula agregaciones usando operadores como $sum (suma), $avg (promedio), $max (máximo), $min (mínimo) y $count (contar). Por ejemplo, para calcular el promedio de seguidores se utiliza un pipeline con $group que agrupa todos los documentos (_id: None) y calcula {"$avg": "$seguidores"}. La etapa $unwind descompone arrays, permitiendo contar hashtags individuales. La etapa $lookup realiza joins entre colecciones, similar a JOIN en SQL, permitiendo combinar datos de posts con información de usuarios. La etapa $project selecciona y transforma campos, y puede incluir cálculos como el ratio de engagement calculado como (likes + comentarios) / visualizaciones.

### 4.3.3 Análisis de resultados de las consultas de agregación

Las consultas de agregación implementadas proporcionan insights valiosos sobre los datos de la red social. La consulta de promedio de seguidores revela la distribución de popularidad entre usuarios, permitiendo identificar si hay una concentración de seguidores en pocos usuarios o una distribución más equitativa. El promedio de likes por post indica el nivel de engagement general de la plataforma, mientras que el total de likes, comentarios y compartidos muestra la actividad agregada de la comunidad.

La agregación que agrupa posts por usuario y calcula estadísticas (total_posts, total_likes, total_comentarios, promedio_likes) permite identificar a los usuarios más activos y con mayor engagement. Los resultados ordenados por total_likes descendente muestran una jerarquía de influencia, donde usuarios con mayor cantidad de likes totales tienen mayor impacto en la plataforma. Esta información es crucial para identificar creadores de contenido destacados y entender los patrones de interacción.

La consulta de promedio de likes filtrada para posts con más de 40 likes permite analizar el rendimiento de contenido de alta calidad, comparándolo con el promedio general. Si el promedio filtrado es significativamente mayor, indica que existe una brecha entre contenido popular y contenido promedio, sugiriendo que algunos posts generan mucho más engagement que otros. La agregación que cuenta hashtags mediante $unwind revela los temas más populares en la plataforma, información valiosa para estrategias de contenido y tendencias de la comunidad.

En conjunto, estas consultas de agregación demuestran la capacidad de MongoDB para realizar análisis complejos sobre datos no relacionales, proporcionando insights que serían difíciles de obtener con consultas simples. Los pipelines de agregación permiten transformar y analizar datos en una sola operación, optimizando el rendimiento al procesar los datos directamente en la base de datos en lugar de transferirlos a la aplicación para procesamiento posterior. Los resultados obtenidos pueden utilizarse para tomar decisiones informadas sobre estrategias de contenido, identificar tendencias y optimizar la experiencia del usuario en la plataforma.

---

## 📁 Estructura del Proyecto

```
fase2-mongodb/
│
├── README.md                           # Este archivo
├── ESQUEMA_REDES_SOCIALES.md           # Documentación detallada del esquema
│
├── [Python - PyMongo]
├── comandos_mongodb.py                 # Script Python para crear BD e insertar datos (6 docs)
├── consultas_mongodb.py                # Script Python con todas las consultas
├── generar_datos_json.py               # Script para generar archivos JSON (110 docs)
├── importar_datos_json.py              # Script Python para importar desde JSON (110 docs)
├── requirements.txt                    # Dependencias Python
│
├── [Consola MongoDB - mongosh]
├── comandos_mongodb_consola.js         # Script de consola para crear BD e insertar datos (6 docs)
├── consultas_mongodb_consola.js        # Script de consola con todas las consultas
├── importar_datos_json.js              # Script de consola para importar desde JSON (110 docs)
│
├── [Generar Datos Iniciales]
├── generar_datos_json.py               # Script para generar archivos JSON (110 docs)
├── datos_usuarios.json                 # 40 usuarios en formato JSON
├── datos_posts.json                     # 40 posts en formato JSON
├── datos_comentarios.json              # 30 comentarios en formato JSON
│
├── [Imagenes]
├── descargando mogo.png                # Imagen de descarga de MongoDB
├── instalador terminando la intalcion.png # Imagen de instalación
├── carpeta con script y archivos json generados.png # Carpeta con archivos
├── creando base red_social compass.png # Creación de base de datos
├── importar json a mongo compass.png   # Importación en Compass
├── vista de coleciones ya importadas en mongo compass.png # Vista de colecciones
├── red_social_esquema_compass.png      # Esquema de BD (MongoDB Compass)
└── esquema_base_datos_red_social.png   # Diagrama del esquema
```

---

## 🔐 Notas de Seguridad

⚠️ **Importante**: Para este ejercicio educativo, MongoDB se configuró **sin autenticación** para facilitar el desarrollo y las pruebas. En un entorno de producción, siempre se debe configurar autenticación con usuario y contraseña.

Para configurar autenticación en MongoDB:

1. Crear un usuario administrador
2. Habilitar autenticación en el archivo de configuración
3. Modificar la cadena de conexión en los scripts para incluir credenciales

---

## 👤 Autor

**CRISTIAN JOHAN GALVIS BERNAL**

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

- **Dos opciones disponibles**: Puedes usar Python (PyMongo) o Consola MongoDB (mongosh)
- Los scripts están comentados para facilitar la comprensión
- **Python**: Se recomienda ejecutar primero `generar_datos_json.py` y luego importar los datos
- **Consola**: Se recomienda ejecutar primero `comandos_mongodb_consola.js` y luego `consultas_mongodb_consola.js`
- Para empezar desde cero, descomenta las líneas de limpieza en los scripts correspondientes
- Los datos de prueba generan 110 documentos (40 usuarios, 40 posts, 30 comentarios)
- Ambos métodos (Python y consola) producen los mismos resultados
