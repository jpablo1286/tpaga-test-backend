# MiniApp - Prueba Tecnica - Tpaga
Este proyecto de MiniApp, se divide en dos parte, la primera es el backend,
y la segunda es la UI. Para un tiempo total de desarrollo de 6 dias.

## Backend
El backend se desarrolla en django, usando rest framework. por motivos de
sencilles se utiliza una Base Datos embebida sqllite. Este backend se desarrolla
para ser desplegado como contenedor Docker. las tares para esta parte del proyecto
se listan a continuación

* Diseñar/Modelar la base de datos.
* Preparar django y prerequisitos
* Escribir los modelos y serializadores
* Escribir las vistas
* Integrar con Tpaga
* Pruebas y Correciones
* Despliegue

## UI
La UI se desarrolla en Angular-Material, la cual consumira el API proporcinada
por el backend, se procura un diseño responsive, pero no se prioriza, se diseña como
prioridad para dispositivo movil, de acuerdo a requerimientos. La UI tambien se desarrolla
para despliegue como contenedor  Las tares implicadas
se listan a continuación.

* Preparar Angular-Material y prerequisitos
* Crear los componentes necesarios
* Escribir los templates para cada componente
* Escribir los methodos (acciones) para cada componente en typescript
* Escribir las hojas de estilo (CSS)
* Pruebas y Correciones
* Despliegue


## Como hacer uso de este repositorio
Este repositorio cuenta con un script que permite desplegar un contenedor Docker, tanto para
trabajar en pruebas, como para desplegar en modo "produccion", las sintaxis es la siguiente:

```sh
$ ./start.sh <dev>
```
[dev] :se agraga la palabra "dev" para inidicar que se inicia en modo desarrollo, en este modo el directorio "tpaga" es montado
como volumen en el contenedo Docker, así que los cambios que hagamos en este se reflejaran de inmediato en el contenedor.

Una vez inicia el contenedor este empezara a escuchar peticiones en el puerto 8000, donde usando el estandar Restful.
