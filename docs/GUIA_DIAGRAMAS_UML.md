# Guía de Diagramas UML - Sistema de Pagos

Este documento proporciona una guía completa de los diagramas UML generados para el proyecto de Sistema de Gestión de Pagos.

## 📋 Diagramas Generados

Se han generado 8 diagramas UML en formato PlantUML (.puml) para visualizar diferentes aspectos de la arquitectura del proyecto:

### 1. **Diagrama de Clases** (`diagrama_clases.puml`)
**Propósito:** Visualizar todas las clases, interfaces y sus relaciones.

**Contenido:**
- Clases del dominio (PaymentStrategy y sus implementaciones)
- Modelos (Payment, PaymentConstants)
- Servicios de aplicación (PaymentsService)
- Factory (StrategyFactory)
- DTOs (PaymentRequest, PaymentMethod)
- Repositorio (PaymentRepository e implementación FilePaymentRepository)
- Excepciones de negocio

**Patrones mostrados:**
- Strategy Pattern (PaymentStrategy)
- Factory Pattern (StrategyFactory)
- Repository Pattern (PaymentRepository)
- DTO Pattern

**Caso de uso:**
- Entender la estructura completa del sistema
- Identificar relaciones entre clases
- Ver métodos y atributos principales

---

### 2. **Diagrama de Arquitectura** (`diagrama_arquitectura.puml`)
**Propósito:** Mostrar la arquitectura hexagonal/en capas del proyecto.

**Contenido:**
- **Capa API:** FastAPI, PaymentRoutes, Dependency Injection
- **Capa Application:** PaymentsService, StrategyFactory, DTOs
- **Capa Domain:** PaymentStrategy y sus implementaciones, Payment, Constants
- **Puertos:** PaymentRepository (interface)
- **Adaptadores/Infraestructura:** FilePaymentRepository, data.json
- **Excepciones:** PaymentAlreadyExistsError, PaymentNotFoundError, PaymentValidationError

**Flujo:**
Cliente → API → Application → Domain → Ports → Infra → Storage

**Caso de uso:**
- Entender la organización en capas
- Ver cómo interactúan los componentes
- Visualizar inversión de control (Puertos y Adaptadores)

---

### 3. **Diagrama de Componentes** (`diagrama_componentes.puml`)
**Propósito:** Mostrar componentes del sistema y sus dependencias.

**Contenido:**
- Cliente HTTP
- FastAPI Server + Uvicorn
- PaymentController (rutas)
- PaymentsService
- StrategyFactory
- PaymentStrategy e implementaciones
- PaymentRepository e implementación
- Modelos de dominio
- Persistencia JSON
- Validación con Pydantic

**Caso de uso:**
- Entender qué componentes existen
- Ver cómo se conectan
- Identificar dependencias tecnológicas

---

### 4. **Diagrama de Secuencia - Flujo de Pago** (`diagrama_secuencia_pago.puml`)
**Propósito:** Mostrar el flujo paso a paso de procesar un pago.

**Contenido:**

#### Caso 1: Procesar Pago (pay_payment)
1. Cliente hace POST a `/payments/{id}/pay`
2. PaymentRoutes delega en PaymentsService
3. Servicio obtiene datos del repositorio
4. Valida existencia del pago
5. Valida transición de estado (REGISTRADO → PAGADO)
6. Factory proporciona Strategy apropiada
7. Strategy valida reglas de negocio
   - **Si éxito:** estado → PAGADO
   - **Si falla:** estado → FALLIDO
8. Repositorio persiste cambios
9. Devuelve respuesta HTTP (200 o 422)

#### Caso 2: Revertir Pago (revert_payment)
1. Cliente hace POST a `/payments/{id}/revert`
2. Valida que estado sea FALLIDO
3. Transición FALLIDO → REGISTRADO
4. Persiste cambios
5. Devuelve respuesta HTTP 200

**Caso de uso:**
- Entender el flujo de negocio
- Depuración de problemas
- Documentación de procesos

---

### 5. **Diagrama de Paquetes** (`diagrama_paquetes.puml`)
**Propósito:** Mostrar la estructura de directorios y dependencias entre módulos.

**Contenido:**
- Estructura de directorios del proyecto
- Dependencias entre paquetes
- Archivos clave en cada paquete
- Dependencias externas (config, requirements.txt)
- CI/CD (workflows de GitHub)

**Paquetes principales:**
- `app/api` → rutas HTTP
- `app/application` → servicios y DTOs
- `app/domain` → lógica de negocio
- `app/ports` → interfaces
- `app/infra` → adaptadores
- `tests/` → suite de pruebas

**Caso de uso:**
- Entender la estructura del proyecto
- Navegar entre módulos
- Ver dependencias externas

---

### 6. **Diagrama de Estados** (`diagrama_estados.puml`)
**Propósito:** Mostrar los estados posibles de un pago y transiciones.

**Contenido:**

Estados:
- **REGISTRADO** (estado inicial)
  - Estado: Pago no procesado, listo para procesar
  - Transiciones:
    - → PAGADO (pay_payment exitoso)
    - → FALLIDO (pay_payment fallido)

- **PAGADO** (estado terminal)
  - Estado: Pago completado exitosamente
  - Transiciones: Ninguna (fin del ciclo de vida)

- **FALLIDO** (estado reversible)
  - Estado: Pago rechazado por validación
  - Transiciones:
    - → REGISTRADO (revert_payment)

**Validaciones:**
- Transiciones válidas entre estados
- Solo se puede revertir desde FALLIDO
- PAGADO es terminal

**Caso de uso:**
- Entender máquina de estados
- Validar flujos permitidos
- Documentación de negocio

---

### 7. **Diagrama de Despliegue** (`diagrama_despliegue.puml`)
**Propósito:** Mostrar cómo el sistema se despliega en diferentes ambientes.

**Contenido:**

**Ambientes:**
1. **Estación Local del Desarrollador**
   - Code Editor (VSCode)
   - Python 3.x
   - Git Repository local

2. **GitHub Repository**
   - Source Code
   - CI/CD Workflows (GitHub Actions)

3. **Servidor de Testing**
   - Pytest
   - Coverage Analyzer
   - Pylint Linter

4. **Servidor Render.com (Producción)**
   - FastAPI App
   - Uvicorn ASGI
   - Persistencia JSON

5. **Cliente**
   - Navegador / API Client

**Flujo CI/CD:**
- Developer → git commit/push
- GitHub → trigger workflows
- Testing → run tests & lint
- If green → deploy to Render.com
- If red → pipeline fails

**Caso de uso:**
- Entender pipeline de despliegue
- Ver ambientes de ejecución
- Documentar proceso de CI/CD

---

### 8. **Diagrama de Patrones de Diseño** (`diagrama_patrones.puml`)
**Propósito:** Explicar y mostrar los patrones de diseño utilizados.

**Patrones implementados:**

1. **Strategy Pattern**
   - Ubicación: `app/domain/`
   - Interfaz: `PaymentStrategy`
   - Implementaciones: `CreditCardPaymentStrategy`, `PayPalPaymentStrategy`
   - Beneficio: Desacoplar lógica de pago, facilita agregar nuevas estrategias

2. **Factory Pattern**
   - Ubicación: `app/application/strategy_factory.py`
   - Propósito: Crear instancias de Strategy sin especificar clase concreta
   - Método: `get_strategy(payment_method)`

3. **Repository Pattern**
   - Ubicación: `app/ports/` y `app/infra/`
   - Interfaz: `PaymentRepository`
   - Implementación: `FilePaymentRepository`
   - Beneficio: Abstrae persistencia, facilita testing

4. **Dependency Injection**
   - Ubicación: `app/api/payment_routes.py`
   - Mecanismo: FastAPI `Depends()`
   - Función: `get_payment_service()`

5. **Service Layer Pattern**
   - Ubicación: `app/application/payments_service.py`
   - Propósito: Encapsular lógica de negocio y orquestar operaciones

6. **DTO Pattern**
   - Ubicación: `app/application/dto/`
   - DTOs: `PaymentRequest`, `PaymentMethod`
   - Beneficio: Validación con Pydantic, transferencia de datos entre capas

7. **Layered Architecture**
   - API Layer → Application Layer → Domain Layer → Infrastructure Layer

8. **Hexagonal Architecture**
   - Core (Domain) → Ports → Adapters (Infra)

**Caso de uso:**
- Documentar patrones utilizados
- Enseñanza de arquitectura
- Justificar decisiones de diseño

---

## 🎯 Cómo Visualizar los Diagramas

### Opción 1: PlantUML Online
1. Ir a: https://www.plantuml.com/plantuml/uml/
2. Copiar contenido del archivo .puml
3. Pegar en el editor
4. El diagrama se genera automáticamente

### Opción 2: Extensión VSCode
1. Instalar extensión: "PlantUML" (jebbs.plantuml)
2. Abrir archivo .puml
3. Ejecutar comando: `PlantUML: Preview Current Diagram`
4. Ver diagrama en panel lateral

### Opción 3: Compilar a PNG/SVG
```bash
# Instalar plantUML (requiere Java)
npm install -g plantuml-pipe

# O si tienes instalado graphviz:
plantuml diagrama_clases.puml -o ../output -Tpng
```

---

## 🖼️ Diagramas PNG Generados

Los diagramas han sido compilados a formato PNG y se encuentran disponibles en la carpeta `out/docs/`. Cada diagrama tiene su propia subcarpeta con la imagen renderizada:

### Acceso Directo a los PNG

| Diagrama | Archivo PNG | Ruta |
|----------|-------------|------|
| **Diagrama de Clases** | `Diagrama_de_Clases_Sistema_de_Pagos.png` | `out/docs/diagrama_clases/` |
| **Diagrama de Arquitectura** | `Diagrama_Arquitectura_Hexagonal.png` | `out/docs/diagrama_arquitectura/` |
| **Diagrama de Componentes** | `Diagrama_Componentes_Pagos.png` | `out/docs/diagrama_componentes/` |
| **Diagrama de Secuencia** | `Diagrama_Secuencia_Pago.png` | `out/docs/diagrama_secuencia_pago/` |
| **Diagrama de Paquetes** | `Diagrama_Paquetes_Proyecto.png` | `out/docs/diagrama_paquetes/` |
| **Diagrama de Estados** | `Diagrama_Estados_Pago.png` | `out/docs/diagrama_estados/` |

### Cómo Usar los PNG

1. **Visualización rápida:**
   - Navega a la carpeta correspondiente en `out/docs/`
   - Abre el archivo PNG en tu visor de imágenes favorito

2. **Incluir en documentación:**
   ```markdown
   ![Diagrama de Clases](out/docs/diagrama_clases/Diagrama_de_Clases_Sistema_de_Pagos.png)
   ```

3. **Presentaciones:**
   - Descarga los PNG de `out/docs/`
   - Insértalos en PowerPoint, Google Slides o Keynote
   - Los PNG están optimizados para presentaciones

4. **Repositorio:**
   - Los PNG están versionados en el repositorio
   - Aparecen automáticamente en GitHub al visualizar el directorio
   - Útil para compartir en PRs o issues

### Estructura de Carpetas

```
out/docs/
├── diagrama_arquitectura/
│   └── Diagrama_Arquitectura_Hexagonal.png
├── diagrama_clases/
│   └── Diagrama_de_Clases_Sistema_de_Pagos.png
├── diagrama_componentes/
│   └── Diagrama_Componentes_Pagos.png
├── diagrama_despliegue/
│   └── Diagrama_Despliegue.png
├── diagrama_estados/
│   └── Diagrama_Estados_Pago.png
├── diagrama_paquetes/
│   └── Diagrama_Paquetes_Proyecto.png
├── diagrama_patrones/
│   └── Diagrama_Patrones_Diseño.png
└── diagrama_secuencia_pago/
    └── Diagrama_Secuencia_Pago.png
```

### Regenerar los PNG

Si necesitas regenerar los PNG después de actualizar los archivos `.puml`:

```bash
# Requiere Java y PlantUML instalado
# Desde la carpeta /docs:

plantuml "diagrama_clases.puml" -o ../out/docs/diagrama_clases -Tpng
plantuml "diagrama_arquitectura.puml" -o ../out/docs/diagrama_arquitectura -Tpng
plantuml "diagrama_componentes.puml" -o ../out/docs/diagrama_componentes -Tpng
plantuml "diagrama_secuencia_pago.puml" -o ../out/docs/diagrama_secuencia_pago -Tpng
plantuml "diagrama_paquetes.puml" -o ../out/docs/diagrama_paquetes -Tpng
plantuml "diagrama_estados.puml" -o ../out/docs/diagrama_estados -Tpng
plantuml "diagrama_despliegue.puml" -o ../out/docs/diagrama_despliegue -Tpng
plantuml "diagrama_patrones.puml" -o ../out/docs/diagrama_patrones -Tpng
```

O ejecutar un script para regenerarlos todos:

```bash
#!/bin/bash
cd parcial_grupo_5/docs
mkdir -p ../out/docs

for file in diagrama_*.puml; do
    dirname="${file%.puml}"
    mkdir -p "../out/docs/$dirname"
    plantuml "$file" -o "../out/docs/$dirname" -Tpng
done

echo "Todos los diagramas han sido regenerados"
```

---

## 📖 Referencias

- [PlantUML Documentation](https://plantuml.com/)
- [UML Class Diagram](https://en.wikipedia.org/wiki/Class_diagram)
- [Design Patterns](https://refactoring.guru/design-patterns)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

---

