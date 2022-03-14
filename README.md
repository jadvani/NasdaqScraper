# Nasdaq Website Scraper

NASDAQ (National Association of Securities Dealers Automated Quotation) es el segundo mercado de valores
y bolsa de valores automatizada y electrónica más grande de los Estados Unidos, siendo la primera la Bolsa de Nueva York, 
con más de 3800 compañías y corporaciones. Tiene más volumen de intercambio por hora que cualquier otra bolsa de valores en el mundo. 
Más de 7000 acciones de pequeña y mediana capitalización cotizan en la NASDAQ. Se caracteriza por comprender las empresas 
de alta tecnología en electrónica, informática, telecomunicaciones, biotecnología, y muchas otras más.

![Resume Preview](https://github.com/jadvani/NasdaqScrapper/blob/main/img/readme_nasdaq.jpg)

## Objetivo

Conocer los valores de acciones a tiempo real puede resultar crucial para decidir qué hacer con el capital invertido, por lo que 
la extracción automática del valor de la(s) empresa(s), sin necesidad de acudir al sitio web, así como la posterior manipulación
para arrojar predicciones, son herramientas complementarias que pueden ayudar al inversor. 

*DISCLAIMER: Este trabajo se trata de una actividad académica para la asignatura de Topología y Ciclo de Vida de los Datos, para el master de Ciencias de Datos de la UOC.*

El conjunto de funciones presentadas en este repositorio, elaboradas con Python 3.10, tienen como objetivo dos puntos principales:

* Obtener el listado actualizado de símbolos (identificador unívoco) de empresas. 
* A partir del símbolo o listado de símbolos, obtener distintos parámetros relevantes para determinar el estado de la empresa.

El listado de símbolos de empresas completo a 13 de marzo de 2022 se ha guardado en ```execution_results/symbols.txt```.

Los detalles de cada empresa del listado que se desee ejecutar se guardan en un CSV con el timestamp de ejecución, dentro del mismo directorio ```execution_results/```

## Dependencias

Aunque se ha extraído un **requirements.txt** usando ```pip freeze```, listando todas las dependencias instaladas en la máquina utilizada, 
las que realmente atañen al código son las siguientes:
```
PyYAML==5.3.1
selenium==4.1.0
pandas==1.0.5
logging==0.5.1.2
```
## Obtención de CSV

La forma más sencilla de obtener un CSV, es ejecutando el script```generate_dataset.py```.

Cabe destacar que, para obtener de nuevo todos los símbolos de empresas, es necesario descomentar 
las líneas del código 3, 8 y 9 de ```generate_dataset.py```, que se encargan de escrapear nuevamente la tabla que contiene todo el listado. 

Todos esos símbolos se almacenan en ```symbols.txt```, y es un proceso que toma unos 6 minutos. 

Si en su lugar deseamos obtener los datos de tan sólo algunos símbolos, podemos generar un ```symbols.txt``` diferente, siguiendo la estructura 
del fichero con aquellas (una lista de strings guardada literalmente en el fichero):

```['AAPL', 'APPN', 'DIS']```

Para simplificar y optimizar el tiempo de ejecución, se ha dejado en el script la obtención de los 5 primeros símbolos de todo el listado completo, 
pues cada símbolo se escrapea en unos 3 segundos. En el directorio ```execution_results``` se muestran CSVs con un mayor número de entradas. 

En ocasiones, algunas empresas no tenían los datos presentes, o estaban incompletos, probablemente porque se están actualizando en ese momento. Esto hace que el scrapper obtenga las líneas mal o salten excepciones, que se han tratado debidamente con sentencias ```try - except```

![Resume Preview](https://github.com/jadvani/NasdaqScrapper/blob/main/img/data_not_available.jpg)

Los campos del CSV resultante son los siguientes:

* symbol: El símbolo de la compañía. 
* name: El nombre completo.
* price: Precio de cada acción en el momento de ejecución.
* pricing_changes: Variación en dólares del precio en las últimas 24h.
* pricing_percentage_changes: Variación en % del precio en las últimas 24h.
* sector: Sector al que pertenece (Ejemplos: Technology, Consumer Services, Finance, ...)
* industry: Industria del sector (Ejemplo: Computer Manufacturing)
* market_cap: Capitalización total de la empresa, su valor total, en dólares.
* share_volume: Volumen de acciones. Son la cantidad de acciones que se han negociado en las últimas 24 horas.
* earnings_per_share: El beneficio por acción, lo que ha aportado en el periodo de un año.
* annualized_dividend: Utiliza el último dividendo pagado multiplicado por la frecuencia. Es el importe de un dividendo pagado a los accionistas en cuatro trimestres. 
* dividend_pay_date: Fecha de pago de los últimos dividendos.
* symbol_yield: El rendimiento de la acción es la apreciación del precio de la acción más los dividendos pagados, dividido por el precio original de la acción.
* beta: La beta es una forma de medir la volatilidad de una acción en comparación con la volatilidad del mercado en general. El mercado en su conjunto tiene una beta de 1. Los valores con un valor superior a 1 son más volátiles que el mercado (lo que significa que generalmente subirán más de lo que sube el mercado y bajarán más de lo que baja el mercado)
