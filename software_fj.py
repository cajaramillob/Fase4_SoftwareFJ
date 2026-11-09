"""Ingeniería de Sistema
Curso de PROGRAMACIÓN
Grupo 213023_139
Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y
Reservas
Trabajo colaborativo uso de GitHub
Autores:
ANDRES FELIPE SUAREZ VALENCIA
CARLOS ANDRES JARAMILLO BRITTO"""

# Importamos Tkinter para la interfaz gráfica
import tkinter as tk
from tkinter import messagebox, ttk
import os
from pathlib import Path

# ABC permite crear clases abstractas y métodos abstractos
from abc import ABC, abstractmethod

# datetime permite trabajar con fechas y horas
from datetime import datetime

# logging permite registrar eventos y errores en un archivo de registro
import logging

# re nos permite la validación de formatos de datos, como fechas, emails, etc.
import re

# Configuración del registro de eventos y errores
# Obtener la carpeta donde está guardado este programa
CARPETA_PROYECTO = Path(__file__).resolve().parent

# Definir la ubicación del archivo de registros
ARCHIVO_LOG = CARPETA_PROYECTO / "logs_software_fj.log"

# Configurar el sistema de registros
logging.basicConfig(
    filename=str(ARCHIVO_LOG),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


# Función para registro de eventos importantes
def registrar_evento(mensaje):
    logging.info(mensaje)


# Función para registro de errores del sistema
def registrar_error(mensaje):
    logging.error(mensaje)


"""CONTROL DE PRUEBAS DEL SISTEMA
Esta función permitirá que el sistema guarde información de cada prueba:
- Nombre de la prueba.- Si fue exitosa o fallida.- Detalle del resultado."""

# Lista para almacenar los resultados de las pruebas
resultados_pruebas = []


def registrar_resultado_prueba(nombre, exitosa, detalle=""):

    # Crear el resultado de la prueba
    resultado = {"nombre": nombre, "exitosa": exitosa, "detalle": detalle}

    # Guardar el resultado en la lista
    resultados_pruebas.append(resultado)

    # Registrar el resultado en el archivo de logs
    if exitosa:
        registrar_evento(f"Prueba exitosa: {nombre}")
    else:
        registrar_error(f"Prueba fallida: {nombre} - {detalle}")


# RESUMEN DE PRUEBAS DEL SISTEMA


def obtener_resumen_pruebas():

    # Contar el total de pruebas
    total = len(resultados_pruebas)

    # Contar las pruebas exitosas
    exitosas = sum(1 for prueba in resultados_pruebas if prueba["exitosa"])

    # Calcular las pruebas fallidas
    fallidas = total - exitosas

    # Construir el resumen
    return {"total": total, "exitosas": exitosas, "fallidas": fallidas}


# CONSULTAR DETALLE DE LAS PRUEBAS


def listar_resultados_pruebas():

    # Recorrer todos los resultados registrados
    for prueba in resultados_pruebas:

        # Determinar el estado de la prueba
        estado = "EXITOSA" if prueba["exitosa"] else "FALLIDA"

        # Mostrar información
        print(f"\nPrueba: {prueba['nombre']}")
        print(f"Estado: {estado}")
        print(f"Detalle: {prueba['detalle']}")


# EXCEPCIONES PERSONALIZADAS


class ErrorSistema(Exception):
    pass


class DatosInvalidosError(ErrorSistema):
    pass


class RegistroDuplicadoError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class OperacionReservaError(ErrorSistema):
    pass


# CLASE ABSTRACTA: ENTIDAD


class Entidad(ABC):

    # Constructor de la clase
    def __init__(self, identificador):

        # Validar que el identificador no esté vacío
        if not identificador or not str(identificador).strip():
            raise DatosInvalidosError("El identificador es obligatorio.")

        # Guardar el identificador como atributo protegido
        self._identificador = str(identificador).strip()

    # Propiedad para consultar el identificador
    @property
    def identificador(self):
        return self._identificador

    # Método abstracto que las clases hijas deben implementar
    @abstractmethod
    def obtener_resumen(self):
        pass


# CLASE CLIENTE


class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):

        # Inicializar los atributos heredados de Entidad
        super().__init__(identificador)

        # Asignar los datos utilizando sus propiedades
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # PROPIEDAD: NOMBRE

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):

        if not valor or not valor.strip():
            raise DatosInvalidosError("El nombre del cliente es obligatorio.")

        self.__nombre = valor.strip()

    # PROPIEDAD: CORREO

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):

        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(patron, valor):
            raise DatosInvalidosError("El correo electrónico no es válido.")

        self.__correo = valor.strip()

    # PROPIEDAD: TELEFONO

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):

        # Permitir números, espacios, guiones y el signo +
        if not re.fullmatch(r"[0-9+\-\s]+", valor):
            raise DatosInvalidosError("El teléfono contiene caracteres no permitidos.")

        # Comprobar que tenga entre 7 y 15 dígitos
        cantidad_digitos = sum(caracter.isdigit() for caracter in valor)

        if cantidad_digitos < 7 or cantidad_digitos > 15:
            raise DatosInvalidosError("El teléfono debe tener entre 7 y 15 dígitos.")

        self.__telefono = valor.strip()

    # MÉTODO ABSTRACTO HEREDADO

    def obtener_resumen(self):

        return (
            f"Cliente: {self.nombre} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )


# CLASE ABSTRACTA: SERVICIO


class Servicio(Entidad):

    # Constructor de la clase
    def __init__(self, identificador, nombre, tarifa_base):

        # Inicializar los atributos heredados
        super().__init__(identificador)

        # Validar el nombre del servicio
        if not nombre or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")

        # Validar la tarifa base
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError(
                "La tarifa base debe ser un número mayor que cero."
            )

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)

    # PROPIEDAD: NOMBRE

    @property
    def nombre(self):
        return self._nombre

    # PROPIEDAD: TARIFA BASE

    @property
    def tarifa_base(self):
        return self._tarifa_base

    # MÉTODOS ABSTRACTOS

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs):
        pass

    @abstractmethod
    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):
        pass

    # IMPLEMENTACIÓN DEL MÉTODO HEREDADO

    def obtener_resumen(self):
        return self.describir()


# SERVICIO ESPECIALIZADO # 1 --> RESERVA DE SALAS, se aplica herencia


class ReservaSala(Servicio):

    # Constructor de la clase
    def __init__(self, identificador, nombre, tarifa_base, capacidad_maxima):

        # Inicializar los atributos de Servicio
        super().__init__(identificador, nombre, tarifa_base)

        # Validar la capacidad máxima
        if not isinstance(capacidad_maxima, int) or capacidad_maxima <= 0:
            raise DatosInvalidosError(
                "La capacidad máxima debe ser un entero mayor que cero."
            )

        self._capacidad_maxima = capacidad_maxima

    # PROPIEDAD: CAPACIDAD MAXIMA

    @property
    def capacidad_maxima(self):
        return self._capacidad_maxima

    # DESCRIPCION DEL SERVICIO, aqui se realiza la sobreescritura de métodos (POLIMORFISMO)

    def describir(self):

        return (
            f"Sala: {self.nombre} | "
            f"Tarifa por hora: ${self.tarifa_base:,.0f} | "
            f"Capacidad máxima: {self.capacidad_maxima} personas"
        )

    # VALIDAR PARAMETROS DE LA RESERVA

    def validar_parametros(self, **kwargs):

        horas = kwargs.get("horas")
        personas = kwargs.get("personas")

        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or horas <= 0:
            raise DatosInvalidosError("La cantidad de horas debe ser mayor que cero.")

        if not isinstance(personas, int) or isinstance(personas, bool):
            raise DatosInvalidosError(
                "La cantidad de personas debe ser un número entero."
            )

        if personas <= 0 or personas > self.capacidad_maxima:
            raise DatosInvalidosError(
                "La cantidad de personas supera la capacidad de la sala."
            )

        return True

    # CALCULAR COSTO DEL SERVICIO

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):

        # Validar la cantidad de horas
        self.validar_parametros(horas=cantidad, personas=1)

        # Validar impuesto y descuento
        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise DatosInvalidosError(
                "El impuesto y el descuento deben estar entre 0 y 100."
            )

        # Calcular el valor inicial
        subtotal = self.tarifa_base * cantidad

        # Aplicar descuento
        valor_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - valor_descuento

        # Aplicar impuesto
        valor_impuesto = subtotal_con_descuento * (impuesto / 100)

        # Calcular valor final
        total = subtotal_con_descuento + valor_impuesto

        return total


# SERVICIO ESPECIALIZADO # 2 -->  ALQUILER DE EQUIPOS, se aplica herencia


class AlquilerEquipo(Servicio):

    # Constructor de la clase
    def __init__(self, identificador, nombre, tarifa_base, unidades_disponibles):

        # Inicializar los atributos heredados
        super().__init__(identificador, nombre, tarifa_base)

        # Validar las unidades disponibles
        if (
            not isinstance(unidades_disponibles, int)
            or isinstance(unidades_disponibles, bool)
            or unidades_disponibles < 0
        ):
            raise DatosInvalidosError(
                "Las unidades disponibles deben ser un entero igual o mayor que cero."
            )

        self._unidades_disponibles = unidades_disponibles

    # PROPIEDAD: UNIDADES DISPONIBLES

    @property
    def unidades_disponibles(self):
        return self._unidades_disponibles

    # DESCRIPCION DEL SERVICIO

    def describir(self):

        return (
            f"Equipo: {self.nombre} | "
            f"Tarifa diaria: ${self.tarifa_base:,.0f} | "
            f"Unidades disponibles: {self.unidades_disponibles}"
        )

    # VALIDAR PARAMETROS DEL ALQUILER

    def validar_parametros(self, **kwargs):

        dias = kwargs.get("dias")
        unidades = kwargs.get("unidades")

        if not isinstance(dias, (int, float)) or isinstance(dias, bool) or dias <= 0:
            raise DatosInvalidosError("La cantidad de días debe ser mayor que cero.")

        if not isinstance(unidades, int) or isinstance(unidades, bool):
            raise DatosInvalidosError(
                "La cantidad de equipos debe ser un número entero."
            )

        if unidades <= 0:
            raise DatosInvalidosError("Debe alquilar al menos un equipo.")

        if unidades > self.unidades_disponibles:
            raise ServicioNoDisponibleError("No hay suficientes equipos disponibles.")

        return True

    # CALCULAR COSTO DEL SERVICIO

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):

        # Validar los parámetros del alquiler
        self.validar_parametros(dias=cantidad, unidades=1)

        # Validar impuesto y descuento
        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not 0 <= impuesto <= 100
            or not 0 <= descuento <= 100
        ):
            raise DatosInvalidosError(
                "El impuesto y el descuento deben estar entre 0 y 100."
            )

        # Calcular el subtotal
        subtotal = self.tarifa_base * cantidad

        # Aplicar descuento
        valor_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - valor_descuento

        # Aplicar impuesto
        valor_impuesto = subtotal_con_descuento * (impuesto / 100)

        # Calcular el total
        total = subtotal_con_descuento + valor_impuesto

        return total


# SERVICIO ESPECIALIZADO 3 -->  ASESORIAS, se aplica herencias


class AsesoriaEspecializada(Servicio):

    # Constructor de la clase
    def __init__(self, identificador, nombre, tarifa_base, especialidad, modalidad):

        # Inicializar los atributos heredados
        super().__init__(identificador, nombre, tarifa_base)

        # Validar la especialidad
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosError("La especialidad de la asesoría es obligatoria.")

        # Validar la modalidad
        modalidades_permitidas = ["Presencial", "Virtual"]

        if modalidad not in modalidades_permitidas:
            raise DatosInvalidosError("La modalidad debe ser Presencial o Virtual.")

        self._especialidad = especialidad.strip()
        self._modalidad = modalidad

    # PROPIEDAD: ESPECIALIDAD

    @property
    def especialidad(self):
        return self._especialidad

    # PROPIEDAD: MODALIDAD

    @property
    def modalidad(self):
        return self._modalidad

    # DESCRIPCION DEL SERVICIO

    def describir(self):

        return (
            f"Asesoría: {self.nombre} | "
            f"Especialidad: {self.especialidad} | "
            f"Modalidad: {self.modalidad} | "
            f"Tarifa por hora: ${self.tarifa_base:,.0f}"
        )

    # VALIDAR PARAMETROS DE LA ASESORIA

    def validar_parametros(self, **kwargs):

        horas = kwargs.get("horas")
        modalidad = kwargs.get("modalidad")

        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or horas <= 0:
            raise DatosInvalidosError(
                "Las horas de asesoría deben ser mayores que cero."
            )

        if modalidad not in ["Presencial", "Virtual"]:
            raise DatosInvalidosError("La modalidad seleccionada no es válida.")

        return True

    # CALCULAR COSTO DE LA ASESORIA

    def calcular_costo(self, cantidad=1, impuesto=0, descuento=0):

        # Validar los parámetros de la asesoría
        self.validar_parametros(horas=cantidad, modalidad=self.modalidad)

        # Validar impuesto y descuento
        if (
            not isinstance(impuesto, (int, float))
            or isinstance(impuesto, bool)
            or not isinstance(descuento, (int, float))
            or isinstance(descuento, bool)
            or not 0 <= impuesto <= 100
            or not 0 <= descuento <= 100
        ):
            raise DatosInvalidosError(
                "El impuesto y el descuento deben estar entre 0 y 100."
            )

        # Calcular subtotal
        subtotal = self.tarifa_base * cantidad

        # Aplicar descuento
        valor_descuento = subtotal * (descuento / 100)
        subtotal_con_descuento = subtotal - valor_descuento

        # Aplicar impuesto
        valor_impuesto = subtotal_con_descuento * (impuesto / 100)

        # Calcular total
        total = subtotal_con_descuento + valor_impuesto

        return total


# CLASE RESERVA


class Reserva(Entidad):

    # Constructor de la clase
    def __init__(self, identificador, cliente, servicio, duracion):

        # Inicializar el identificador heredado
        super().__init__(identificador)

        # Validar que el cliente sea un objeto Cliente
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("La reserva debe tener un cliente válido.")

        # Validar que el servicio sea un objeto Servicio
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("La reserva debe tener un servicio válido.")

        # Validar la duración
        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise DatosInvalidosError("La duración debe ser mayor que cero.")

        # Guardar los datos de la reserva
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion

        # Estado inicial de la reserva
        self._estado = "Pendiente"

        # Costo inicial
        self._costo = 0

    # PROPIEDADES

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    # CONFIRMAR RESERVA

    def confirmar(self):

        if self._estado != "Pendiente":
            raise OperacionReservaError("Solo se pueden confirmar reservas pendientes.")

        self._estado = "Confirmada"

        registrar_evento(f"Reserva {self.identificador} confirmada.")

        return "Reserva confirmada correctamente."

    # CANCELAR RESERVA

    def cancelar(self):

        if self._estado not in ["Pendiente", "Confirmada"]:
            raise OperacionReservaError(
                "No se puede cancelar una reserva procesada o cancelada."
            )

        self._estado = "Cancelada"

        registrar_evento(f"Reserva {self.identificador} cancelada.")

        return "Reserva cancelada correctamente."

    # PROCESAR RESERVA

    def procesar(self):

        if self._estado != "Confirmada":
            raise OperacionReservaError(
                "La reserva debe estar confirmada antes de procesarse."
            )

        try:

            # Calcular el costo utilizando el servicio contratado
            self._costo = self._servicio.calcular_costo(cantidad=self._duracion)

            self._estado = "Procesada"

            registrar_evento(
                f"Reserva {self.identificador} procesada. " f"Costo: {self._costo}"
            )

            return self._costo

        except Exception as error:

            registrar_error(
                f"Error al procesar la reserva {self.identificador}: {error}"
            )

            raise OperacionReservaError(
                "No fue posible procesar la reserva."
            ) from error

    # OBTENER RESUMEN

    def obtener_resumen(self):

        return (
            f"Reserva: {self.identificador}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duración: {self.duracion}\n"
            f"Estado: {self.estado}\n"
            f"Costo: ${self.costo:,.0f}"
        )


# CLASE GESTOR DE CLIENTES


class GestorClientes:

    # Constructor de la clase
    def __init__(self):

        # Lista donde se almacenarán los clientes
        self._clientes = []

    # Registrar un cliente
    def registrar_cliente(self, cliente):

        # Comprobar que sea un objeto Cliente
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El registro debe contener un cliente válido.")

        # Verificar que no exista el identificador
        for cliente_existente in self._clientes:

            if cliente_existente.identificador == cliente.identificador:
                raise RegistroDuplicadoError(
                    "Ya existe un cliente con ese identificador."
                )

        # Agregar el cliente a la lista
        self._clientes.append(cliente)

        # Registrar el evento
        registrar_evento(f"Cliente registrado: {cliente.identificador}")

        return "Cliente registrado correctamente."

    # Consultar todos los clientes
    def listar_clientes(self):

        return self._clientes.copy()

    # Buscar un cliente por identificador
    def buscar_cliente(self, identificador):

        for cliente in self._clientes:

            if cliente.identificador == identificador:
                return cliente

        return None


# CLASE GESTOR DE SERVICIOS


class GestorServicios:

    # Constructor de la clase
    def __init__(self):

        # Lista para almacenar los servicios
        self._servicios = []

    # Registrar un servicio
    def registrar_servicio(self, servicio):

        # Comprobar que sea un servicio válido
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El registro debe contener un servicio válido.")

        # Verificar que no exista el identificador
        for servicio_existente in self._servicios:

            if servicio_existente.identificador == servicio.identificador:
                raise RegistroDuplicadoError(
                    "Ya existe un servicio con ese identificador."
                )

        # Agregar el servicio a la lista
        self._servicios.append(servicio)

        # Registrar el evento
        registrar_evento(f"Servicio registrado: {servicio.identificador}")

        return "Servicio registrado correctamente."

    # Consultar todos los servicios
    def listar_servicios(self):

        return self._servicios.copy()

    # Buscar un servicio por identificador
    def buscar_servicio(self, identificador):

        for servicio in self._servicios:

            if servicio.identificador == identificador:
                return servicio

        return None


# CLASE GESTOR DE RESERVAS


class GestorReservas:

    # Constructor de la clase
    def __init__(self):

        # Lista para almacenar las reservas
        self._reservas = []

    # Registrar una reserva
    def registrar_reserva(self, reserva):

        # Comprobar que sea una reserva válida
        if not isinstance(reserva, Reserva):
            raise DatosInvalidosError("El registro debe contener una reserva válida.")

        # Verificar que no exista el identificador
        for reserva_existente in self._reservas:

            if reserva_existente.identificador == reserva.identificador:
                raise RegistroDuplicadoError(
                    "Ya existe una reserva con ese identificador."
                )

        # Agregar la reserva a la lista
        self._reservas.append(reserva)

        # Registrar el evento
        registrar_evento(f"Reserva registrada: {reserva.identificador}")

        return "Reserva registrada correctamente."

    # Consultar todas las reservas
    def listar_reservas(self):

        return self._reservas.copy()

    # Buscar una reserva por identificador
    def buscar_reserva(self, identificador):

        for reserva in self._reservas:

            if reserva.identificador == identificador:
                return reserva

        return None


# INTERFAZ PRINCIPAL DE SOFTWARE FJ


def iniciar_interfaz():

    # Crear la ventana principal
    ventana = tk.Tk()

    # CREAR LOS GESTORES DEL SISTEMA

    gestor_clientes = GestorClientes()
    gestor_servicios = GestorServicios()
    gestor_reservas = GestorReservas()

    # Configuración general de la ventana
    ventana.title("Software FJ | Sistema Integral de Gestión")
    ventana.geometry("1200x750")
    ventana.minsize(1000, 650)
    ventana.configure(bg="#F4F7FC")

    # Definir colores corporativos
    AZUL_OSCURO = "#172B4D"
    AZUL_PRINCIPAL = "#2563EB"
    AZUL_CLARO = "#EFF6FF"
    FONDO = "#F4F7FC"
    BLANCO = "#FFFFFF"
    TEXTO = "#1E293B"
    TEXTO_SECUNDARIO = "#64748B"

    # Configurar el estilo de los componentes
    estilo = ttk.Style()
    estilo.theme_use("clam")

    estilo.configure(
        "Menu.TButton",
        font=("Segoe UI", 10),
        background=AZUL_OSCURO,
        foreground=BLANCO,
        borderwidth=0,
        padding=(15, 12),
        anchor="w",
    )

    estilo.map(
        "Menu.TButton",
        background=[("active", "#29466F"), ("pressed", AZUL_PRINCIPAL)],
        foreground=[("active", BLANCO)],
    )

    # CONTENEDOR PRINCIPAL

    contenedor = tk.Frame(ventana, bg=FONDO)

    contenedor.pack(fill="both", expand=True)

    # MENÚ LATERAL

    menu_lateral = tk.Frame(contenedor, bg=AZUL_OSCURO, width=245)

    menu_lateral.pack(side="left", fill="y")

    # Evitar que el menú cambie de tamaño
    menu_lateral.pack_propagate(False)

    # Nombre del sistema
    marca = tk.Label(
        menu_lateral,
        text="SOFTWARE FJ",
        font=("Segoe UI", 20, "bold"),
        bg=AZUL_OSCURO,
        fg=BLANCO,
    )

    marca.pack(pady=(30, 5))

    # Descripción del sistema
    descripcion = tk.Label(
        menu_lateral,
        text="Sistema de Gestión",
        font=("Segoe UI", 9),
        bg=AZUL_OSCURO,
        fg="#B8C7DC",
    )

    descripcion.pack(pady=(0, 35))

    # Título del menú
    etiqueta_menu = tk.Label(
        menu_lateral,
        text="MENÚ PRINCIPAL",
        font=("Segoe UI", 9, "bold"),
        bg=AZUL_OSCURO,
        fg="#94A3B8",
        anchor="w",
    )

    etiqueta_menu.pack(fill="x", padx=20, pady=(0, 12))

    # FUNCIÓN PARA CAMBIAR DE PANTALLA

    def mostrar_pantalla(nombre, descripcion):

        # Eliminar el contenido anterior
        for elemento in contenido.winfo_children():
            elemento.destroy()

        # Mostrar el título de la sección
        titulo = tk.Label(
            contenido, text=nombre, font=("Segoe UI", 22, "bold"), bg=FONDO, fg=TEXTO
        )

        titulo.pack(anchor="w")

        # Mostrar una descripción
        subtitulo = tk.Label(
            contenido,
            text=descripcion,
            font=("Segoe UI", 10),
            bg=FONDO,
            fg=TEXTO_SECUNDARIO,
        )

        subtitulo.pack(anchor="w", pady=(5, 25))

        # Mostrar una tarjeta genérica, excepto en Servicios
        if nombre != "Servicios":

            # Crear una tarjeta de presentación
            tarjeta = tk.Frame(contenido, bg=BLANCO, padx=25, pady=25)

            tarjeta.pack(fill="x", pady=10)

            mensaje = tk.Label(
                tarjeta,
                text=f"Bienvenido al módulo de {nombre}",
                font=("Segoe UI", 16, "bold"),
                bg=BLANCO,
                fg=AZUL_PRINCIPAL,
            )

            mensaje.pack(anchor="w")

            informacion = tk.Label(
                tarjeta,
                text="Este espacio será utilizado para las funciones de este módulo.",
                font=("Segoe UI", 10),
                bg=BLANCO,
                fg=TEXTO_SECUNDARIO,
            )

            informacion.pack(anchor="w", pady=(10, 0))

        # MÓDULO DASHBOARD

        if nombre == "Dashboard":

            # Contenedor de las tarjetas
            contenedor_tarjetas = tk.Frame(contenido, bg=FONDO)
            contenedor_tarjetas.pack(fill="x", pady=20)

            # Función para crear indicadores
            def crear_tarjeta_indicador(titulo, valor, color):

                tarjeta = tk.Frame(
                    contenedor_tarjetas,
                    bg=BLANCO,
                    padx=20,
                    pady=20,
                    highlightbackground="#E2E8F0",
                    highlightthickness=1,
                )

                tarjeta.pack(side="left", fill="both", expand=True, padx=8)

                tk.Label(
                    tarjeta,
                    text=titulo,
                    font=("Segoe UI", 10),
                    bg=BLANCO,
                    fg=TEXTO_SECUNDARIO,
                ).pack(anchor="w")

                tk.Label(
                    tarjeta,
                    text=valor,
                    font=("Segoe UI", 25, "bold"),
                    bg=BLANCO,
                    fg=color,
                ).pack(anchor="w", pady=(10, 0))

            # Indicador de clientes
            crear_tarjeta_indicador(
                "CLIENTES REGISTRADOS",
                str(len(gestor_clientes.listar_clientes())),
                AZUL_PRINCIPAL,
            )

            # Indicador de servicios
            crear_tarjeta_indicador(
                "SERVICIOS DISPONIBLES",
                str(len(gestor_servicios.listar_servicios())),
                "#0F766E",
            )

            # Indicador de reservas
            crear_tarjeta_indicador(
                "RESERVAS REGISTRADAS",
                str(len(gestor_reservas.listar_reservas())),
                "#D97706",
            )

        # MÓDULO DE SERVICIOS

        # MÓDULO DE SERVICIOS
        if nombre == "Servicios":

            # Crear tarjeta principal del módulo
            tarjeta_servicios = tk.Frame(contenido, bg=BLANCO, padx=25, pady=25)
            tarjeta_servicios.pack(fill="x", pady=10)

            # Título del formulario
            tk.Label(
                tarjeta_servicios,
                text="Registrar nuevo servicio",
                font=("Segoe UI", 16, "bold"),
                bg=BLANCO,
                fg=AZUL_PRINCIPAL,
            ).pack(anchor="w", pady=(0, 20))

            # Campo para seleccionar el tipo de servicio
            tk.Label(
                tarjeta_servicios,
                text="Tipo de servicio:",
                font=("Segoe UI", 10, "bold"),
                bg=BLANCO,
                fg=TEXTO,
            ).pack(anchor="w")

            tipo_servicio = ttk.Combobox(
                tarjeta_servicios,
                values=[
                    "Reserva de sala",
                    "Alquiler de equipos",
                    "Asesoría especializada",
                ],
                state="readonly",
                width=55,
                font=("Segoe UI", 11),
            )
            tipo_servicio.pack(anchor="w", pady=(7, 20), ipady=5)

            # Campo para ingresar el nombre del servicio
            tk.Label(
                tarjeta_servicios,
                text="Nombre del servicio:",
                font=("Segoe UI", 10, "bold"),
                bg=BLANCO,
                fg=TEXTO,
            ).pack(anchor="w")

            entrada_nombre_servicio = ttk.Entry(
                tarjeta_servicios, width=58, font=("Segoe UI", 11)
            )
            entrada_nombre_servicio.pack(anchor="w", pady=(7, 20), ipady=5)

            # Limpiar el nombre cuando cambie el tipo de servicio
            def limpiar_nombre_servicio(event):
                entrada_nombre_servicio.delete(0, tk.END)

            tipo_servicio.bind("<<ComboboxSelected>>", limpiar_nombre_servicio)

            # Campo para ingresar la tarifa base del servicio
            tk.Label(
                tarjeta_servicios,
                text="Tarifa base (COP):",
                font=("Segoe UI", 10, "bold"),
                bg=BLANCO,
                fg=TEXTO,
            ).pack(anchor="w")

            entrada_tarifa_servicio = ttk.Entry(
                tarjeta_servicios, width=58, font=("Segoe UI", 11)
            )
            entrada_tarifa_servicio.pack(anchor="w", pady=(7, 20), ipady=5)

            entrada_descripcion_servicio = tk.Text(
                tarjeta_servicios,
                width=58,
                height=6,
                font=("Segoe UI", 11),
                wrap="word",
                bg=BLANCO,
                fg=TEXTO,
                bd=1,
                relief="solid",
                highlightthickness=1,
                highlightbackground="#CBD5E1",
                highlightcolor=AZUL_PRINCIPAL,
                padx=10,
                pady=8,
            )
            entrada_descripcion_servicio.pack(anchor="w", pady=(7, 15))

        # MÓDULO DE CLIENTES

        if nombre == "Clientes":

            # Contenedor de la tabla
            tabla_contenedor = tk.Frame(contenido, bg=BLANCO, padx=20, pady=20)
            tabla_contenedor.pack(fill="both", expand=True, pady=10)

            # Título de la sección
            tk.Label(
                tabla_contenedor,
                text="Listado de clientes",
                font=("Segoe UI", 14, "bold"),
                bg=BLANCO,
                fg=TEXTO,
            ).pack(anchor="w", pady=(0, 15))

            # FORMULARIO DE REGISTRO DE CLIENTES

            formulario = tk.Frame(tabla_contenedor, bg=BLANCO)
            formulario.pack(fill="x", pady=(0, 20))

            # Campo de identificación
            tk.Label(formulario, text="Identificación:", bg=BLANCO, fg=TEXTO).grid(
                row=0, column=0, sticky="w", padx=5
            )

            entrada_id = ttk.Entry(formulario, width=22)
            entrada_id.grid(row=1, column=0, padx=5, pady=5)

            # Campo de nombre
            tk.Label(formulario, text="Nombre completo:", bg=BLANCO, fg=TEXTO).grid(
                row=0, column=1, sticky="w", padx=5
            )

            entrada_nombre = ttk.Entry(formulario, width=25)
            entrada_nombre.grid(row=1, column=1, padx=5, pady=5)

            # Campo de correo
            tk.Label(formulario, text="Correo electrónico:", bg=BLANCO, fg=TEXTO).grid(
                row=0, column=2, sticky="w", padx=5
            )

            entrada_correo = ttk.Entry(formulario, width=28)
            entrada_correo.grid(row=1, column=2, padx=5, pady=5)

            # Campo de teléfono
            tk.Label(formulario, text="Teléfono:", bg=BLANCO, fg=TEXTO).grid(
                row=0, column=3, sticky="w", padx=5
            )

            entrada_telefono = ttk.Entry(formulario, width=18)
            entrada_telefono.grid(row=1, column=3, padx=5, pady=5)

            # Crear tabla de clientes
            #            tabla_clientes = ttk.Treeview(
            #                tabla_contenedor,
            #                columns=("ID", "Nombre", "Correo", "Telefono"),
            #                show="headings",
            #                height=10,
            #            )

            #            tabla_clientes.heading("ID", text="Identificación")
            #            tabla_clientes.heading("Nombre", text="Nombre completo")
            #            tabla_clientes.heading("Correo", text="Correo electrónico")
            #            tabla_clientes.heading("Telefono", text="Teléfono")

            #            tabla_clientes.column("ID", width=120)
            #            tabla_clientes.column("Nombre", width=200)
            #            tabla_clientes.column("Correo", width=250)
            #            tabla_clientes.column("Telefono", width=140)

            #            tabla_clientes.pack(fill="both", expand=True)

            # Contenedor para la tabla y la barra de desplazamiento
            marco_tabla = tk.Frame(tabla_contenedor, bg=BLANCO)
            marco_tabla.pack(fill="both", expand=True)

            # Crear la tabla de clientes
            tabla_clientes = ttk.Treeview(
                marco_tabla,
                columns=("id", "nombre", "correo", "telefono"),
                show="headings",
                height=10,
            )

            # Configurar los encabezados
            tabla_clientes.heading("id", text="ID")
            tabla_clientes.heading("nombre", text="Nombre")
            tabla_clientes.heading("correo", text="Correo")
            tabla_clientes.heading("telefono", text="Teléfono")

            # Configurar el ancho de las columnas
            tabla_clientes.column("id", width=100, anchor="center")
            tabla_clientes.column("nombre", width=200)
            tabla_clientes.column("correo", width=250)
            tabla_clientes.column("telefono", width=150, anchor="center")

            # Crear la barra de desplazamiento vertical
            barra_vertical = ttk.Scrollbar(
                marco_tabla, orient="vertical", command=tabla_clientes.yview
            )

            # Conectar la barra con la tabla
            tabla_clientes.configure(yscrollcommand=barra_vertical.set)

            # Ubicar la tabla y la barra de desplazamiento
            tabla_clientes.grid(row=0, column=0, sticky="nsew")
            barra_vertical.grid(row=0, column=1, sticky="ns")

            # Permitir que la tabla se expanda
            marco_tabla.grid_rowconfigure(0, weight=1)
            marco_tabla.grid_columnconfigure(0, weight=1)

            # Limpiar la tabla antes de cargar los clientes
            for elemento in tabla_clientes.get_children():
                tabla_clientes.delete(elemento)

            # Cargar los clientes registrados en el gestor
            for cliente in gestor_clientes.listar_clientes():
                tabla_clientes.insert(
                    "",
                    "end",
                    values=(
                        cliente.identificador,
                        cliente.nombre,
                        cliente.correo,
                        cliente.telefono,
                    ),
                )

            # FUNCIÓN PARA REGISTRAR CLIENTES

            def registrar_cliente_interfaz():

                try:
                    # Obtener los datos del formulario
                    cliente = Cliente(
                        entrada_id.get(),
                        entrada_nombre.get(),
                        entrada_correo.get(),
                        entrada_telefono.get(),
                    )

                    # Registrar el cliente en el gestor
                    gestor_clientes.registrar_cliente(cliente)

                    # Limpiar la tabla
                    for elemento in tabla_clientes.get_children():
                        tabla_clientes.delete(elemento)

                    # Actualizar la tabla
                    for cliente_registrado in gestor_clientes.listar_clientes():

                        tabla_clientes.insert(
                            "",
                            "end",
                            values=(
                                cliente_registrado.identificador,
                                cliente_registrado.nombre,
                                cliente_registrado.correo,
                                cliente_registrado.telefono,
                            ),
                        )

                    # Limpiar los campos
                    entrada_id.delete(0, tk.END)
                    entrada_nombre.delete(0, tk.END)
                    entrada_correo.delete(0, tk.END)
                    entrada_telefono.delete(0, tk.END)

                    # Limpiar los campos
                    #                    entrada_id.delete(0, tk.END)
                    #                    entrada_nombre.delete(0, tk.END)
                    #                    entrada_correo.delete(0, tk.END)
                    #                    entrada_telefono.delete(0, tk.END)

                    messagebox.showinfo(
                        "Registro exitoso", "El cliente fue registrado correctamente."
                    )

                except ErrorSistema as error:

                    messagebox.showerror("Error de registro", str(error))

            # Botón para registrar cliente
            boton_registrar = tk.Button(
                formulario,
                text="+ Registrar cliente",
                command=registrar_cliente_interfaz,
                bg=AZUL_PRINCIPAL,
                fg=BLANCO,
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                padx=15,
                pady=7,
                cursor="hand2",
            )

            boton_registrar.grid(row=1, column=4, padx=(15, 5), pady=5)

    #            tabla_clientes.insert(
    #                "",
    #                "end",
    #                values=(
    #                    cliente.identificador,
    #                    cliente.nombre,
    #                    cliente.correo,
    #                    cliente.telefono,
    #                ),
    #            )

    # OPCIONES DE NAVEGACIÓN

    opciones_menu = [
        ("▦   Dashboard", "Dashboard", "Resumen general del sistema."),
        ("♙   Clientes", "Clientes", "Administración de clientes."),
        ("▣   Servicios", "Servicios", "Administración de servicios."),
        ("▤   Reservas", "Reservas", "Gestión y seguimiento de reservas."),
        ("✓   Pruebas del sistema", "Pruebas", "Verificación del funcionamiento."),
        ("≡   Registros", "Registros", "Consulta de eventos y errores."),
    ]

    for texto, nombre, descripcion in opciones_menu:

        boton = ttk.Button(
            menu_lateral,
            text=texto,
            style="Menu.TButton",
            command=lambda n=nombre, d=descripcion: mostrar_pantalla(n, d),
        )

        boton.pack(fill="x", padx=12, pady=3)

    # ÁREA DE TRABAJO

    area_trabajo = tk.Frame(contenedor, bg=FONDO)

    area_trabajo.pack(side="left", fill="both", expand=True)

    # ENCABEZADO SUPERIOR

    encabezado = tk.Frame(area_trabajo, bg=BLANCO, height=75)

    encabezado.pack(fill="x")

    encabezado.pack_propagate(False)

    nombre_empresa = tk.Label(
        encabezado,
        text="Software FJ",
        font=("Segoe UI", 13, "bold"),
        bg=BLANCO,
        fg=TEXTO,
    )

    nombre_empresa.pack(side="left", padx=30, pady=20)

    estado_sistema = tk.Label(
        encabezado,
        text="● Sistema activo",
        font=("Segoe UI", 9),
        bg=BLANCO,
        fg="#16A34A",
    )

    estado_sistema.pack(side="right", padx=30)

    # CONTENIDO CENTRAL

    contenido = tk.Frame(area_trabajo, bg=FONDO)

    contenido.pack(fill="both", expand=True, padx=30, pady=25)

    # Título inicial
    titulo_pagina = tk.Label(
        contenido, text="Dashboard", font=("Segoe UI", 22, "bold"), bg=FONDO, fg=TEXTO
    )

    titulo_pagina.pack(anchor="w")

    subtitulo_pagina = tk.Label(
        contenido,
        text="Bienvenido al sistema integral de gestión de Software FJ.",
        font=("Segoe UI", 10),
        bg=FONDO,
        fg=TEXTO_SECUNDARIO,
    )

    subtitulo_pagina.pack(anchor="w", pady=(5, 25))

    # Tarjeta de bienvenida
    tarjeta = tk.Frame(contenido, bg=BLANCO, padx=25, pady=25)

    tarjeta.pack(fill="x", pady=10)

    mensaje_bienvenida = tk.Label(
        tarjeta,
        text="¡Bienvenido a Software FJ!",
        font=("Segoe UI", 18, "bold"),
        bg=BLANCO,
        fg=AZUL_PRINCIPAL,
    )

    mensaje_bienvenida.pack(anchor="w")

    mensaje_descripcion = tk.Label(
        tarjeta,
        text=("Administra clientes, servicios y reservas " "desde un solo lugar."),
        font=("Segoe UI", 11),
        bg=BLANCO,
        fg=TEXTO_SECUNDARIO,
    )

    mensaje_descripcion.pack(anchor="w", pady=(10, 0))

    # TARJETAS DE INDICADORES DEL DASHBOARD

    # ACTUALIZAR INDICADORES DEL DASHBOARD

    def actualizar_dashboard():

        # Consultar la cantidad de registros
        total_clientes = len(gestor_clientes.listar_clientes())
        total_servicios = len(gestor_servicios.listar_servicios())
        total_reservas = len(gestor_reservas.listar_reservas())

        # Actualizar los valores de las tarjetas
        for tarjeta in contenedor_tarjetas.winfo_children():

            etiquetas = tarjeta.winfo_children()

            if len(etiquetas) >= 2:

                titulo = etiquetas[0].cget("text")

                if titulo == "CLIENTES REGISTRADOS":
                    etiquetas[1].config(text=str(total_clientes))

                elif titulo == "SERVICIOS DISPONIBLES":
                    etiquetas[1].config(text=str(total_servicios))

                elif titulo == "RESERVAS REGISTRADAS":
                    etiquetas[1].config(text=str(total_reservas))

    # BOTÓN DE CIERRE

    boton_salir = tk.Button(
        menu_lateral,
        text="  Salir del sistema",
        font=("Segoe UI", 10),
        bg=AZUL_OSCURO,
        fg="#FCA5A5",
        activebackground="#29466F",
        activeforeground=BLANCO,
        relief="flat",
        bd=0,
        cursor="hand2",
        anchor="w",
        command=ventana.destroy,
    )

    boton_salir.pack(side="bottom", fill="x", padx=15, pady=20)

    # Iniciar la aplicación
    ventana.mainloop()


if __name__ == "__main__":

    # ==========================================
    # PRUEBAS INICIALES DEL SISTEMA
    # ==========================================

    print("======================================")
    print(" SOFTWARE FJ")
    print(" Sistema iniciado correctamente")
    print("======================================")

    registrar_evento("Prueba inicial del sistema.")

    print("Archivo de registros configurado.")
    print("Excepciones personalizadas creadas.")

    # Clase temporal para probar Entidad
    class EntidadPrueba(Entidad):

        def obtener_resumen(self):
            return f"Entidad identificada con código: {self.identificador}"

    # Crear un objeto de prueba
    prueba = EntidadPrueba("TEST-001")

    print("--------------------------------------")
    print("PRUEBA DE LA CLASE ENTIDAD")
    print(prueba.obtener_resumen())
    # ======================================
    # PRUEBA DE LA CLASE CLIENTE
    # ======================================

    print("--------------------------------------")
    print("PRUEBA DE LA CLASE CLIENTE")

    cliente1 = Cliente("CLI-001", "Carlos Pérez", "carlos@gmail.com", "3001234567")

    print(cliente1.obtener_resumen())
    # ======================================
    # PRUEBA DE VALIDACION DE CLIENTE
    # # ======================================

    print("--------------------------------------")
    print("PRUEBA DE CORREO INVALIDO")

    try:
        cliente_invalido = Cliente(
            "CLI-002", "Pedro Gómez", "correo_incorrecto", "3109876543"
        )

        print(cliente_invalido.obtener_resumen())

    except DatosInvalidosError as error:
        print("Validación correcta:", error)
    # ======================================
    # PRUEBA DE LA CLASE SERVICIO
    # ======================================

    print("--------------------------------------")
    print("PRUEBA DE LA CLASE SERVICIO")

    print("Clase abstracta Servicio creada correctamente.")

    print("Métodos abstractos pendientes:")

    for metodo in sorted(Servicio.__abstractmethods__):
        print("-", metodo)
    # ======================================
    # PRUEBA DEL SERVICIO RESERVA DE SALAS
    # ======================================

    print("--------------------------------------")
    print("PRUEBA DEL SERVICIO RESERVA DE SALAS")

    sala1 = ReservaSala("SER-001", "Sala de reuniones principal", 50000, 10)

    print(sala1.describir())

    # Validar una reserva para 8 personas durante 3 horas
    sala1.validar_parametros(horas=3, personas=8)

    print("Validación de la reserva: Correcta")

    # Calcular el costo con descuento e impuesto
    costo = sala1.calcular_costo(cantidad=3, impuesto=19, descuento=10)

    print(f"Costo total de la reserva: ${costo:,.0f}")

    # ======================================
    # PRUEBA DEL SERVICIO ALQUILER DE EQUIPOS
    # ======================================

    print("--------------------------------------")
    print("PRUEBA DEL SERVICIO ALQUILER DE EQUIPOS")

    equipo1 = AlquilerEquipo("SER-002", "Computador portátil", 40000, 5)

    print(equipo1.describir())

    # Validar alquiler de 2 equipos durante 3 días
    equipo1.validar_parametros(dias=3, unidades=2)

    print("Validación del alquiler: Correcta")

    # Calcular costo de 3 días con impuesto del 19 %
    costo_equipo = equipo1.calcular_costo(cantidad=3, impuesto=19)

    print(f"Costo total del alquiler: ${costo_equipo:,.0f}")

    # Probar una cantidad superior a la disponible
    print("--------------------------------------")
    print("PRUEBA DE EQUIPOS NO DISPONIBLES")

    try:
        equipo1.validar_parametros(dias=2, unidades=8)

    except ServicioNoDisponibleError as error:
        print("Validación correcta:", error)

    # ======================================
    # PRUEBA DEL SERVICIO DE ASESORIAS
    # ======================================

    print("--------------------------------------")
    print("PRUEBA DEL SERVICIO DE ASESORIAS")

    asesoria1 = AsesoriaEspecializada(
        "SER-003",
        "Asesoría de implementación de software",
        80000,
        "Implementación de software",
        "Virtual",
    )

    print(asesoria1.describir())

    # Validar una asesoría de 2 horas
    asesoria1.validar_parametros(horas=2, modalidad="Virtual")

    print("Validación de la asesoría: Correcta")

    # Calcular costo con descuento del 5 % e impuesto del 19 %
    costo_asesoria = asesoria1.calcular_costo(cantidad=2, impuesto=19, descuento=5)

    print(f"Costo total de la asesoría: ${costo_asesoria:,.0f}")

    # Probar una modalidad incorrecta
    print("--------------------------------------")
    print("PRUEBA DE MODALIDAD INVALIDA")

    try:
        asesoria_invalida = AsesoriaEspecializada(
            "SER-004", "Asesoría técnica", 80000, "Soporte técnico", "Telepatica"
        )

    except DatosInvalidosError as error:
        print("Validación correcta:", error)

    # ======================================
    # PRUEBA DE POLIMORFISMO
    # ======================================

    print("--------------------------------------")
    print("PRUEBA DE POLIMORFISMO")

    # Crear una lista con los tres tipos de servicios
    servicios = [sala1, equipo1, asesoria1]

    # Recorrer los servicios utilizando los mismos métodos
    for servicio in servicios:

        print("--------------------------------------")

        # Cada objeto ejecuta su propia descripción
        print(servicio.describir())

        # Cada objeto ejecuta su propio cálculo
        costo = servicio.calcular_costo(cantidad=2)

        print(f"Costo por 2 unidades de tiempo: ${costo:,.0f}")

    # ==========================================
    # PRUEBA DE RESERVA EXITOSA
    # ==========================================

    print("\nPRUEBA DE RESERVA EXITOSA")

    # Crear un cliente
    cliente_reserva = Cliente(
        "CLI-003", "Laura Martínez", "laura@gmail.com", "3101234567"
    )

    # Crear un servicio de sala
    sala_reserva = ReservaSala("SER-004", "Sala de capacitación", 50000, 15)

    # Crear la reserva para 3 horas
    reserva1 = Reserva("RES-001", cliente_reserva, sala_reserva, 3)

    # Confirmar la reserva
    print(reserva1.confirmar())

    # Procesar la reserva
    costo_final = reserva1.procesar()

    print(f"Costo final: ${costo_final:,.0f}")

    # Mostrar el resumen
    print(reserva1.obtener_resumen())

    # ==========================================
    # PRUEBA DE RESERVA SIN CONFIRMAR
    # ==========================================

    print("\nPRUEBA DE RESERVA SIN CONFIRMAR")

    try:
        # Crear una nueva reserva
        reserva2 = Reserva("RES-002", cliente_reserva, sala_reserva, 2)

        # Intentar procesarla sin confirmarla
        reserva2.procesar()

    except OperacionReservaError as error:
        print(f"Error controlado correctamente: {error}")
    # ==========================================
    # PRUEBA DE CANCELACIÓN DE RESERVA
    # ==========================================

    print("\nPRUEBA DE CANCELACIÓN DE RESERVA")

    try:
        # Crear una nueva reserva
        reserva3 = Reserva("RES-003", cliente_reserva, sala_reserva, 2)

        # Cancelar la reserva
        print(reserva3.cancelar())

        # Mostrar el estado actual
        print(f"Estado actual: {reserva3.estado}")

        # Intentar procesar la reserva cancelada
        reserva3.procesar()

    except OperacionReservaError as error:
        print(f"Error controlado correctamente: {error}")
    # ==========================================
    # PRUEBA DE DURACIÓN INVÁLIDA
    # ==========================================

    print("\nPRUEBA DE DURACIÓN INVÁLIDA")

    try:
        reserva4 = Reserva("RES-004", cliente_reserva, sala_reserva, 0)

    except DatosInvalidosError as error:
        print(f"Error controlado correctamente: {error}")
    # ==========================================
    # PRUEBA DE EQUIPO NO DISPONIBLE
    # ==========================================

    print("\nPRUEBA DE EQUIPO NO DISPONIBLE")

    try:
        # Crear un servicio con solo 2 equipos disponibles
        equipo_reserva = AlquilerEquipo("SER-005", "Computadores portátiles", 40000, 2)

        # Intentar solicitar 5 equipos
        equipo_reserva.validar_parametros(dias=3, unidades=5)

    except ServicioNoDisponibleError as error:
        print(f"Error controlado correctamente: {error}")
    # ==========================================
    # PRUEBA DE MANEJO AVANZADO DE EXCEPCIONES
    # ==========================================

    print("\nPRUEBA DE MANEJO AVANZADO DE EXCEPCIONES")

    try:
        # Intentar realizar una operación válida
        numero = 10
        resultado = numero / 2

    except ZeroDivisionError as error:
        # Se ejecuta si ocurre una división entre cero
        print(f"Se presentó un error: {error}")

    else:
        # Se ejecuta cuando no ocurre ninguna excepción
        print(f"Operación realizada correctamente: {resultado}")

    finally:
        # Se ejecuta siempre, haya ocurrido un error o no
        print("Finalizó la operación de prueba.")
    # ==========================================
    # PRUEBA DE CAPTURA DE ERRORES
    # ==========================================

    print("\nPRUEBA DE CAPTURA DE ERRORES")

    try:
        # Provocar intencionalmente una división entre cero
        resultado = 10 / 0

    except ZeroDivisionError as error:
        # Capturar el error y registrarlo
        print(f"Error capturado correctamente: {error}")
        registrar_error(f"Prueba de división entre cero: {error}")

    finally:
        print("Finalizó la prueba de captura de errores.")
    # ==========================================
    # PRUEBA DE REGISTRO DE EVENTOS
    # ==========================================

    print("\nPRUEBA DE REGISTRO DE EVENTOS")

    try:
        # Registrar un evento de prueba
        registrar_evento("Verificación del sistema de registros.")

        # Registrar un error de prueba
        registrar_error("Error de prueba para verificar el archivo.")

        # Comprobar que el archivo exista
        if ARCHIVO_LOG.exists():
            print("Archivo de registros encontrado correctamente.")
            print(f"Ubicación: {ARCHIVO_LOG}")
        else:
            print("No se encontró el archivo de registros.")

    except Exception as error:
        print(f"Error al verificar los registros: {error}")
    # ==========================================
    # PRUEBA DE LECTURA DE REGISTROS
    # ==========================================

    print("\nPRUEBA DE LECTURA DE REGISTROS")

    try:
        # Abrir el archivo en modo lectura
        with open(ARCHIVO_LOG, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        # Comprobar que tenga información
        if contenido.strip():
            print("Registros encontrados correctamente.")
            print("\nContenido del archivo:")
            print(contenido)
        else:
            print("El archivo de registros está vacío.")

    except OSError as error:
        print(f"Error al leer el archivo: {error}")

    # ==========================================
    # PRUEBA DEL GESTOR DE CLIENTES
    # ==========================================

    print("\nPRUEBA DEL GESTOR DE CLIENTES")

    # Crear el gestor de clientes
    gestor_clientes = GestorClientes()

    try:
        # Registrar un cliente
        nuevo_cliente = Cliente(
            "CLI-010", "Andrés Ramírez", "andres@gmail.com", "3111234567"
        )

        print(gestor_clientes.registrar_cliente(nuevo_cliente))

        # Buscar el cliente registrado
        cliente_encontrado = gestor_clientes.buscar_cliente("CLI-010")

        if cliente_encontrado:
            print("Cliente encontrado:")
            print(cliente_encontrado.obtener_resumen())

        # Intentar registrar nuevamente el mismo cliente
        gestor_clientes.registrar_cliente(nuevo_cliente)

    except RegistroDuplicadoError as error:
        print(f"Duplicado controlado correctamente: {error}")
    # ==========================================
    # PRUEBA DEL GESTOR DE SERVICIOS
    # ==========================================

    print("\nPRUEBA DEL GESTOR DE SERVICIOS")

    # Crear el gestor
    gestor_servicios = GestorServicios()

    try:
        # Crear una sala
        sala_gestion = ReservaSala("SER-010", "Sala ejecutiva", 60000, 12)

        # Crear un equipo
        equipo_gestion = AlquilerEquipo("SER-011", "Computador portátil", 45000, 5)

        # Crear una asesoría
        asesoria_gestion = AsesoriaEspecializada(
            "SER-012", "Asesoría tecnológica", 90000, "Tecnología", "Virtual"
        )

        # Registrar los tres servicios
        print(gestor_servicios.registrar_servicio(sala_gestion))
        print(gestor_servicios.registrar_servicio(equipo_gestion))
        print(gestor_servicios.registrar_servicio(asesoria_gestion))

        # Listar los servicios registrados
        print("\nServicios registrados:")

        for servicio in gestor_servicios.listar_servicios():
            print(servicio.describir())

        # Buscar un servicio
        servicio_encontrado = gestor_servicios.buscar_servicio("SER-011")

        if servicio_encontrado:
            print("\nServicio encontrado:")
            print(servicio_encontrado.obtener_resumen())

    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # ==========================================
    # PRUEBA DEL GESTOR DE RESERVAS
    # ==========================================

    print("\nPRUEBA DEL GESTOR DE RESERVAS")

    # Crear el gestor de reservas
    gestor_reservas = GestorReservas()

    try:
        # Crear un cliente
        cliente_gestion = Cliente(
            "CLI-020", "María González", "maria@gmail.com", "3121234567"
        )

        # Crear un servicio
        servicio_gestion = ReservaSala("SER-020", "Sala de reuniones", 50000, 10)

        # Crear una reserva
        reserva_gestion = Reserva("RES-020", cliente_gestion, servicio_gestion, 2)

        # Registrar la reserva
        print(gestor_reservas.registrar_reserva(reserva_gestion))

        # Buscar la reserva
        reserva_encontrada = gestor_reservas.buscar_reserva("RES-020")

        if reserva_encontrada:
            print("\nReserva encontrada:")
            print(reserva_encontrada.obtener_resumen())

        # Consultar todas las reservas
        print("\nCantidad de reservas registradas:")
        print(len(gestor_reservas.listar_reservas()))

    except ErrorSistema as error:
        print(f"Error controlado: {error}")

    # ==========================================
    # PRUEBA DEL CONTADOR DE RESULTADOS
    # ==========================================

    print("\nPRUEBA DEL CONTADOR DE RESULTADOS")

    # Registrar dos pruebas exitosas
    registrar_resultado_prueba(
        "Registro de clientes", True, "Cliente registrado correctamente."
    )

    registrar_resultado_prueba(
        "Registro de servicios", True, "Servicio registrado correctamente."
    )

    # Obtener el resumen
    resumen = obtener_resumen_pruebas()

    # Mostrar los resultados
    print(f"Total de pruebas: {resumen['total']}")
    print(f"Pruebas exitosas: {resumen['exitosas']}")
    print(f"Pruebas fallidas: {resumen['fallidas']}")
    # ==========================================
    # PRUEBA DE REGISTRO DE UNA FALLA
    # ==========================================

    print("\nPRUEBA DE REGISTRO DE UNA FALLA")

    # Registrar una prueba fallida
    registrar_resultado_prueba(
        "Validación de correo", False, "El correo no cumple con el formato requerido."
    )

    # Consultar nuevamente el resumen
    resumen = obtener_resumen_pruebas()

    # Mostrar los resultados actualizados
    print(f"Total de pruebas: {resumen['total']}")
    print(f"Pruebas exitosas: {resumen['exitosas']}")
    print(f"Pruebas fallidas: {resumen['fallidas']}")

    # ==========================================
    # PRUEBA DE CONSULTA DE RESULTADOS
    # ==========================================

    print("\nDETALLE DE LAS PRUEBAS REGISTRADAS")

    listar_resultados_pruebas()

    # Iniciar la interfaz gráfica
    iniciar_interfaz()
