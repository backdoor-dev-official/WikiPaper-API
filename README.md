# WikiPaper-API
[WIP]

#17/01/2024 | 03:43 AM

 At the moment it is still in work in progress but the server is close to 90% ready for now it is quite simple and still in development but I saw the need to make use of a client because I am having some bugs but I am working on it for now it works quite well but the latest bugs are solved I am going to add version 1.0 and I will try to prepare the public servant.

#17/01/2024 | 03:43 AM

 Por el momento todavía está en trabajo en progreso pero el servidor está cerca del 90% listo por ahora es bastante simple y aún en desarrollo pero vi la necesidad de hacer uso de un cliente porque estoy teniendo algunos errores pero estoy trabajando en ello por ahora funciona bastante bien pero los últimos errores están solucionados voy a agregar la versión 1.0 y trataré de Preparar al servidor público.

#18/01/2024 | 08:56 AM

 Some changes were made and errors were fixed. It should be usable with curl and the client would not be required. I am working on resolving a final error with file upload and after that, file lists would be available. The request of file content and file upload are already done, but there are some security issues that are being worked on. They are actually done, but there are some errors that are being resolved. It may be ready in a week, at most in one day.

#18/01/2024 | 08:56 AM

 Se realizaron algunos cambios y se corrigieron errores. Debería ser utilizable con curl y el cliente no sería necesario. Estoy trabajando para resolver un error final con la carga de archivos y después de eso, las listas de archivos estarían disponibles. La solicitud de contenido de archivos y la carga de archivos ya están realizadas, pero hay algunos problemas de seguridad en los que se está trabajando. En realidad están hechos, pero hay algunos errores que se están resolviendo. Puede estar listo en una semana, como mucho en un día.

#19/01/2024 | 02:25 AM

 The basic logic of the server is 100% complete. The public server will be ready from tomorrow at around 5pm. I will start working on creating documentation now, so you can learn how to implement it in your code if you want. You must give credit if you do. The main functions will be revealed. Binaries will be made for both Windows and Linux, but it will take a little longer for Linux because I don't know how to compile for Linux yet. I'm going to try to learn. After finishing the documentation, I will work on a graphical client. I plan to try to learn Flutter or something similar to bring an app to Android as well. That's all the update for now. I plan to add a roadmap soon. It's quite possible that it will also be when the public server opens at around 1am. I will post a place where you can share your ideas for adding to the API. Please keep in mind that this is my first major project and I am also a high school junior. Please be patient. I would like to inform you that this is Argentina time. I plan to create a Discord server where you can interact with me. Thank you for your time.

#19/01/2024 | 02:25 AM

 ¡Buenas noticias! El núcleo del servidor está 100% completo y ¡la versión pública estará disponible mañana a las 5pm! Mientras tanto, me dedicaré a crear la documentación para que puedas implementarlo en tu código si lo deseas. Eso sí, ¡recuerda darme crédito! Te explicaré las funciones principales. También prepararé binarios para Windows y Linux, aunque tardaré un poco más con Linux porque aún no sé compilar para ese sistema. ¡Pero lo intentaré! Luego de la documentación, me enfocaré en un cliente gráfico. También quiero aprender Flutter o algo similar para crear una app para Android. De momento, ¡eso es todo! Pronto subiré un roadmap, quizás a la 1am junto con la apertura del servidor público. Y abriré un espacio para que compartas tus ideas para ampliar la API. Ten en cuenta que este es mi primer proyecto grande y que aún estoy en la secundaria, así que ¡sé paciente! Por cierto, todo esto está basado en el horario de Argentina. También planeo crear un servidor de Discord para que podamos interactuar. ¡Gracias por tu tiempo!

#19/01/2024 | 5:05 PM

 Here are some security limitations I'll implement: file size limit, only .txt and .md files can be uploaded, and only to the unofficial folder. I'll also release the server code in the future, within a week or two. By the time the public server is up, I'll have already tried to attack it to test its security. So, there will be a minimum of security. I'm also working on a graphics client with Flutter.

#19/01/2024 | 5:05 PM

 Implementé algunas limitaciones de seguridad, como un límite de tamaño de archivo, solo se permiten archivos .txt y .md, y solo se pueden subir a la carpeta "unofficial". Igualmente, en el futuro, dentro de una semana o dos, posiblemente liberaré el código del servidor también. Para cuando el servidor público esté disponible, ya habré intentado hacer ataques informáticos al mismo para probar su seguridad. Por lo tanto, habrá un mínimo de seguridad. Estoy trabajando tambien en un cliente grafico con flutter exactamente con el modulo flet de python.

#22/01/2024 | 12:12am

I'm really sorry about the server outage last weekend. As you know, I had to change the operating system of the server from ArchLinux to Ubuntu Server. This caused some problems, but the documentation is now corrected and the instance that appears in the examples is now the new public instance.
The interface is progressing well. I wanted to make it with Flet, but Flet has been giving me some headaches. It's possible that I can resolve them, but it's also possible that the first interface will be released with Tkinter.
I'm also starting to work on the Discord server. I hope it will be ready by next week.
Thanks for your patience and understanding.

#22/01/2024 | 12:12am

Lamento mucho la caída del servidor ayer. Como saben o no, tuve que cambiar el sistema operativo del servidor de ArchLinux a Ubuntu Server. Esto se debe a que ArchLinux me causó algunos problemas, pero la documentación ya está corregida y la instancia que aparece en los ejemplos ahora es la nueva instancia pública.
La interfaz está avanzando bien. Quería hacerla con Flet, pero he tenido algunos problemas. Es posible que pueda resolverlos, pero también es posible que la primera interfaz se lance con Tkinter.
También estoy empezando a trabajar en el servidor de Discord. Espero que esté listo para la próxima semana.
Gracias por su paciencia y comprensión.

###DOCS EN ESPAÑOL

### Funciones principales

> El sistema cuenta con tres funciones principales:
>
> * **List:** Esta función genera una lista de los archivos contenidos en la carpeta seleccionada. La carpeta puede ser **official** o **unofficial**. El método utilizado es **GET**.
> * **Upload:** Esta función permite subir archivos a la carpeta seleccionada. Las limitaciones actuales son: tamaño máximo de 10 MB y extensiones permitidas: **.txt** y **.md**. Si los usuarios sugieren extensiones adicionales o un tamaño máximo mayor, se considerarán las solicitudes. El método utilizado es **POST**.
> * **File:** Esta función permite obtener el contenido de un archivo determinado. Para ello, es necesario haber utilizado previamente la función **List** para obtener el nombre y el tipo del archivo. El método utilizado es **POST**.
>
> El lanzamiento del servidor Discord está previsto para dentro de una semana aproximadamente.

 **Listar archivos**

Para listar los archivos en la carpeta "official":

```
curl -X GET https://long-right-analyzed-diameter.trycloudflare.com/list?path=official
```

Para listar los archivos en la carpeta "unofficial":

```
curl -X GET https://long-right-analyzed-diameter.trycloudflare.com/list?path=unofficial
```

**Subir un archivo**

Para subir un archivo llamado "example.txt" a la carpeta "unofficial":

```
curl -F file=@example.txt https://long-right-analyzed-diameter.trycloudflare.com/upload
```

**Leer el contenido de un archivo**

Para leer el contenido del archivo "example.md" en la carpeta "official":

```
curl -X POST https://long-right-analyzed-diameter.trycloudflare.com/file/official/example.md
```

Para leer el contenido del archivo "example.txt" en la carpeta "unofficial":

```
curl -X POST https://long-right-analyzed-diameter.trycloudflare.com/file/unofficial/example.txt
```

**Ejemplos de parámetros**

El parámetro `path` es opcional y puede establecerse en "official" o "unofficial" para especificar la carpeta que se desea consultar.

El parámetro `file` es obligatorio y debe especificar el archivo que se desea subir o leer. Puede ser un archivo local o una URL.

**Ejemplo de error**

Si se intenta subir un archivo de un tipo no permitido, se recibirá un error HTTP 400:

```
curl -F file=@example.exe https://long-right-analyzed-diameter.trycloudflare.com/upload
```

```
< HTTP/1.1 400 Bad Request
< Content-Type: application/json

{
  "detail": "File type not allowed. Only .md or .txt files are allowed."
}
```

###DOCS IN ENGLISH

### Main Functions

> The system has three main functions:
>
> * **List:** This function generates a list of the files contained in the selected folder. The folder can be **official** or **unofficial**. The method used is **GET**.
> * **Upload:** This function allows you to upload files to the selected folder. The current limitations are: maximum size of 10 MB and allowed extensions: **.txt** and **.md**. If users suggest additional extensions or a larger maximum size, the requests will be considered. The method used is **POST**.
> * **File:** This function allows you to get the content of a specific file. To do this, you must have previously used the **List** function to obtain the name and type of the file. The method used is **POST**.
>
> The launch of the Discord server is scheduled for within a week approximately.

**Listing files**

To list the files in the "official" folder, run the following command:

```
curl -X GET https://long-right-analyzed-diameter.trycloudflare.com/list?path=official
```

To list the files in the "unofficial" folder, run the following command:

```
curl -X GET https://long-right-analyzed-diameter.trycloudflare.com/list?path=unofficial
```

**Uploading a file**

To upload the file "example.txt" to the "unofficial" folder, run the following command:

```
curl -F file=@example.txt https://long-right-analyzed-diameter.trycloudflare.com/upload
```

**Reading the contents of a file**

To read the contents of the file "example.md" in the "official" folder, run the following command:

```
curl -X POST https://long-right-analyzed-diameter.trycloudflare.com/file/official/example.md
```

To read the contents of the file "example.txt" in the "unofficial" folder, run the following command:

```
curl -X POST https://long-right-analyzed-diameter.trycloudflare.com/file/unofficial/example.txt
```

**Parameter examples**

The `path` parameter is optional. If it is not specified, the default folder is "official".

The `file` parameter is required. It must specify the path to the file to be uploaded or read. The path can be a local file or a URL.

**Error example**

If an attempt is made to upload a file of an unsupported type, an HTTP 400 error will be returned. The error response will include the following JSON object:

```
{
 "detail": "File type not allowed. Only .md or .txt files are allowed."
}
```

 **The errors from upload are in spanish sorry i forgot to translate that in 1 week i'll translate that mensagges an the public instance will change of url.**

![Alt](https://repobeats.axiom.co/api/embed/0f49858a84160d6696cdaa3b393a68db4ba52277.svg "Repobeats analytics image")
