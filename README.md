# Proyecto de Validación de Datos con Great Expectations

## Descripción

Este proyecto es un prototipo que utiliza la biblioteca Great Expectations para automatizar el control de calidad de datos durante la carga de nuevos datos mediante procesos ETL. Se configura para generar informes HTML que documentan los resultados de las validaciones realizadas en un entorno de base de datos SQL, asegurando la integridad y calidad de los datos cargados.

## Configuración del Entorno

Antes de iniciar, asegúrate de que las variables de entorno estén configuradas correctamente en tu archivo `.env`:

```plaintext
SQL_CONNSTRING_170_PRE="mssql+pyodbc://<usuario>:<contraseña>@<host>,<puerto>/"
SQL_CONNSTRING_170_POST="?driver=ODBC+Driver+17+for+SQL+Server&autocommit=true"
SQL_CONNSTRING_170_DB=<dbname>
```

**Nota:** Sustituye `<usuario>`, `<contraseña>`, `<host>`, `<puerto>` y `<dbname>` con tus credenciales reales y la información del servidor.

## Instalación

Para ejecutar las validaciones, debes seguir estos pasos:

1. Instala las dependencias necesarias: `pip install -r requirements.txt`.
2. Ejecuta el script principal (en la carpeta de scripts) para iniciar las validaciones y generar la documentación de datos. `python <PAIS_ISO2>_qa.py`. Sustituye `<usuario>` por el código ISO2 del país. Esta demo contiene unas validaciones para Panamá cuya ISO2 es "PA".

## Componentes del Proyecto

### Conexión a la Fuente de Datos

Establecimiento de una conexión a una base de datos SQL y configuración de una fuente de datos dentro del contexto de Great Expectations.

### Creación y Ejecución de Expectativas

Definición y configuración de expectativas específicas para validar:

- Presencia de valores nulos.
- Unicidad de valores en las columnas.
- Rangos específicos de valores (fechas, números, etc.).

### Checkpoints

Configuración y ejecución de checkpoints para validar los datos contra las expectativas definidas y documentar los resultados.

## Expansión de Reglas y Expectativas

### Ideas para Nuevas Reglas

- **Consistencia Temporal:** Validar que las fechas en los registros sean realistas y se mantengan dentro de un rango lógico.
- **Validación de Relaciones:** Asegurar que las claves foráneas correspondan a registros válidos en otras tablas.
- **Patrones de Datos:** Implementar expectativas para validar formatos específicos como correos electrónicos o números de teléfono.
- **Análisis de Tendencias:** Detectar cambios significativos que podrían indicar problemas de calidad de los datos.

### Automatización de Pruebas

Integración de estas validaciones en un pipeline de CI/CD para ejecutar automáticamente las pruebas de datos con cada actualización de la base de datos o cambio en las definiciones de expectativas.

## Contribuciones

Te invitamos a contribuir al proyecto. Si tienes sugerencias o mejoras, crea un pull request o abre un issue en el repositorio del proyecto.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE.md` para más detalles.

# Fuentes Documentales

- https://docs.greatexpectations.io/docs/oss/
- https://www.paradigmadigital.com/dev/great-expectations-data-assistant/ 