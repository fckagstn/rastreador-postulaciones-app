// =========USUARIOS ENTRADA Y SALIDA=============
export interface UsuarioEntrada{
    nombre: string;
    apellidos: string;
    correo: string;
    contrasena: string;
}

export interface UsuarioSalida{
    id: number;
    nombre: string;
    correo: string;
}
// =========PORTALES ENTRADA Y SALIDA============
export interface PortalEntrada{
    nombre_portal: string;
}

export interface PortalSalida{
    id: number;
    nombre_portal: string;
}

// ==========CATALOGOS SALIDAS===============
export interface EmpresaSalida{
    id: number;
    nombre_empresa: string;
}

export interface MercadoSalida{
    id: number;
    nombre: string;
}

export interface ModalidadSalida{
    id: number;
    nombre: string;
}

// # =========POSTULACIONES ENTRADA ,SALIDA==========
export interface PostulacionEntrada{
    puesto: string;
    sueldo_centavos: number | null;
    empresa: string;
    portal: string | null;
    mercado_id: number | null;
    modalidad_id: number | null;
    fecha_postulacion: Date;
}

export interface PostulacionSalida{
    id: number;
    puesto: string;
    sueldo_centavos: number | null;
    empresa: EmpresaSalida;
    estado: EstadoSalida;
    portal: PortalSalida;
    mercado: MercadoSalida | null;
    modalidad: ModalidadSalida | null;
    fecha_postulacion: Date
}

// =============ESTADO ENTRADA Y SALIDA===============
export interface EstadoEntrada{
    estado: string;
}

export interface EstadoSalida{
    id: number;
    nombre_estado: string;
}

// ==========LOGIN ENTRADA==============
export interface LoginEntrada{
    correo: string;
    contrasena: string;
}

// =========HISTORIAL SALIDA=========
export interface HistorialSalida{
    id: number;
    estado: EstadoSalida;
    fecha: Date;
}