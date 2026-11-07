# GameJam API

API REST para la app Android **GameJam · Bitácora de videojuegos** (Proyecto Unidad 3). Hecha con **FastAPI + SQLModel (SQLite)**, autenticación con **JWT Bearer** y contraseñas con **bcrypt**.

Cada usuario sólo ve y modifica **sus propios** juegos.

## Requisitos
- Python 3.10 o superior

## Instalación y ejecución (Windows, PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- Documentación interactiva: http://localhost:8000/docs
- Desde el emulador de Android: `http://10.0.2.2:8000/`
- La base de datos `gamejam.db` se crea sola al iniciar.

## Variables de entorno (opcionales)
| Variable | Valor por defecto | Uso |
|---|---|---|
| `GAMEJAM_SECRET_KEY` | clave de desarrollo | Firma de los tokens |
| `GAMEJAM_TOKEN_MINUTES` | `10080` (7 días) | Duración del token |
| `GAMEJAM_DATABASE_URL` | `sqlite:///./gamejam.db` | Base de datos |

## Contrato
| Método | Ruta | Body | Respuesta |
|---|---|---|---|
| POST | `/register` | `{ name, email, password }` | 201 `{ accessToken, user: { id, name, email } }` |
| POST | `/login` | `{ email, password }` | 200 `{ accessToken, user }` |
| GET | `/games` | — | 200 `[ Game ]` |
| GET | `/games/{id}` | — | 200 `Game` |
| POST | `/games` | `Game` sin `id` | 201 `Game` |
| PUT | `/games/{id}` | `Game` | 200 `Game` |
| DELETE | `/games/{id}` | — | 204 vacío |

Las rutas `/games` requieren `Authorization: Bearer <token>`.

```json
{ "id": 1, "title": "Celeste", "platform": "Switch", "hoursPlayed": 12, "rating": 9, "startDate": "2026-10-15", "completed": false }
```

## Validaciones y errores
| Código | Cuándo |
|---|---|
| 401 | Token ausente, inválido o expirado; credenciales incorrectas en `/login` |
| 404 | El juego no existe o pertenece a otro usuario |
| 409 | El correo ya está registrado |
| 422 | Datos inválidos: correo con formato incorrecto, contraseña de menos de 8 caracteres, `title` vacío o mayor a 60, `platform` vacía, `hoursPlayed` < 0, `rating` fuera de 1–10, `startDate` futura |

Los errores responden `{ "detail": ... }`.
