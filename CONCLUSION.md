# Reflexión - Backend Control Transportistas

## 1. Retos Encontrados

### Técnicos
- **Serialización de fechas**: FastAPI generaba errores de validación al convertir datetime a string en respuestas JSON.
- **Redirects de rutas**: Las rutas sin trailing slash causaban redirects 307, complicando las pruebas.

### De Diseño
- **Validación de estado de rutas**: Implementar un ciclo de vida complejo con transiciones controladas entre estados.
- **Cálculos automáticos**: Desarrollar lógica para métricas de rendimiento calculadas en tiempo real.
- **Separación de responsabilidades**: Mantener capas claras entre repositorio, servicio y API.

### De Integración Frontend-Backend
- **CORS**: Configurar políticas de origen cruzado para permitir requests desde Angular.
- **Documentación de API**: Asegurar que los parámetros de query aparezcan correctamente en Swagger.
- **Mensajes de error**: Proporcionar respuestas en español para mejor experiencia de usuario.

## 2. Cómo Fueron Solucionados

### Técnicos
- **Serialización de fechas**: Cambié los tipos en los schemas de `str` a `datetime`, permitiendo que FastAPI maneje la conversión automáticamente a ISO 8601.
- **Redirects de rutas**: Forcé las rutas con y sin trailing slash para compatibilidad, evitando los redirects 307.

### De Diseño
- **Validación de estado**: Creé un enum `RouteStatus` y lógica en el servicio que valida transiciones permitidas (ASIGNADA→EN_RUTA→COMPLETADA).
- **Cálculos automáticos**: Implementé el método `_calculate_metrics()` en el servicio de rendimiento, calculando eficiencia de combustible, tiempo y puntuación general.
- **Separación de capas**: Mantuve repositorios para acceso a datos, servicios para lógica de negocio y rutas para exposición de API.

### De Integración Frontend-Backend
- **CORS**: Agregué middleware CORSMiddleware permitiendo orígenes específicos de desarrollo (localhost:4200, etc.).
- **Documentación**: Incluí descripciones detalladas en los parámetros Query de FastAPI para que aparezcan en Swagger.
- **Mensajes de error**: Traduje todos los mensajes de error de inglés a español en los parámetros `detail` de HTTPException.

**Alternativas consideradas**: Para los redirects, consideré configurar FastAPI globalmente, pero opté por la simplicidad. Para CORS, evalué configuración más restrictiva pero prioricé facilidad de desarrollo.

## 3. Aprendizajes

### Qué Aprendió Nuevo
- **FastAPI Response Models**: Los schemas deben usar tipos Python nativos (datetime) en lugar de strings para serialización automática.
- **SQLModel Constraints**: Las restricciones se definen en los modelos y se aplican automáticamente en la base de datos (Usando SQLModel)
- **Dependency Injection**: El patrón `Depends()` de FastAPI facilita el desacoplamiento y testing de componentes.
- **CORS Middleware**: Configuración necesaria para integración frontend-backend en desarrollo.

### Qué Mejoraría con Más Tiempo
- **Testing**: Implementar tests unitarios e integración para validar la lógica de negocio.
- **Migraciones**: Sistema de migraciones de base de datos (Alembic) para cambios de schema en producción.
- **Autenticación**: Sistema JWT completo para proteger endpoints.
- **Monitoreo**: Logs estructurados y métricas de rendimiento.
- **Documentación**: Documentación más detallada de la API con ejemplos de uso.
- **Validaciones**: Más validaciones de negocio, como límites de distancia o tiempo para rutas.

---

**Conclusión**: La implementación cumplió todos los requisitos técnicos con una arquitectura sólida. Los retos encontrados fortalecieron el entendimiento de FastAPI y mejores prácticas de desarrollo backend.
