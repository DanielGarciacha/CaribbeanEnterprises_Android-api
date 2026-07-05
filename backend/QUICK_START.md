# 🚀 Guía Rápida de Inicio

## ⚡ Inicio Rápido (5 minutos)

### 1. Asegúrate de que XAMPP esté corriendo

- Abre XAMPP Control Panel
- Inicia **MySQL**

### 2. Crea la base de datos

Opción A - Desde phpMyAdmin:

1. Abre http://localhost/phpmyadmin
2. Haz clic en "Nueva"
3. Nombre: `ctp_db`
4. Cotejamiento: `utf8mb4_unicode_ci`
5. Haz clic en "Crear"

Opción B - Desde consola MySQL:

```sql
CREATE DATABASE ctp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Copia el archivo de configuración

```bash
copy .env.example .env
```

### 4. Instala las dependencias (solo primera vez)

```bash
pip install -r requirements.txt
```

### 5. Inicializa la base de datos

**Doble clic en:** `init_database.bat`

O desde terminal:

```bash
python init_db.py
```

### 6. Inicia el servidor

**Doble clic en:** `start_server.bat`

O desde terminal:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Prueba la API

Abre en tu navegador:

- **Swagger UI**: http://localhost:8000/docs
- **API Root**: http://localhost:8000

## 🧪 Probar Login

### Desde Swagger UI (http://localhost:8000/docs):

1. Expande `POST /auth/login`
2. Haz clic en "Try it out"
3. Ingresa:
   - username: `admin`
   - password: `admin123`
4. Haz clic en "Execute"
5. ✅ Deberías recibir un token y los datos del usuario

### Desde curl:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### Respuesta esperada:

```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@ctp.com",
    "role": "admin",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

## 🔑 Usuarios de Prueba

| Usuario | Contraseña | Rol    |
| ------- | ---------- | ------ |
| admin   | admin123   | admin  |
| usuario | usuario123 | normal |

## 📱 Conectar con Android

Edita `RetrofitClient.kt`:

```kotlin
// Si usas emulador
private const val BASE_URL = "http://10.0.2.2:8000/"

// Si usas dispositivo físico, obtén tu IP con: ipconfig
private const val BASE_URL = "http://TU_IP:8000/"
```

## ❓ Solución de Problemas

### ❌ "Access denied for user 'root'"

→ Verifica que MySQL esté corriendo en XAMPP

### ❌ "Unknown database 'ctp_db'"

→ Crea la base de datos (paso 2)

### ❌ "ModuleNotFoundError"

→ Instala dependencias: `pip install -r requirements.txt`

### ❌ "Address already in use"

→ El puerto 8000 está ocupado, cambia en `.env`: `PORT=8001`

---

Para más información, lee el [README.md](README.md) completo.
