# armai-shared

Código común para servicios Python de ARMAI.

## Estructura

- `shared/`: Contratos y utilidades transversales
  - `channel_contracts.py`: Contratos de comunicación entre canales
  - `crypto.py`: Utilidades de cifrado
  - `constants.py`: Constantes compartidas
  
- `models/`: Paquete de modelos compartidos
  - Instalable como `pip install ./models`

## Uso como Submodule

```bash
git submodule add git@github.com:jigc4200/armai-shared.git shared
```

## Jira

- Nombre: armai-shared
- Proyecto (clave sugerida): SHR
