### ¿Qué es AWS CodeFamily?

> Es un conjunto de servicios ofrecidos por AWS que están diseñados para ayudar a los desarrolladores a automatizar y agilizar el ciclo de vida del desarrollo de software. Estos servicios están enfocados en diferentes etapas del proceso de desarrollo y ofrecen herramientas y funcionalidades específicas.

> La familia de servicios de AWS CodeFamily incluye:

- AWS CodeCommit: Es un servicio de alojamiento de repositorios de control de versiones completamente administrado basado en Git. Permite a los equipos de desarrollo almacenar y administrar su código fuente de manera segura en la nube
- AWS CodeBuild: Es un servicio de compilación y prueba completamente administrado. Permite a los desarrolladores compilar, probar y generar artefactos de software de manera automatizada y escalable
- AWS CodeDeploy: Es un servicio de implementación de aplicaciones automatizado que permite a los desarrolladores desplegar aplicaciones de forma rápida y consistente en instancias de Amazon EC2, servidores locales y otros servicios de AWS
- AWS CodePipeline: Es un servicio de entrega continua completamente administrado que ayuda a los desarrolladores a automatizar el flujo de trabajo de entrega de aplicaciones. Permite la configuración de pipelines personalizados que incluyen etapas y acciones para compilar, probar y desplegar aplicaciones
- AWS CodeStar: Es un servicio que combina varios servicios de la familia AWS CodeFamily para ofrecer una experiencia de desarrollo integrada. Proporciona plantillas preconfiguradas para diferentes tipos de proyectos y facilita la colaboración en equipos de desarrollo

> En conjunto, los servicios de AWS CodeFamily ofrecen a los desarrolladores una gama completa de herramientas y funcionalidades para agilizar y automatizar el desarrollo, prueba, implementación y entrega de aplicaciones en la nube de AWS. Estos servicios trabajan de manera conjunta para ayudar a los equipos a aumentar la eficiencia, la calidad y la velocidad en el desarrollo de software.

### Tarea 1
### Requisitos previos
### Configurar el IDE de AWS Cloud9
> AWS Cloud9 es un IDE basado en la nube que facilita la escritura, ejecución y depuración de código directamente desde un navegador web. Este entorno de desarrollo integrado incluye un editor de código, un depurador y una terminal. Cloud9 viene preconfigurado con todas las herramientas necesarias para los lenguajes de programación más populares, eliminando la necesidad de instalar archivos o configurar su propia máquina de desarrollo al comenzar nuevos proyectos.
> Lanzar un nuevo IDE de Cloud9

1. Dirigirse al servicio de AWS Cloud9
2. Hacer clic en Crear entorno
3. Proporcionar un nombre para el entorno y proporcionar una descripción útil
4. Seleccionar Crear una nueva instancia EC2 para el entorno. Para el tipo de instancia seleccionar t2.micro y para la plataforma Amazon Linux 2. Los ajustes restantes se pueden dejar como predeterminados
5. Hacer clic en Crear entorno

### Tarea 2
### AWS CodeCommit

> AWS CodeCommit es un servicio de alojamiento de repositorios de control de código fuente basado en Git, que se administra de manera segura y escalable. CodeCommit proporciona la capacidad de alojar repositorios privados de Git sin la necesidad de administrar su propio sistema de control de código fuente ni escalar su infraestructura.

> En esta tarea, nos enfocaremos en la configuración de un repositorio de CodeCommit para almacenar el código Java.

### Crear un repositorio
1. Dirigirse al servicio de AWS CodeCommit
2. Hacer clic en Crear repositorio. Establecer el nombre de lab-web-project y darle una descripción. También agregar una etiqueta con clave y valor
3. Hacer clic en Crear
4. En la página siguiente, seleccionar Clonar URL y Clonar HTTPS. Esto copiará la URL del repositorio al portapapeles. La URL tendrá el siguiente formato:

```
https://git-codecommit.<region>.amazonaws.com/v1/repos/<project-name>
```

> Mantener esta URL a mano para la siguiente sección.

### Confirma el código
1. Regresar al entorno de Cloud9 y configurar la identidad de Git:

```
git config --global user.name "<your name>"
git config --global user.email <your email>
```

2. Asegurarse de estar en ~/environment/lab-web-project e iniciar el repositorio local y establecer el origen remoto en la URL de CodeCommit que copió anteriormente:

```
cd ~/environment/lab-web-project
git init -b main
git remote add origin <HTTPS CodeCommit repo URL>
```

3. Ahora se va a confirmar y enviar el código
```
git add *
git commit -m "Initial commit"
git push -u origin main
```

4. Debería poder actualizar la página de CodeCommit en la consola de AWS y ver los archivos recién creados

> Ahora tenemos un repositorio de CodeCommit en funcionamiento para almacenar y controlar la versión del código. A continuación, necesitamos una forma de obtener los paquetes para generar nuestro archivo WAR de Java.

### Tarea 3
### AWS CodeArtifact
> AWS CodeArtifact es un servicio de repositorio de artefactos completamente administrado que simplifica el proceso de obtención, almacenamiento, publicación y compartición segura de paquetes de software utilizados en el desarrollo de software de cualquier organización.

> En este paso, nos enfocaremos en configurar un repositorio de CodeArtifact que utilizaremos durante la fase de compilación con CodeBuild para obtener paquetes de Maven de un repositorio público conocido como el Repositorio central de Maven. Utilizar CodeArtifact en lugar de acceder directamente al repositorio público tiene múltiples ventajas, como una mejor seguridad al poder definir de manera precisa qué paquetes se pueden utilizar.

> Dentro de este laboratorio, utilizaremos CodeArtifact como un simple caché de paquetes. Esto significa que, incluso si el repositorio de paquetes público no estuviera disponible, aún podríamos construir nuestra aplicación. En situaciones reales, esto es un requisito importante para mitigar el riesgo de que una interrupción del repositorio público afecte toda la cadena de CI/CD. Además, ayuda a garantizar que los paquetes en los que depende nuestro proyecto, y que pueden haber sido eliminados del repositorio público (ya sea accidental o intencionalmente), no interrumpan el flujo de CI/CD, ya que seguirán disponibles a través de CodeArtifact en ese caso.

### Crear Dominio y Repositorio
1. Dirigirse al servicio de AWS CodeArtifact
2. Seleccionar Dominios en el menú de la izquierda, luego Crear dominio. Establecer un nombre y hacer clic en Crear dominio para finalizar la configuración del dominio
3. Ahora, hacer clic en Crear repositorio para crear un repositorio para este nuevo dominio. Establecer un nombre y darle una descripción
4. Seleccionar maven-central-store como repositorio ascendente público y hacer clic en Siguiente
5. Revisar la configuración. Tenga especialmente en cuenta la sección de flujo de paquetes que visualiza cómo se crearán dos repositorios como parte del proceso: el repositorio de paquetes que creó anteriormente, así como un repositorio ascendente (maven-central-store), que sirve como un intermediario entre el repositorio público. Hacer clic en Crear repositorio para finalizar el proceso

### Conectar el repositorio de CodeArtifact
1. En la página siguiente, hacer clic en Ver instrucciones de conexión. En el cuadro de diálogo, hacer clic en Mac y Linux como sistema operativo y mvn como administrador de paquetes
2. Copiar el comando para el token de autorización y ejecutarlo en el símbolo del sistema de Cloud9. Esto se verá similar al siguiente. Asegúrese de ajustar el propietario del dominio y, si está presente, la región a su ID de cuenta y región, respectivamente

```
export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain unicorns --domain-owner 123456789012 --query authorizationToken --output text`
```

3. Para los siguientes pasos, tendremos que actualizar settings.xml. Como esto aún no existe, vamos a crearlo primero:

```
cd ~/environment/lab-web-project
echo $'<settings>\n</settings>' > settings.xml
```

4. Abrir el archivo settings.xml recién creado en el árbol de directorios de Cloud9 y seguir los pasos restantes en el cuadro de diálogo Instrucciones de conexión en la consola de CodeArtifact , incluida la sección espejo. El archivo completo se verá similar al siguiente. Cerrar el cuadro de diálogo cuando termine haciendo clic en Listo

> Nota: 
NO copie/pegue el contenido a continuación en su archivo settings.xml, ya que esto es solo para ilustrar la estructura; su propio archivo settings.xml usará diferentes URL, que debe copiar desde el cuadro de diálogo CodeArtifact.

```
<settings>
    <profiles>
        <profile>
            <id>unicorns-unicorn-packages</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <repositories>
                <repository>
                    <id>unicorns-unicorn-packages</id>
                    <url>https://unicorns-123456789012.d.codeartifact.us-east-2.amazonaws.com/maven/unicorn-packages/</url>
                </repository>
            </repositories>
        </profile>
    </profiles>
    <servers>
        <server>
            <id>unicorns-unicorn-packages</id>
            <username>aws</username>
            <password>${env.CODEARTIFACT_AUTH_TOKEN}</password>
        </server>
    </servers>
    <mirrors>
        <mirror>
            <id>unicorns-unicorn-packages</id>
            <name>unicorns-unicorn-packages</name>
            <url>https://unicorns-123456789012.d.codeartifact.us-east-2.amazonaws.com/maven/unicorn-packages/</url>
            <mirrorOf>*</mirrorOf>
        </mirror>
    </mirrors>
</settings>
```

### Prueba a través de Cloud9
1. Verificar si la aplicación se puede compilar con éxito localmente en Cloud9 usando el archivo de configuración:

```
mvn -s settings.xml compile
```

2. Si la compilación fue exitosa, regresar a la consola de CodeArtifact y actualizar la página del repositorio. Ahora debería ver los paquetes que se usaron durante la compilación en el repositorio de artefactos. Esto significa que se descargaron del repositorio público y ahora están disponibles como una copia dentro de CodeArtifact

### Política de IAM para consumir CodeArtifact
> Antes de pasar a la siguiente tarea, definamos una política de IAM para que otros servicios puedan consumir nuestro repositorio de CodeArtifact recién creado.

1. Dirigirse al servicio de IAM
2. Hacer clic en Políticas en el menú de la izquierda
3. Hacer clic en Crear política y seleccionar la pestaña JSON en la parte superior para ver el código JSON sin procesar de la política de IAM, luego copiar y pegar el código de política a continuación. Esto asegurará que otros servicios como CodeBuild puedan leer los paquetes en el repositorio de CodeArtifact

```
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Action": [ "codeartifact:GetAuthorizationToken",
                      "codeartifact:GetRepositoryEndpoint",
                      "codeartifact:ReadFromRepository"
                      ],
          "Resource": "*"
      },
      {
          "Effect": "Allow",
          "Action": "sts:GetServiceBearerToken",
          "Resource": "*",
          "Condition": {
              "StringEquals": {
                  "sts:AWSServiceName": "codeartifact.amazonaws.com"
              }
          }
      }
  ]
}
```

4. Hacer clic en Siguiente: Etiquetas y Siguiente: Revisión

5. Nombrar la política como: ``` codeartifact-lab-consumer-policy ``` y proporcionar una descripción significativa como ``` Proporciona permisos para leer de CodeArtifact ```

6. Hacer clic en Crear política

> Ahora tenemos nuestros repositorios de trabajo que pueden ser consumidos por otros servicios. A continuación, necesitamos una forma de compilar nuestro código desde AWS para producir nuestro archivo WAR de Java.

### Tarea 4
### AWS CodeBuild
> AWS CodeBuild es un servicio de integración continua completamente administrado que se encarga de compilar el código fuente, ejecutar pruebas y generar paquetes de software listos para ser implementados. Puede empezar rápidamente utilizando entornos de compilación predefinidos o crear sus propios entornos de compilación personalizados que utilicen sus propias herramientas de compilación.

> En este paso, nos enfocaremos en configurar un proyecto de CodeBuild para empaquetar el código de la aplicación en un archivo WAR de Java.

### Crear un bucket de S3
> Primero necesitamos crear un bucket S3 que se usará para almacenar la salida de CodeBuild, es decir, del archivo WAR.

1. Dirigirse al servicio de Amazon S3
2. Hacer clic en Crear Bucket y asignarle un nombre único
3. Dejar todas las demás opciones como predeterminadas y hacer clic en Crear bucket

### Crear un proyecto de compilación de CodeBuild
1. Dirigirse al servicio de AWS CodeBuild
2. En proyectos de compilación, seleccionar Crear proyecto de compilación
3. Nombrar el proyecto como lab-web-build y establecer una descripción útil. Debajo de 4. Configuración adicional, agregar una etiqueta con clave y valor
4. En origen, seleccionar AWS CodeCommit como proveedor de origen y seleccionar el proyecto web como repositorio. La rama debe ser main sin ID de CodeCommit
5. En Entorno, seleccionar usar una imagen administrada y establecer lo siguiente:

---
#### **Recurso**	 **Estado Final**
---
#### **Sistema operativo** 	*Seleccionar Amazon Linux 2*
---
#### **Tiempo de ejecución**  *Seleccionar Estándar*
---
#### **Imagen**	*Seleccionar  aws/codebuild/amazonlinux2-x86_64-standard:3.0*
---
#### **Versión de imagen** *Utilizar siempre la imagen más reciente para esta versión de tiempo de ejecución*
---
#### **Tipo de entorno**  *Seleccionar Linux*
---

6. Seleccionar Crear un nuevo rol de servicio y dejar el nombre del rol como predeterminado
7. En Buildspec, dejar la opción predeterminada para Usar un archivo buildspec que buscará un archivo de configuración llamado buildspec.yml (lo crearemos más adelante)
8. En Artefactos, seleccionar Amazon S3 y seleccionar el nombre del bucket creado anteriormente. Establecer el nombre en lab-web-build.zip. Dejar las otras opciones como predeterminadas, asegurándose de que el empaquetado del artefacto esté configurado en Zip
9. Finalmente, en Registros, habilitar los registros de CloudWatch si aún no está habilitado. Establecer el nombre del grupo como lab-build-logs y el nombre de la transmisión como webapp. Esto nos permitirá realizar un seguimiento del resultado de la compilación en CloudWatch Logs
10. Hacer clic en Crear proyecto de compilación

### Crear el archivo buildspec.yml
> Ahora que tenemos la configuración del proyecto de compilación, debemos darle algunas instrucciones sobre cómo compilar la aplicación. Para ello crearemos un archivo buildspec.yml (YAML) en la raíz del repositorio de código.

1. Regresar al IDE de Cloud9
2. En la carpeta ~/environment/LAB-web-project/ crear un nuevo archivo llamado buildspec.yml (el nombre debe ser exacto) y copiar el contenido a continuación. Asegurarse de reemplazar el ID de cuenta del propietario del dominio con su propio ID de cuenta

```
version: 0.2

phases:
  install:
    runtime-versions:
      java: corretto8
  pre_build:
    commands:
      - echo Initializing environment
      - export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain unicorns --domain-owner 123456789012 --query authorizationToken --output text`
  build:
    commands:
      - echo Build started on `date`
      - mvn -s settings.xml compile
  post_build:
    commands:
      - echo Build completed on `date`
      - mvn -s settings.xml package
artifacts:
  files:
    - target/unicorn-web-project.war
  discard-paths: no

```

3. Guardar el archivo buildspec.yml. Luego confirmar y enviar a CodeCommit

```
cd ~/environment/lab-web-project
git add *
git commit -m "Adding buildspec.yml file"
git push -u origin main
```

### Modificar el rol de IAM
> Como usamos CodeArtifact durante la fase de compilación, se requiere un pequeño cambio en el rol de IAM generado automáticamente para garantizar que tenga permisos para usar CodeArtifact. Para esto, usaremos la política de IAM que se creó en la tarea anterior.

1. Dirigirse al servicio de IAM
2. Hacer clic en ```Roles``` en el menú de la izquierda
3. Buscar ```codebuild-lab-web-build-service-role``` para ubicar el rol generado automáticamente y hacer clic en él
4. Hacer clic en el botón ```Agregar permisos``` y seleccionar ```Adjuntar políticas``` en el menú desplegable
5. Buscar ```codeartifact-lab-consumer-policy```, seleccionar el elemento y hacer clic en ```Adjuntar políticas```

### Probar el proyecto de compilación
> Ahora tenemos todo listo para ejecutar nuestra primera compilación con CodeBuild.

1. Dirigirse al servicio de CodeBuild
2. Seleccionar el proyecto ```lab-web-build``` y seleccionar Start build > Start now
3.Supervisar los registros y esperar a que se complete el estado de compilación (esto no debería demorar más de 5 minutos):
4. Finalmente, navegar hasta el bucket S3 de artefactos para verificar que tiene un archivo WAR empaquetado dentro de un zip llamado ```lab-web-project.zip```

> Ahora tenemos un repositorio de código y artefactos, y una solución para compilar nuestra aplicación. Es una compilación activada manualmente en este momento que se solucionará más adelante. Pero al menos sabemos que nuestras compilaciones se completan de manera consistente.

### Tarea 5
### AWS CodeDeploy
> AWS CodeDeploy es un servicio de implementación completamente gestionado que automatiza el proceso de despliegue de software en una amplia gama de servicios informáticos, incluyendo Amazon EC2, AWS Fargate, AWS Lambda y servicios locales. Con AWS CodeDeploy, puede automatizar las implementaciones de software, eliminando la necesidad de realizar operaciones manuales que pueden ser propensas a errores.

### Crear una instancia EC2
> Se utilizará el servicio de AWS CloudFormation para aprovisionar una VPC y una instancia EC2 para implementar la aplicación.

1. Dirigirse al servicio de AWS CloudFormation
2. Descargar la siguiente plantilla YAML de CloudFormation
3. En la consola de CloudFormation, hacer clic en Crear pila > con nuevos recursos (estándar)
4. Seleccionar Cargar un archivo de plantilla y hacer clic en Elegir archivo. Seleccionar el archivo yaml descargado y hacer clic en Siguiente
5. Nombrar la pila como lab-stack y proporcionar su dirección IP de ```http://checkip.amazonaws.com/``` en el formato ```1.2.3.4/32``` cuando se solicite. Hacer clic en Siguiente para aceptar todos los valores predeterminados restantes. Recordar marcar la casilla de verificación de recursos de IAM antes de hacer clic en Crear pila
Esperar a que se complete la pila. Esto no debería tomar más de 5 minutos
Dirigirse al servicio de Amazon EC2 y hacer clic en Instancias (en ejecución). Debería ver una instancia llamada ```UnicornStack::WebServer```

### Crear scripts para ejecutar la aplicación
> A continuación, debemos crear algunos scripts de bash en el repositorio de Git. CodeDeploy usa estos scripts para configurar e implementar la aplicación en la instancia EC2 de destino.

1. Regresar al IDE de Cloud9
2. Crear una nueva carpeta de scripts en ~/environment/lab-web-project/
3. Crear un archivo `install_dependencies.sh` en la carpeta de scripts y agregar las siguientes líneas:

```
#!/bin/bash
sudo yum install tomcat -y
sudo yum -y install httpd
sudo cat << EOF > /etc/httpd/conf.d/tomcat_manager.conf
<VirtualHost *:80>
    ServerAdmin root@localhost
    ServerName app.wildrydes.com
    DefaultType text/html
    ProxyRequests off
    ProxyPreserveHost On
    ProxyPass / http://localhost:8080/lab-web-project/
    ProxyPassReverse / http://localhost:8080/lab-web-project/
</VirtualHost>
EOF
```

4. Crear un archivo `start_server.sh` en la carpeta de scripts y agregar las siguientes líneas:

```
#!/bin/bash
sudo systemctl start tomcat.service
sudo systemctl enable tomcat.service
sudo systemctl start httpd.service
sudo systemctl enable httpd.service
```

5. Crear un archivo `stop_server.sh` en la carpeta de scripts y agregar las siguientes líneas:

```
#!/bin/bash
isExistApp="$(pgrep httpd)"
if [[ -n $isExistApp ]]; then
sudo systemctl stop httpd.service
fi
isExistApp="$(pgrep tomcat)"
if [[ -n $isExistApp ]]; then
sudo systemctl stop tomcat.service
fi
```
6. CodeDeploy usa un archivo de especificación de aplicación (AppSpec) en YAML para especificar qué acciones se deben realizar durante una implementación y para definir qué archivos del origen se colocan en el destino de destino. El archivo AppSpec debe llamarse `appspec.yml` y colocarse en el directorio raíz del código fuente. Crear un nuevo archivo appspec.yml en la carpeta `~/environment/lab-web-project/` y agregar las siguientes líneas:

```
version: 0.0
os: linux
files:
  - source: /target/lab-web-project.war
    destination: /usr/share/tomcat/webapps/
hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
      runas: root
  ApplicationStart:
    - location: scripts/start_server.sh
      timeout: 300
      runas: root
  ApplicationStop:
    - location: scripts/stop_server.sh
      timeout: 300
      runas: root
```

7. Para garantizar que la carpeta de scripts y el archivo `appspec.yml` recién agregados estén disponibles para CodeDeploy, debemos agregarlos al archivo zip que crea CodeBuild. Esto se hace modificando la sección de artefactos en `buildspec.yml` como se muestra a continuación:

```
phases:
  [..]

artifacts:
  files:
    - target/lab-web-project.war
    - appspec.yml
    - scripts/**/*
  discard-paths: no
```

8. Ahora confirmar todos los cambios en CodeCommit:

```
cd ~/environment/lab-web-project
git add *
git commit -m "Adding CodeDeploy files"
git push -u origin main
```

9. Iniciar sesión en CodeBuild Console y hacer clic en Iniciar compilación para ejecutar nuevamente el proyecto `lab-web-build`, que incluirá los artefactos recién agregados en el paquete zip

### Crear el rol de IAM del servicio de CodeBuild
> CodeDeploy requiere un rol de servicio para otorgarle permisos a la plataforma informática deseada. Para implementaciones EC2/on-premises, puede utilizar la política AWSCodeDeployRole administrada por AWS.

1. Dirigirse al servicio de IAM
2. Hacer clic en Funciones y luego hacer clic en Crear función
3. Seleccionar CodeDeploy como servicio y luego seleccionar CodeDeploy para el caso de uso. Hacer clic en Siguiente
4. Aceptar la política predeterminada de AWSCodeDeployRole. No olvidar echar un vistazo a los permisos que esto otorga
5. Hacer clic en Siguiente y nombre el rol LabCodeDeployRole. Hacer clic en Crear función para finalizar

### Tarea 6
### AWS CodePipeline
> AWS CodePipeline es un servicio de entrega continua completamente administrado que le permite automatizar sus pipelines de lanzamiento para realizar actualizaciones rápidas y confiables de su infraestructura y aplicaciones. Con CodePipeline, solo paga por los recursos que utiliza.

> En este paso, utilizamos CodePipeline para crear un pipeline automatizado utilizando los componentes previamente configurados de CodeCommit, CodeBuild y CodeDeploy. El pipeline se activará automáticamente cuando se realice una nueva confirmación en la rama principal de nuestro repositorio de Git.

### Crear la canalización
1. Dirigirse al servicio de CodePipeline
2. En Pipelines, hacer clic en Create pipeline
3. Ingresar lab-web-pipeline como el nombre de la canalización. Hacer clic en Crear un nuevo rol de servicio y usar el nombre generado automáticamente. Dejar otras configuraciones como predeterminadas y hacer clic en Siguiente
4. En el proveedor de origen, seleccionar AWS CodeCommit y seleccionar `lab-web-project` como repositorio. Establecer el nombre del main como principal . Dejar la opción de detección como Amazon CloudWatch Events y el formato del artefacto de salida como predeterminado de CodePipeline. Hacer clic en Siguiente
5. En la pantalla de la etapa de compilación, seleccionar AWS CodeBuild como proveedor de compilación y `lab-web-build` como nombre del proyecto. Dejar el tipo de compilación como compilación única. Hacer clic en Siguiente
6. En la pantalla de la etapa de implementación, seleccionar AWS CodeDeploy como proveedor de implementación y `lab-web-deploy` como nombre de la aplicación. Seleccionar `lab-web-deploy-group` como grupo de implementación. Hacer clic en Siguiente
7. Revisar la configuración de la canalización y hacer clic en Crear canalización. Una vez que haga clic en Crear, toda la canalización se ejecutará por primera vez. Asegurarse de que se complete con éxito (esto puede tardar unos minutos)

### Liberar un cambio
> Ahora tiene una canalización de CI/CD completamente administrada. Se va a probar si todo está funcionando.

1. Regresar a iniciar sesión en el entorno Cloud9
2. Actualizar el index.jsp con el siguiente html:

```
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <style>
    body{
        font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .site-header .title{
        background: url(images/wr-home-top.jpg) no-repeat top;
        background-size: cover;
        padding-bottom: 70.2753441802%;
        margin: 0;
        text-indent: -999em;
        position: relative;
    }
    .home-about {
        background: #f50856;
        color: #fff;
        padding: 5rem 0;
        text-align: center;
    }
    </style>
  <title>Wild Rydes</title>
</head>

<body>
    <header class="site-header">
        <h1 class="title">Wild Rydes</h1>
    </header>
    <section class="home-about">

        <h2 class="section-title">How Does This Work?</h2>
        <p class="content">
            In today's fast paced world, you've got places you need to be but not enough time in your jam packed schedule. Wouldn't it be nice if there were a transportation service that changed the way you get around daily? Introducing Wild Rydes, an innovative transportation service that helps people get to their destination faster and hassle-free. Getting started is as easy as tapping a button in our app.
        </p>
        <h2 class="section-title">Our Story</h2>
      <p class="content">
        Wild Rydes was started by a former hedge fund analyst and a software developer. The two long-time friends happened upon the Wild Rydes idea after attending a silent yoga retreat in Nevada. After gazing upon the majestic herds of unicorns prancing across a surreal Nevada sunset, they witnessed firsthand the poverty and unemployment endemic to that once proud race. Whether it was modern society's reliance on science over magic or not, we'll never know the cause of their Ozymandian downfall and fade to obscurity. Moved by empathy, romance, and free enterprise, they saw an opportunity to marry society's demand for faster, more flexible transportation to underutilized beasts of labor through an on-demand market making transportation app. Using the founders' respective expertise in animal husbandry and software engineering, Wild Rydes was formed and has since raised untold amounts of venture capital. Today, Wild Rydes has thousands of unicorns in its network fulfilling hundreds of rydes each day.
      </p>
    </section>


</body>
</html>
```

3. Descargar la imagen de fondo y guardarla en su máquina local. Luego crear una nueva carpeta de imágenes debajo de ```lab-web-project/src/main/webapp/images/``` y cargar el archivo a través de Cloud9 usando Archivo > Cargar archivo local...

4. Confirmar los cambios usando el siguiente comando:

```
cd ~/environment/lab-web-project/
git add *
git commit -m "Visual improvements to homepage"
git push -u origin main
```

5. Regresar a consultar en la consola de CodePipeline. La canalización debe activarse automáticamente mediante la inserción. Esperar a que la canalización se complete correctamente (esto no debería demorar más de 5 minutos)

6. Una vez finalizada la canalización, dirigirse a la dirección IP pública de EC2 `http://<ip-address>/` para ver los cambios

> Ahora tiene una canalización de CI/CD en funcionamiento que utiliza los servicios de código de AWS.

### Extendiendo el pipeline
> En esta sección de laboratorio, veremos cómo ampliar nuestra canalización de CodePipeline existente para incluir un paso de aprobación manual antes de la implementación en un servidor de producción.

### Actualizar la pila de CloudFormation
> Primero, actualizar nuestro stack de CloudFormation para incluir una instancia EC2 adicional que actuará como nuestro servidor de producción.

1. Dirigirse al servicio de AWS CloudFormation
2. Descargar la [plantilla YAML](https://static.us-east-1.prod.workshops.aws/public/550745d8-3d9f-48e3-ab2b-6dfe650928ab/static/ec2-cfn-cp-ext.yaml)
3. En la consola de CloudFormation, hacer clic en lab-stack y hacer clic en Actualizar
4. Hacer clic en Reemplazar plantilla actual y cargar el archivo descargado
5. Continuar con los siguientes pasos usando Siguiente hasta que llegue a la página Revisar
6. Confirmar los cambios de IAM y hacer clic en Actualizar pila. Esto tardará unos minutos en completarse

### Agregar un grupo de implementación de CodeDeploy adicional
> Ahora necesitamos agregar un grupo de implementación del servidor de producción en CodeDeploy.

1. Dirigirse a CodeDeploy
2. Hacer clic en Aplicaciones y dirigirse a la aplicación `lab-web-deploy`
3. En la pestaña de Grupos de implementación, hacer clic en Crear grupo de implementación
4. Configurar los siguientes ajustes:
---
#### **Recurso**	**Estado Final**
---
#### **Nombre del grupo de implementación**	*Ingresar lab-web-deploy-group-prod*
---
#### **Rol de servicio**	*Seleccionar LabCodeDeployRole*
---
#### **Tipo de implementación**	*Seleccionar In situ*
---
#### **Configuración del entorno**	*Seleccionar instancias de Amazon EC2*
---
#### **Grupo de etiquetas 1 Clave**	*Ingresar rol*
---
#### **Grupo de etiquetas 1 Valor**	*Ingresar webserverprd*
---
#### **Instale CodeDeploy Agent**	*Seleccionar ahora y programe actualizaciones (14 días)*
---
#### **Configuración del entorno**	*Seleccionar CodeDeployDefault.AllAtOnce*
---
#### **Equilibrador de carga	Desmarcar** *Habilitar el equilibrio de carga*
---

5. Hacer clic en Crear grupo de implementación

### Crear tema SNS
> Crearemos un tema de SNS que se usará para las aprobaciones manuales en la siguiente sección.

1. Dirigirse al servicio de SNS
2. En la barra de menú de la izquierda, hacer clic en Temas y luego hacer clic en Crear tema
3. Establecer el tipo en Estándar y el nombre en `lab-pipeline-notifications`. Dejar todo lo demás como predeterminado y hacer clic en Crear tema
4.En Suscripciones, hacer clic en Crear suscripción. Configurar el Protocolo para que sea Correo electrónico e ingresar su dirección de correo electrónico. Hacer clic en Crear suscripción
5. Iniciar sesión en los correos electrónicos, donde debe tener un correo electrónico con el asunto `Notificación de AWS - Confirmación de suscripción`. Hacer clic en el enlace para confirmar la suscripción

### Actualizar CodePipeline
> Ahora debemos agregar nuestro paso de aprobación manual y la implementación en el servidor web de producción.

1. Dirigirse al servicio de CodePipeline
2. Hacer clic en lab-web-pipeline y hacer clic en Editar (necesita ver los detalles del pipeline para ver el botón de edición)
3.En la etapa Implementar, hacer clic en Agregar etapa. Asignar el nombre Aprobación a la etapa y hacer clic en Agregar etapa
4. En la etapa Aprobación recién creada, hace clic en Agregar grupo de acción. Establecer el nombre de la acción en Aprobación de producción y el proveedor de la acción en Aprobación manual. Configurar el ARN del tema SNS para que sea `lab-pipeline-notifications` que creamos anteriormente. Dejar las otras opciones en blanco y hacer clic en Listo
5. Ahora agregar otra Etapa después de la aprobación denominada DeployProd
6. Agregar un grupo de acciones en esta etapa denominado DeployProd. Configurar el proveedor de acciones para que sea AWS CodeDeploy y el artefacto de entrada para que sea BuildArtifact. Para el nombre de la aplicación, seleccionar `lab-web-deploy` y `lab-web-deploy-prod` para el grupo de implementación
7. Hacer clic en Listo y luego hacer clic en Guardar para guardar los cambios en la canalización. Deberá hacer clic en Guardar nuevamente en la pantalla emergente

### Probar el nuevo pipeline

1. Hacer clic en lab-web-pipeline en la consola de CodePipeline
2. Hacer clic en Liberar cambio y hacer clic en Liberar
3. Esperar a que el pipeline llegue a la etapa de aprobación manual y luego revisar sus correos electrónicos para obtener un enlace de aprobación
> Nota:
También puede aprobar esto directamente en la Consola de AWS.

4. Hacer clic en Revisar en la etapa de aprobación y en el cuadro de revisión agregar algunos comentarios y hacer clic en Aprobar
5. Una vez aprobada, la canalización continuará en la etapa de `CodeDeploy` de producción después de unos segundos
6. Asegurarse de que la canalización se complete con éxito y luego verificar que la dirección IP pública `UnicornStack::WebServerProd` de la instancia EC2 esté ejecutando la aplicación web

> Enhorabuena, ha ampliado correctamente CodePipeline mediante una etapa de aprobación que separa las implementaciones de desarrollo y producción.

### Ejercicios adicionales
> En los laboratorios anteriores, se ha centrado en una aplicación web Java simple que se implementa directamente en una instancia EC2.

> Ahora se verá cómo modificar la canalización para crear una imagen de contenedor con CodeBuild y enviarla a Amazon Elastic Container Registry (ECR).

### Agregar archivos para la compilación de la ventana acoplable
> Primero, debemos agregar un Dockerfile que contendrá instrucciones sobre cómo construir nuestra imagen de contenedor.

1. Regresar a iniciar sesión en el IDE de Cloud9
2. Crear un nuevo archivo llamado Dockerfile en la carpeta ~/environment/lab-web-project/ y agregar las siguientes líneas:

```
FROM public.ecr.aws/bitnami/tomcat:9.0

COPY ./target/unicorn-web-project.war /usr/local/tomcat/webapps/ROOT.war
```
> Esta es una instalación muy simple ya que estamos usando la imagen Bitnami Apache Tomcat de la galería pública de Amazon ECR.

3. Crear un nuevo archivo llamado buildspec_docker.yml en la misma carpeta y agregar las siguientes líneas:

```
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
```

> ste nuevo archivo buildspec construirá la imagen de contenedor y la enviará a un repositorio de ECR.

4. Modificar el archivo buildspec.yml existente para incluir los archivos de artefactos adicionales (`Dockerfile` y `buildspec_docker.yml`). Este trabajo de CodeBuild se ejecutará antes que el trabajo de buildspec-docker, por lo que debemos pasar los archivos en sentido descendente

```
version: 0.2

phases:
  [..]

artifacts:
  files:
    - target/lab-web-project.war
    - appspec.yml
    - scripts/**/*
    - Dockerfile
    - buildspec_docker.yml
  discard-paths: no
```

5. Ahora confirmar los cambios en CodeCommit:

```
git add *
git commit -m "Adding container support"
git push -u origin main
```

### Crear un repositorio de Amazon ECR

> Necesitamos un lugar para almacenar las imágenes de nuestros contenedores y para eso usaremos *Amazon ECR (Elastic Container Registry)*.

1. Dirigirse al servicio de Elastic Container Registry
2. En Repositorios privados, hacer clic en Crear repositorio

> Nota:
si ve una página de inicio, hacer clic en Comenzar

3. Nombre el repositorio `lab-web-images` dejando las otras configuraciones como predeterminadas. Hacer clic en Crear repositorio

### Crear un nuevo proyecto de compilación de CodeBuild
> Ahora necesitamos crear un nuevo proyecto de CodeBuild que usará nuestro archivo buildspec_docker.yml para construir nuestra imagen de contenedor y enviarlo a ECR.

1. Dirigirse al servicio de CodeBuild
2. En Proyectos de compilación, seleccionar Crear proyecto de compilación
3. Configurar los siguientes ajustes de compilación: Configuración del proyecto

---
#### **Recurso**	**Estado Final**
---
#### **Nombre del proyecto**	*Ingresar `lab-web-build-container`*
---
#### **Descripción**	*Ingresar `Crear imagen de contenedor acoplable`*
---
### Fuente
---
#### **Recurso**	**Estado Final**
---
#### **Proveedor de origen**	*Seleccionar Amazon S3*
---
#### **Bucket**	Ingresar <nombre del bucket de su artefacto>
---
#### **Clave de objeto S3 o carpeta S3**	Seleccionar `lab-web-build.zip`
---

### Ambiente
---
#### **Recurso**	**Estado Final**
---
#### **Imagen del entorno**	Seleccionar Imagen gestionada
---
#### **Sistema operativo**	Seleccionar Amazon Linux 2
---
#### **Tiempo de ejecución**	Seleccionar Estándar
---
#### **Imagen**	Seleccionar aws/codebuild/amazonlinux2-x86_64-standard:3.0
---
#### **Versión de imagen**	Utilizar siempre la imagen más reciente para esta versión de tiempo de ejecución
---
#### **Tiempo de ejecución**	Seleccionar Linux
---
#### **Privilegiado**	Marcar para Habilitar el indicador (requerido para compilaciones de Docker)
---
#### **Rol de servicio**	Seleccionar Rol de servicio nuevo (deje el nombre como predeterminado)
---

> Variables de entorno de configuración adicionales:

- Nombre = `AWS_DEFAULT_REGION`; Valor = `<su-región, por ejemplo, eu-west-1>`
- Nombre = `AWS_ACCOUNT_ID`; Valor = `<su id de cuenta>`
- Nombre = `IMAGEN_REPO_NOMBRE`; Valor = `lab-web-images`
- Nombre = `IMAGEN_ETIQUETA`; Valor = `último`

> Especificaciones de compilación

- Nombre de especificación de compilación = buildspec_docker.yml

> Artefactos
- Tipo = *Sin artefactos*

> Registros
- Nombre del grupo = unicorn-build-logs
- Nombre de flujo = contenedor

4. Haga clic en Crear proyecto de compilación

### Establecer el permiso del rol de IAM del proyecto de compilación

> Antes de que podamos probar la compilación, primero debemos agregar algunos permisos adicionales al rol de IAM del proyecto de CodeBuild. Esto es para proporcionar permisos de CodeBuild para usar Amazon ECR.

1. Dirigirse al servicio de IAM
2. Seleccionar Roles en el menú de la izquierda
3. Buscar `codebuild-unicorn-web-build-container-service-role` para ubicar el rol generado automáticamente y hacer clic en él
4. Hacer clic en el botón Agregar permisos y seleccionar Crear política en línea en el menú desplegable
5. Hacer clic en la pestaña JSON e insertar el siguiente código de política:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:BatchCheckLayerAvailability",
                "ecr:CompleteLayerUpload",
                "ecr:GetAuthorizationToken",
                "ecr:InitiateLayerUpload",
                "ecr:PutImage",
                "ecr:UploadLayerPart"
            ],
            "Resource": "*"
        }
    ]
}
```

6. Hacer clic en Revisar política y asignar a la política el nombre UnicornECRPush. Luego confirmar los cambios con Crear política

### Probar el proyecto CodeBuild
> Antes de ejecutar la prueba, primero necesitamos una versión actualizada de nuestro artefacto en S3 que contenga el Dockerfile. Para hacer esto, volveremos a ejecutar el proyecto original `unicorn-web-build` para crear este archivo zip.

1. Dirigirse al servicio de CodeBuild
2. En Proyectos de compilación, seleccionar `lab-web-build` y seleccionar Iniciar compilación > Comenzar ahora y asegurarse de que la compilación se complete correctamente (debe tener un archivo zip en el bucket de artefactos S3 con la marca de tiempo más reciente)
3. Ahora regresar a Crear proyectos y seleccionar `lab-web-build-container` y hacer clic en Iniciar compilación > Comenzar ahora
4. Asegurarse de que la compilación se complete correctamente. Si navega hasta el repositorio `lab-web-build-container` con la consola de Amazon ECR, debería encontrar que ahora hay una imagen etiquetada como Latest

> Felicitaciones, ahora tiene una versión en contenedor de la aplicación Unicorn Wild Rydes lista para implementar en la plataforma de contenedores que elija. Por ejemplo, ahora puede configurar CodeDeploy para implementar en un clúster Fargate de Amazon ECS.

### Implementación sin servidor
> En esta sección de laboratorio, veremos cómo implementar aplicaciones sin servidor en AWS utilizando el modelo de aplicación sin servidor. CLI.

> El modelo de aplicación sin servidor (SAM) de AWS es un marco de código abierto para crear aplicaciones sin servidor. Proporciona sintaxis abreviada para expresar funciones, API, bases de datos y asignaciones de fuentes de eventos. Con solo unas pocas líneas por recurso, puede definir la aplicación que desea y modelarla usando YAML. Durante la implementación, SAM transforma y expande la sintaxis de SAM en la sintaxis de AWS CloudFormation, lo que le permite crear aplicaciones sin servidor más rápido.

> Usaremos el arranque de canalización sam incorporado funcionalidad para crear la siguiente canalización:

> La aplicación sin servidor que implementaremos es una API Gateway simple que activa una función Lambda

### Obtención de la configuración
> Para esta práctica de laboratorio, utilizaremos el entorno UnicornIDE Cloud9 existente que ya tiene la CLI de SAM instalada.

> Nota:
Si desea instalar SAM CLI en su propia máquina, en lugar de Cloud9, siga las instrucciones aquí.

### Creación de una aplicación sin servidor
> Con todo configurado, es hora de crear nuestra primera aplicación sin servidor.

1. Iniciar sesión en el entorno UnicornIDE Cloud9 creado anteriormente. En la terminal, ejecutar lo siguiente:
```
cd ~/environment/
sam init
```
> Seguir el proceso de inicialización guiada, especificando las siguientes opciones cuando se le solicite:

---
#### **Recurso**	**Estado Final**
---
#### **Plantilla**	*Seleccionar Plantillas de inicio rápido de AWS*
---
#### **Tipo de paquete**	*Seleccionar Cremallera*
---
#### **Tiempo de ejecución**	*Seleccionar Nodejs14.x*
---
#### **Nombre del proyecto**	*Ingresar lab-serverleess*
---
#### **Plantilla de inicio rápido**	*Seleccionar backend web*
---

> Esto creará una nueva aplicación web NodeJS sin servidor con plantilla con una API Gateway, una función Lambda y una tabla de DynamoDB. Tómese un momento para explorar los recursos creados, en particular el archivo `template.yml` , que contiene varios recursos sin servidor que se crearán.

### Cree el repositorio de Git para la aplicación sin servidor

1. Dirigirse al servicio de CodeCommit y crear un nuevo repositorio
2. Nombre el repositorio `serverless-unicorns`. Una vez creado, copiar la URL HTTPS
3. De vuelta en el IDE de Cloud9, inicializar el repositorio de Git:

```
cd ~/environment/serverless-unicorns
git init -b main
git remote add origin <HTTPS CodeCommit repo URL>
```

4. Hacer push en la nueva aplicación al repositorio ejecutando los siguientes comandos:

```
git add *
git commit -m "Initial commit"
git push -u origin main
```

### Implementación de la aplicación

> Ahora que tenemos nuestra aplicación web básica sin servidor, es hora de implementarla. En la terminal, ejecutar los siguientes comandos:
```
sam build
sam deploy --guided
```
> Siga el proceso de creación de pila guiada, ingresando las siguientes variables cuando se le solicite, reemplazando la región con la región en la que se está ejecutando el taller (por ejemplo, eu-west-1):
---
#### **Recurso**	**Estado Final**
---
#### **Nombre de la pila [sam-app]**	Ingresar lab-serverleess
---
#### **Región de AWS [us-east-1]**	Seleccionar la región de este laboratorio
---
#### **Confirmar cambios antes de implementar [Y/N]:**	Ingresar y
---
#### **Permitir la creación de roles de IAM de la CLI de SAM [Y/N]:**	Ingresar y
---
#### **Es posible que getAllItemsFunction no tenga definida la autorización. ¿Está bien? [Y/N]:**	Ingresar y
---
#### **Es posible que getByIdFunction no tenga definida la autorización. ¿Está bien [Y/N]:**	Ingresar y
---
#### **putItemFunction puede no tener definida la autorización, ¿Está bien [Y/N]:**	Ingresar y
---
#### **Guardar argumentos en el archivo de configuración [Y/N]:**	Ingresar y
---
#### **Archivo de configuración de SAM [samconfig.toml]**	Confirmar como predeterminado
---
#### **Entorno de configuración SAM [predeterminado]**	Confirmar como predeterminado
---

> Cuando se le pregunte si desea ¿Implementar este conjunto de cambios?, confirme con y . Esto luego implementará la plantilla de CloudFormation ampliada y aprovisionará los recursos subyacentes dentro de su cuenta de AWS (esto llevará unos minutos).

> Navegar a la consola de CloudFormation en la Consola de administración de AWS y verá que se ha creado la pila. Aquí puede ver los recursos creados por la implementación de SAM.

### Creando la canalización
> Esto es genial, pero no queremos que todos los desarrolladores tengan que empujar manualmente desde sus portátiles cada vez. Queremos crear una canalización de CI/CD centralizada que podamos invocar cuando se realicen cambios en nuestro repositorio de aplicaciones sin servidor.

> Afortunadamente, SAM tiene algunas herramientas integradas para ayudarnos con esto. Ahora usaremos la CLI de SAM para crear la canalización para AWS CodePipeline que implementará nuestra aplicación sin servidor.

1. En la terminal, ejecutar el siguiente comando:
```
sam pipeline init --bootstrap
```
2. Especificar los siguientes valores cuando lo solicite la inicialización guiada:

---
#### **Recurso**	**Estado Final**
---
#### **Plantilla**	Seleccionar Plantillas de canalización de inicio rápido de AWS
---
#### **Sistema CI/CD	**Seleccionar AWS CodePipeline
---
#### **[..] pasar por el proceso de configuración del escenario [..]?**	Ingresar y
---
#### **Nombre artístico**	Ingresar uat
---
#### **Origen de la credencial**	Seleccionar predeterminado (perfil con nombre)
---
#### **Región**	Seleccionar la región de este laboratorio
---
#### **Usuario de canalización**	Confirmar como predeterminado
---
#### **Rol de ejecución de canalización**	Confirmar como predeterminado
---
#### **Rol de ejecución de CloudFormation**	Confirmar como predeterminado
---
#### **Buckets de artefactos**	Confirmar como predeterminado
---
#### **¿Su aplicación contiene alguna función Lambda de tipo IMAGE? [s/n]:**	Confirmar como 
---

3. Presionar Enter para confirmar que todo se ve bien. Luego presionar Y para confirmar y continuar con la creación de los recursos

A continuación, se nos pedirá que creemos la segunda etapa. Confirmar con Y que desea volver a realizar el proceso de configuración del escenario. Repetir el proceso anterior nuevamente comenzando con el nombre de la etapa donde especifica prod . Los demás valores pueden permanecer igual que en la etapa anterior.

4. Cuando se le solicite el proveedor de Git, elija lo siguiente:
---
#### **Recurso**	**Estado Final**
---
#### **Proveedor Git**	Seleccionar CodeCommit
---
#### **Nombre del repositorio**	Ingresar lab-serverless
---
#### **Branch**	Seleccionar main
---
#### **Ruta del archivo de plantilla**	Seleccionar `template.yml`
---

> Para el siguiente mensaje, elija la etapa uat ( 1 ) e ingresar serverless-lab-uat como el nombre de la pila SAM. Luego seleccionar la etapa de producción ( 2 ) con el nombre serverless-lab-prod.

> SAM ahora creará el archivo de configuración de CodePipeline. Envíe los nuevos archivos de configuración al repositorio ejecutando los siguientes comandos:

```
git add .
git commit -m "Add CodePipeline config"
git push origin main
```

5. Ejecutar el siguiente comando para implementar la canalización en su cuenta de AWS. Confirmar con y cuando se le pregunte si implementar los cambios

```
sam deploy -t codepipeline.yaml --stack-name serverless-pipeline --capabilities=CAPABILITY_IAM
```

> Esto tomará un minuto para implementar la pila de CloudFormation y crear los recursos subyacentes. Una vez completado, navegue a la consola de CloudFormation donde notará tres nuevas pilas de CloudFormation que se han creado:

- pila de canalización sin servidor para los recursos de CI
- pila serverless-lab-uat para el entorno de prueba
- pila serverless-lab-prod para el entorno de producción

6. Abrir la consola de CodePipeline y vea que se ha creado una nueva canalización como implementación inicial de nuestro proyecto. Espere a que se complete esta canalización antes de continuar

> Probando la canalización

1. Regresar a navegar a CloudFormation. Seleccionar la pila serverless-lab-uat y hacer clic en la pestaña Recursos. Siga el enlace para ServerlessRestApi
2. Hacer clic en el recurso POST y hacer clic en Prueba
3. Pegar lo siguiente en el cuadro Cuerpo de la solicitud y presionar Probar:
```
{ "id": "1" }
```
4. Observar que se ha creado un nuevo recurso
5. Ahora intente lo mismo con el método GET y vea que se devuelve nuestra identificación
6. Ahora haremos un cambio localmente y lo implementaremos para ver nuestro CI/CD en acción
7. Abrir el archivo get-all-items.js y buscar la siguiente línea de JavaScript:
```
const items = data.Items;
```
8. Reemplazar esto con lo siguiente:
```
const items = data.Items;
items.push({ "unicorns-enabled": true });
```
9. Guardar y cerrar el archivo. Luego confirmar y enviar nuestros cambios al origen:
```
git add .
git commit -m "Add unicorn power"
git push origin main
```
10. Dirigirse a la consola de CodePipeline. Después de unos momentos, verá una nueva canalización en ejecución para nuestros cambios
11. Hacer clic para ver la canalización a medida que se ejecuta. Una vez que se haya completado, regresar a la consola de API Gateway
12. Regresar a probar el método GET en la API para ver que nuestros cambios se implementaron correctamente. ¡Ahora nuestro microservicio sin servidor tiene poder de unicornio!