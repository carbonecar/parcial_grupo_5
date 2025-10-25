### Creación de repositorio

 gh repo create parcial_grupo_5 --public --source=. --remote=origin

### Deploy automático
El deploy automático se hace al taguear y se genera mediante la api de render
    - Crear el tag
 ``` git tag -a v1.0.0 -m 'primer version```
 ``` git push origin v1.0.0 ```

Para deployar se agregan las credenciales en github como secret

- Agregar las secrets a github 
 - RENDER_API_KEY ``` gh secret set RENDER_API_KEY --body "tu_api_key_de_render" ```
 - RENDER_SERVICE_ID ``` gh secret set RENDER_SERVICE_ID --body "tu_service_id_de_render" ```
 
Observacion: Si el servicio esta bajo. Hacer un tag y deployar
### Ejecutar la aplicacion local
 fastapi dev main.py

### crear

 # Examen  1