#:after:nereid/nereid:section:ficheros_estaticos#

CMS
===

Dispone de la gestión de elementos base para su web, como:

* Artículos
* Menús
* Banners

Artículos
---------

En |menu_cms_article| podrá publicar artículos estáticos para su web. Estos contenidos
son informarción estática para su web como:

* Horario comercial
* Contacto
* Delegaciones
* Disposiciones legales
* ...

Estos contenidos podemos añadir código HTML para dar elementos gráficos. Consulte con
su diseñador gráfico para que elabore estos contenidos.

.. |menu_cms_article| tryref:: nereid_cms.menu_cms_article_form/complete_name

Menús
-----

En |menu_cms_menu| podrá organizar los menús de su web añadiendo o quitando opciones.
En la plantilla de su web existe un tag para renderizar un *bloque de menú* (por código).
Por cada bloque podrá añadir o modificar los menús.

* El campo URI hace referencia la URL donde deberá apuntar el menú; una URL interna o externa.
* El campo código es el identificador del bloque del menú.

.. |menu_cms_menu| tryref:: nereid_cms.menu_cms_menu_form/complete_name

Banners
-------

En |menu_cms_banner| podrá organizar los banners de su web añadiendo o quitando opciones.
En la plantilla de su web existe un tag para renderizar un *banner* (por código).

* El campo código es el identificador del banner.

Los banners pueden ser:

* Imagenes
* Imagenes remotas
* Código personalizado

.. |menu_cms_banner| tryref:: nereid_cms.menu_cms_banner_form/complete_name
