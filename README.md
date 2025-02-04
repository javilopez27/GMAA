# GMAA - Sistema Web de Apoyo a la Toma de Decisiones

## Descripción
GMAA es una aplicación de escritorio basada en la **Teoría de la Utilidad Multiatributo (MAUT)** que asiste en la toma de decisiones considerando la **imprecisión de las preferencias** de los decisores y la **incertidumbre** sobre las consecuencias de las alternativas disponibles.

El sistema se basa en la integración de **métodos de decisión multicriterio**, incluyendo:
- **MAUT** (Multi-Attribute Utility Theory)
- **OUTRANKING METHODS**
- **AHP** (Analytic Hierarchy Process)

## Objetivos del Proyecto
✔ **Readaptación e implementación** de la teoría de decisión multicriterio.
✔ **Mejorar la eficiencia** del sistema.
✔ **Optimizar la interfaz de usuario**.
✔ **Desarrollar estructuras más intuitivas**.

## Arquitectura Backend
El backend está construido en Python y contiene múltiples clases y funciones para la gestión de atributos, alternativas y nodos en el sistema. La estructura principal incluye:

### **app.py - Estructura del Código**
- **Constantes**: `PrimaryObjective`, `Branch`, `Leaf`, `identifier_labels`, `currentRow`, `currentColumn`, `attributes`, `attributesnames`, `alternatives`, `root`.
- **Clases Principales**:
  - `MyWidget`
  - `VentanaPrincipalGMAA`
  - `VentanaHelp`
  - `VentanaLogIn`
  - `VentanaAltCon`
  - `VentanaAddAlt`
  - `VentanaCUV`
  - `VentanaModifyAltCon`
  - `VentanaNodeInfo`
  - `LabelNode`
  - `ChartView`
  - `HLineFrame`
  - `DLineFrame`
  - `DLineFrameB`
  - `ContinuousAttribute`
  - `DiscreteAttribute`
  - `Alternative`
- **Funciones Clave**:
  - `fn_help()`, `fn_login()`, `getFinalAttributes()`
  - `new_workspace()`, `open_workspace()`, `save_project()`, `close_workspace()`
  - `enable_apply()`, `modifyAltCon()`, `delete_PO()`
  - `on_combo_box_changed()`, `create_table()`, `disable_discrete()`, `disable_continuous()`
  - `mousePressEvent()`, `mouseMoveEvent()`, `mouseReleaseEvent()`

## Tecnologías Utilizadas
- **Lenguaje de Programación**: Python
- **Frameworks y Bibliotecas**: PyQt, Pandas, Numpy
- **Bases de Datos**: SQLite / PostgreSQL (según implementación)
- **Otras Herramientas**: Git, Docker, Jenkins

## Instalación y Uso
### 1️ **Clonar el Repositorio**
```bash
 git clone https://github.com/tuusuario/gmaa.git
 cd gmaa
```

### 2️ **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### 3️ **Ejecutar la Aplicación**
```bash
python app.py
```

## Uso
1. **Iniciar sesión** en la plataforma.
2. **Cargar un workspace** existente o crear uno nuevo.
3. **Definir los atributos y alternativas**.
4. **Utilizar el sistema para evaluar decisiones** con base en criterios multicriterio.
5. **Visualizar gráficos** y análisis generados por el modelo.

## Contribuciones
Si deseas contribuir al desarrollo de **GMAA**, ¡eres bienvenido! Por favor, sigue estos pasos:
1. **Haz un fork** del repositorio.
2. **Crea una nueva rama** para tu mejora (`git checkout -b feature-nueva-mejora`).
3. **Realiza tus cambios y sube los commits** (`git commit -m 'Descripción del cambio'`).
4. **Envía un Pull Request** y lo revisaremos.

---
**Autor**: Javier López Palacios  
**Última actualización**: Febrero 2019
