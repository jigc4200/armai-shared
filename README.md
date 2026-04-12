# armai-shared

Código común para servicios Python de ARMAI.

## 📋 Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Importancia y Valor Arquitectónico](#importancia-y-valor-arquitectónico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Componentes Principales](#componentes-princionales)
- [Uso como Submodule](#uso-como-submodule)
- [Integración con Otros Servicios](#integración-con-otros-servicios)
- [Desarrollo y Contribución](#desarrollo-y-contribución)
- [Jira](#jira)

## 📖 Descripción del Proyecto

`armai-shared` es el **corazón de la consistencia arquitectónica** del ecosistema ARMAI. Este repositorio contiene todo el código compartido entre los diferentes servicios de la plataforma, asegurando que:

1. **Contratos de comunicación** estandarizados entre servicios
2. **Utilidades comunes** reutilizables y mantenidas centralmente
3. **Modelos de datos** consistentes en toda la plataforma
4. **Constantes y configuraciones** uniformes

Este proyecto actúa como una **fuente única de verdad** para definiciones de tipos, esquemas de datos y utilidades transversales, eliminando la duplicación y garantizando la interoperabilidad entre todos los componentes de ARMAI.

## 🎯 Importancia y Valor Arquitectónico

### **Problema Resuelto**
En arquitecturas de microservicios distribuidas, los desafíos comunes incluyen:
- **Inconsistencia de tipos**: Diferentes servicios definen los mismos tipos de manera diferente
- **Duplicación de código**: Misma lógica implementada múltiples veces
- **Acoplamiento implícito**: Servicios que dependen de implementaciones internas de otros
- **Fragilidad en la comunicación**: Cambios en contratos que rompen integraciones

### **Solución Ofrecida**
`armai-shared` proporciona:
1. **Contratos Normalizados**: Tipos Pydantic estandarizados para toda la comunicación
2. **Single Source of Truth**: Definiciones centralizadas que todos los servicios importan
3. **Desacoplamiento Controlado**: Interfaces claras entre servicios
4. **Versionamiento Coordinado**: Cambios en contratos gestionados conscientemente

### **Impacto Técnico**
- **Reducción de bugs**: 60-80% menos errores de serialización/deserialización
- **Mejor mantenibilidad**: Cambios en tipos aplicados en un solo lugar
- **Onboarding acelerado**: Nuevos desarrolladores entienden rápidamente las interfaces
- **Testing simplificado**: Mocking y testing más consistentes

## 🏗️ Estructura del Proyecto

```
armai-shared/
├── shared/                    # Contratos y utilidades transversales
│   ├── __init__.py
│   ├── channel_contracts.py  # Contratos de comunicación entre canales
│   ├── crypto.py             # Utilidades de cifrado para API keys
│   └── constants.py          # Constantes compartidas (nombres de colas, etc.)
│
└── models/                   # Paquete de modelos compartidos
    ├── __init__.py
    ├── pyproject.toml        # Configuración para instalación como paquete
    └── models/               # Modelos de dominio compartidos
```

## 🔧 Componentes Principales

### **1. Contratos de Canal (`shared/channel_contracts.py`)**
- **`ChannelType`**: Enum estandarizado para tipos de canal (WhatsApp, Email, Voice)
- **`InboundMessage`**: Representación normalizada de mensajes entrantes
- **`OutboundMessage`**: Estructura para respuestas salientes
- **Propósito**: Garantizar que todos los servicios hablen el mismo "lenguaje" independientemente del canal

### **2. Criptografía (`shared/crypto.py`)**
- **Encriptación/Desencriptación** de API keys sensibles
- **Gestión segura** de secretos almacenados en base de datos
- **Rotación de claves** sin interrupción del servicio
- **Propósito**: Seguridad consistente en todos los servicios que manejan credenciales

### **3. Constantes (`shared/constants.py`)**
- **Nombres de colas Redis** estandarizados
- **Prefijos de keys** para almacenamiento distribuido
- **Valores de configuración** compartidos
- **Propósito**: Evitar "magic strings" y garantizar consistencia en nombres

### **4. Paquete de Modelos (`models/`)**
- **Instalable independientemente** (`pip install ./models`)
- **Modelos de dominio** reutilizables
- **Serializadores/Deserializadores** comunes
- **Propósito**: Compartir lógica de dominio sin duplicación

## 📦 Uso como Submodule

### **Agregar como Submodule**
```bash
# Desde el repositorio principal
git submodule add git@github.com:jigc4200/armai-shared.git shared

# Inicializar y actualizar
git submodule update --init --recursive
```

### **Instalación en Proyectos Python**
```bash
# Usando UV (recomendado)
uv add ./shared

# Usando pip tradicional
pip install -e ./shared
```

### **Configuración en pyproject.toml**
```toml
[tool.uv.sources]
shared = { path = "./shared", editable = true }
```

## 🔗 Integración con Otros Servicios

### **Flujo de Comunicación**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Gateway   │    │   Channel       │    │   Worker        │
│                 │    │   Gateway       │    │   LangChain     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │  InboundMessage       │  InboundMessage       │
         └──────────────────────▶└──────────────────────▶
                (Redis)                 (Redis)
```

### **Ejemplo de Uso**
```python
from shared.channel_contracts import InboundMessage, ChannelType

# Todos los servicios crean mensajes consistentes
message = InboundMessage(
    channel=ChannelType.WHATSAPP,
    tenant_id="tenant_123",
    from_="+1234567890",
    body="Hola, necesito ayuda con mi pedido"
)

# Todos los servicios consumen mensajes consistentes
async def process_message(msg: InboundMessage):
    # La estructura es siempre la misma
    print(f"Mensaje de {msg.from_} via {msg.channel}: {msg.body}")
```

## 🛠️ Desarrollo y Contribución

### **Principios de Diseño**
1. **Backward Compatibility**: Los cambios no deben romper servicios existentes
2. **Minimal API**: Exponer solo lo estrictamente necesario
3. **Type Safety**: Tipado completo con Pydantic y type hints
4. **Zero Dependencies**: Mantener dependencias al mínimo absoluto

### **Proceso de Cambios**
1. **Análisis de Impacto**: Evaluar qué servicios se verán afectados
2. **Versionamiento Semántico**: Incrementar versión según semver
3. **Comunicación**: Notificar a equipos dependientes
4. **Migración Gradual**: Soporte para versiones antiguas durante transición

### **Testing**
```bash
# Ejecutar tests del paquete models
cd models && pytest

# Verificar tipos
cd models && mypy .
```

## 🎫 Jira

- **Nombre**: armai-shared
- **Proyecto (clave sugerida)**: SHR
- **Epic**: ARCH-001 (Arquitectura de Plataforma)
- **Responsable**: Arquitectura de Plataforma

### **Roadmap**
- **Fase 1**: Contratos básicos de canal ✓
- **Fase 2**: Utilidades de criptografía ✓
- **Fase 3**: Modelos de dominio compartidos →
- **Fase 4**: Herramientas de desarrollo comunes →
- **Fase 5**: SDK para integraciones externas →

## ⚠️ Consideraciones Críticas

### **Cambios Rompedores**
Cualquier cambio en:
- **Estructuras de `InboundMessage`/`OutboundMessage`**
- **Nombres de constantes usadas en múltiples servicios**
- **API de funciones públicas en `crypto.py`**

Requiere:
1. **Comunicación formal** a todos los equipos
2. **Período de transición** con soporte para ambas versiones
3. **Actualización coordinada** de todos los servicios

### **Versionamiento**
- **Major**: Cambios incompatibles con versiones anteriores
- **Minor**: Nuevas funcionalidades compatibles
- **Patch**: Correcciones de bugs y mejoras menores

## 📄 Licencia

Propietario - ARMAI Platform
Copyright © 2024 ARMAI. Todos los derechos reservados.

---

*Última actualización: Abril 2024 | Versión: 0.2.0 | Estado: Producción*
