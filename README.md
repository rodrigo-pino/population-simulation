# Simulación

## Eventos Discretos

**Rodrigo Daniel Pino Trueba C412** 



### Resolución del Ejercicio 6

#### Principales ideas seguidas para la solución del problema

En este problema se dan unas tablas que indican los eventos a ejecutar y las probabilidades que estos se cumplan, no obstante no queda claro cuando dichos eventos se ejecuten. La idea a seguir fue realizar una maquina de estado para cada persona que se mueve probabilísticamente en una dirección o hacia otra. Para moverse hacia un estado la persona se somete a un evento asociado con dicho estado, en el caso de cumplirlo se realiza la transición, en caso negativo se programa otro intento de transición más adelante en el tiempo. Lo anterior dicho aplicado a nuestra problema desemboca en los siguientes eventos:

* **Desear Pareja:** Este evento se aplica a todas las personas mayores de 12 años. El cumplimiento de este evento implica que hubo una transición satisfactoria y que la persona actual desea pareja. Se le programa entonces el evento Emparejarse. En caso contrario, la persona no desea pareja y el evento se le es programado nuevamente.
* **Emparejarse:** El cumplimiento de este evento implica la formación de una nueva pareja, a la mujer se le programa el evento Embarazarse y el evento Ruptura para más adelante en el tiempo. Sólo es asignado Ruptura a la mujer, pues en caso de asignárselo también al hombre, la pareja estaría sujeta a 2 eventos de este tipo, en vez de uno sólo.  El no cumplimiento de este evento implica la reprogramación de Emparejarse para más adelante en el tiempo.
* **Ruptura:** En el caso de Ruptura, la pareja se separa y se les pasa a programar a ambos miembros el evento Desear Pareja tras un tiempo de espera determinado por la ruptura en si. En caso contrario, se re-programa otro evento Ruptura para la mujer de la pareja más adelante en el tiempo.
* **Embarazarse:** Cuando ocurre el embarazo se crea el evento Parir a los 9 meses donde se simula el ocurrimiento del parto y se añaden los nuevos mini-pobladores a la simulación. En caso contrario a la mujer se le vuelve a programar el evento Embarazarse.
* **Parir:** El evento se explica por sí solo. La población incrementa, y se calcula si los niños envejecen o mueren (_explicado más adelante_). Este evento nunca falla. Si en el momento del parto la mujer tiene una pareja y este es el padre de sus hijos se programa un evento Embarazarse para la mujer más adelante en el tiempo.

El momento exacto en el que una persona va a intentar cumplir un evento se calcula utilizando una variable uniforme en un rango [a, b], donde a es el tiempo mínimo en meses y b el tiempo máximo. Cada evento tiene su rango específico, el de desear parjea, por ejemplo, está en el rango de 1 a 6 meses. Este y los otros rangos se pueden configurar a en _src/config.py_.

Mientras un poblador transita por sus estados utilizando los eventos dichos previamente, este va envejeciendo a lo largo del tiempo hasta morir. Envejecer no afecta de manera directa a la simulación, excepto por cambiar las probabilidades a las que se someten las personas debido al aumento de edad, en cambio Morir signifca el fin de esa persona en la simulación. Como a ojos de la simulación la edad exacta de una persona no es importante, sino el rango entre el cual se encuentra, se definen las etapas (de 0 a 12 años, 12 a 15 años, ... y de 76 a 125 años). El evento Envejecer solo se ejecuta una vez por cada una de estas etapas. 

* **Envejecer:** Este evento siempre se cumple e implica el crecimiento de dicha persona. Si la persona recién llega a los 12 años se le programa el evento **Desear Pareja** (_así se garantiza que todos los individuos entren dentro del ciclo Desear Pareja, Emparejarse, etc..._).  Luego se decide dado la edad de la persona y una variable aleatoria uniforme, si esta muere, o logra envejecer hasta la próxima etapa. En el caso de que envejezca, se le pronostica otro evento Envejecer para años más adelante. En caso contrario se le pronostica el evento Morir.
* **Morir:** Este evento siempre se cumple e implica el fin de la persona en la simulación y la transición al estado final de la máquina de estados.

Programar un evento a futuro implica añadirlo a una lista ordenada, donde se sitúan de menor a mayor los eventos de acuerdo su tiempo de ejecución. La simulación avanza ejecutando siempre el evento más cercano en el tiempo, y utiliza la fecha de dicho evento para avanzar el tiempo global hasta ese momento. La unidad base en que medimos el tiempo para este simulación es el _mes._ La simulación se detiene una vez llegado el límite de tiempo o cuando no quedan eventos pronosticados. El tiempo por defecto de la duración de la simulación es de 100 años y se puede editar en _src/config.py_. 

La máquina de estado de una persona durante una simulación con todas sus posibles transiciones:

![](./diagram.png)

#### Modelo

Variable de tiempo $t$. Indica el estado actual de la simulación.

Variables contadoras (en funcion de la variable tiempo $t$):

* $N_{d}$ La cantidad de personas que han deseado pareja.
* $N_p$ La cantidad de parejas formada.
* $N_r$ La cantidad de rupturas ocurridas.
* $N_e$ La cantidad de embarazos ocurridos.
* $N_n$ La cantidad de partos ocurridos.
* $N_v$ La cantidad de enviudamientos que han ocurrido.

Variables de estado del sistema:

* $m$ y $f$  señalan la cantidad de mujeres y hombres respectivamente que se encuentran dentro de la simulación.

* Para las personas en general

  * $a_i$ edad de la persona $i$

  * $d_i$ si la persona $i$ desea pareja o no.

  - $p_i$ si la persona $i$ tiene pareja o no.
  - $m_i$ la cantidad máxima deseada de hijos de la persona $i$.
  - $h_i$ número de hijos de la persona $i$.

* Para las mujeres en específico:
  * $e_i$ indica si la mujer $i$ esta embarazada o no.
  * $q_i$ señala la pareja que embarazó a la mujer, que no necesariamente tiene que ser la pareja actual.  

Variables de entrada $f$ y $m$ que indican la cantidad inicial de mujeres y hombres.

Variables de salida: $f$, $m$ y todas las variables contadoras.

**Inicialización**

```
t = 0
m = input(), f = input()
for i in m + f:
	# Se inicializan a todas las personas y 
	# se les añade el evento envejecer
	init_person:
		a_i = uniform(0, 100)*12
		d_i = False
		p_i = false
		m_i = generate_max_kids()
		h_i = 0
	if woman:
		e_i = 0
		q_i = None
	person.grow_old

for i in m + f:
	if e_i >= 12*12:
		# Las personas mayores de 12 años se les programa
		# desear pareja
		person_i.wants_partner()
```

A partir de esta inicialización los demás eventos se generan dinámicamente, como se explica en **Principales Ideas Seguidas**

#### Consideraciones Obtenidas

El modelo fue ejecutado múltiples veces y en todos los casos con una cantidad suficiente e igual de mujeres y hombres se observó que en el transcurso de los 100 años la población decrecía a 1/3 o 1/2 de la población total. Estos resultados tienen sentido pues lo más probable es que cada pareja tenga entre 1 o 2 hijos, que serían los remplazos de sus puedras cuando estos fallezcan. Luego como por regla la población tiene una mayor tendencia a mantenerse o decrecer a lo largo del tiempo. Cuando se simula con el número de hijos fijo y mayor que 2 la población a lo largo del tiempo tiende a crecer.

Cuando se ejecuta con un numero pequeño de personas los resultados terminan siendo erráticos y poco predecibles.

Cuando se ejecuta con una cantidad muy dispar de hombres y mujeres termina en una población que no logra mantener sus números durante el paso del tiempo y decrece rápidamente. 

### Ejecutar

El proyecto fue implementado y probado con _Python 3.9_, se aconseja esta versión, o una superior para su ejecución. Es necesario además tener instalad la biblioteca SortedContainers.

```bash
pip install sortedcontainers
```

Luego para correr la simulación:

```bash
cd src
python main.py <h> <f>
```

Donde _h_ y _f_ son la cantidad de hombres y mujeres iniciales.

#### Poetry

Es posible crear el ambiente si se tiene _poetry_ con los siguientes comandos:

```bash
poetry install
```

Luego para ejecutar:

```bash
cd src
poetry shell
python main.py <h> <f>
```

#### Configurar

En _src/config.py_ se encuentran definidas varias constantes con las que funciona el sistema, estas sirven como parametros de la simulación y condicionan su funcionamiento.

```python
# config.py

# Determina el fin de la simulacion
SIMULATION_END = 100 * 12
# Los rangos de edades de las personas
AGE_RANK = [i * 12 for i in [12, 15, 21, 35, 45, 60, 125, 200]]

# Los rangos en el tiempo en los que se programan los eventos 
PARTNER_RANGE = (1, 3) # de 1 a 3 mesees en adelante
WANT_PARTNER_RANGE = (1, 12) # de 1 a 12 meses en adelante
BREAK_UP_RANGE = (6, 18)
PREGNANT_RANGE = (1, 6)
# Caso especial cuando una mujer tiene un embarazo con exito, espera un
# tiempo mayor antes de embarazarse de nuevo
PREGNANT_REST_RANGE = (3, 12)wan
```
