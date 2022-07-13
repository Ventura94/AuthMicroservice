# Para DataInt

## Tecnologías

![image](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)
![image](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)
![image](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

#### Detalles del Proyecto:

> El proyecto es un proveedor de autenticación, que puede ser utilizado como API Gateway para una arquitectura orientada
> a microservicios.

#### Requerimientos

1. Mongo DB
2. Instalar los paquetes necesarios:

 ```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Nota: El segundo archivo es para poder usar los test con pytest y otras herramientas de
desarrollo [coverage, pylint, mypy]

3. Configurar variables de entorno, siendo las siguientes que muestro de ejemplo:

```
ALGORITHM=HS256
SECRET_KEY=09c35e095fab6ca2656c918166c8a9563b93f7099f6f0f5cba6df74c88e8e3e7
MONGO_DB_URL=mongodb://localhost:27017
```

4. Correr los test:

```bash
pytest
```

5. Correr el proyecto en desarrollo:

```
python -m uvicorn main:app --reload
```

Nota: La url de la documentación: "http://127.0.0.1:8000/docs"

### Detalles a tener en cuenta:

> El único módulo que no posee test es el de service_wrapper, debido a que lo tengo previsto como libreria externa con
> sus propios test, esta prevista para que no exista acoplamiento con el ORM o base de datos utilizada, y no sea
> necesario modificar el código ante un cambio de requerimiento mediante el uso de interfaces.   