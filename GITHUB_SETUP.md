# Conectar Alfred a un repositorio privado de GitHub

## Estado del entorno

| Herramienta | Estado |
|-------------|--------|
| Git 2.49    | Instalado |
| OpenSSH 9.9 | Instalado |
| gh CLI      | No instalado |
| Clave SSH   | No existe |

---

## Opción A — SSH (recomendada)

Es la forma más segura y no requiere guardar contraseñas.

### 1. Generar clave SSH

Abre PowerShell y ejecuta:

```powershell
ssh-keygen -t ed25519 -C "pablomerida03@gmail.com"
```

Cuando pregunte dónde guardarla, pulsa **Enter** para usar la ruta por defecto (`C:\Users\pablo\.ssh\id_ed25519`).

Puedes dejar la passphrase vacía o añadir una — ambas opciones funcionan.

### 2. Copiar la clave pública

```powershell
Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub" | Set-Clipboard
```

### 3. Añadirla a GitHub

1. Ve a **GitHub → Settings → SSH and GPG keys → New SSH key**
2. Dale un nombre (ej. `Alfred-Windows`)
3. Pega la clave en el campo *Key*
4. Guarda

### 4. Verificar la conexión

```powershell
ssh -T git@github.com
```

Respuesta esperada:
```
Hi <tu-usuario>! You've successfully authenticated, but GitHub does not provide shell access.
```

### 5. Clonar el repositorio

```powershell
git clone git@github.com:<usuario>/<repositorio>.git D:\Programas\Alfred\<nombre-carpeta>
```

---

## Opción B — Personal Access Token (PAT)

Más simple de configurar, pero menos seguro (el token es texto plano).

### 1. Crear el token

1. Ve a **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Haz clic en **Generate new token (classic)**
3. Selecciona el scope: `repo` (acceso completo a repos privados)
4. Copia el token generado — solo se muestra una vez

### 2. Clonar el repositorio

```powershell
git clone https://<usuario>:<TOKEN>@github.com/<usuario>/<repositorio>.git D:\Programas\Alfred\<nombre-carpeta>
```

### 3. Guardar el token en Alfred

Añade esta línea al archivo `.env` del proyecto:

```env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

---

## Recomendación

Usa **SSH**. Una vez configurado, no necesitas credenciales en cada operación y el token no queda expuesto en ningún archivo.

---

## Siguiente paso

Dime el URL del repositorio y ejecuto el clone directamente.
