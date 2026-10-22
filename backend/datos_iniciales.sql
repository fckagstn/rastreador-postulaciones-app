INSERT INTO estados (nombre_estado) VALUES
    ('postulado'),
    ('rechazado'),
    ('entrevista'),
    ('oferta') 
ON CONFLICT (nombre_estado) DO NOTHING; 

INSERT INTO modalidad (nombre) VALUES 
    ('presencial'),
    ('remoto'),
    ('híbrido') 
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO mercado (nombre) VALUES
    ('local'),
    ('nacional'),
    ('nearshore'),
    ('offshore') 
ON CONFLICT (nombre) DO NOTHING;
