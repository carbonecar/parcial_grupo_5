### Creación de repositorio

 gh repo create parcial_grupo_5 --public --source=. --remote=origin

### Deploy automático
El deploy automático se hace al taguear y se genera mediante la api de render
    - Crear el tag
 ``` git tag -a v1.0.0 -m 'primer version```
 ``` git push origin v1.0.0 ```
### Ejecutar la aplicacion local
 fastapi dev main.py

### crear

 # Examen  1