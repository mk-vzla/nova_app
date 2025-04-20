CREATE USER C##novashiftadmin IDENTIFIED BY "NuevaClave123"
  DEFAULT TABLESPACE "USERS"
  TEMPORARY TABLESPACE "TEMP";

-- Definir cuotas de espacio en tablespace
ALTER USER C##novashiftadmin QUOTA UNLIMITED ON USERS;

-- Asignar roles
GRANT "RESOURCE" TO C##novashiftadmin;
GRANT "CONNECT" TO C##novashiftadmin;

-- Establecer roles por defecto
ALTER USER C##novashiftadmin DEFAULT ROLE "RESOURCE", "CONNECT";
-- Darle todos los permisos
GRANT ALL PRIVILEGES TO C##novashiftadmin;


------------------------------------------------------------- Poblacion de tablas
--Población de tabla rol
insert into core_rol (identificador,nombre) values (1,'ADMINISTRADOR');
insert into core_rol (identificador,nombre) values (2,'JUGADOR');
insert into core_rol (identificador,nombre) values (3,'DESARROLLADOR');
commit;
--Población de tabla categoría
INSERT INTO core_categoria (nombre_categoria) VALUES ('Terror');
INSERT INTO core_categoria (nombre_categoria) VALUES ('Acción');
INSERT INTO core_categoria (nombre_categoria) VALUES ('Mundo Abierto');
INSERT INTO core_categoria (nombre_categoria) VALUES ('Free To Play');
INSERT INTO core_categoria (nombre_categoria) VALUES ('Supervivencia');
commit;
-- Población de tabla plataforma
INSERT INTO core_plataforma (nombre_plataforma) VALUES ('Steam');
INSERT INTO core_plataforma (nombre_plataforma) VALUES ('Epic Games');
INSERT INTO core_plataforma (nombre_plataforma) VALUES ('Origin');
INSERT INTO core_plataforma (nombre_plataforma) VALUES ('Battle.net');
INSERT INTO core_plataforma (nombre_plataforma) VALUES ('PSN');
INSERT INTO core_plataforma (nombre_plataforma) VALUES ('Xbox');
INSERT INTO core_plataforma (nombre_plataforma) VALUES ('Nintendo');
commit;
-------------------------------------------------------------
--Query consulta de usuarios
SELECT * FROM core_usuario usu JOIN core_rol rol ON usu.rol_id = rol.identificador;




------------------------------------------------------------- Eliminación de tablas y todo
-- Primero eliminamos las tablas que dependen de otras
DROP TABLE CORE_COMPRA CASCADE CONSTRAINTS;
DROP TABLE CORE_CARRITO CASCADE CONSTRAINTS;
DROP TABLE CORE_JUEGO CASCADE CONSTRAINTS;

-- Luego las que son referenciadas por CORE_JUEGO
DROP TABLE CORE_CATEGORIA CASCADE CONSTRAINTS;
DROP TABLE CORE_PLATAFORMA CASCADE CONSTRAINTS;

-- CORE_USUARIO depende de CORE_ROL
DROP TABLE CORE_USUARIO CASCADE CONSTRAINTS;
DROP TABLE CORE_ROL CASCADE CONSTRAINTS;

-- Eliminar las migraciones de Django
DROP TABLE django_migrations CASCADE CONSTRAINTS;
commit;
-- Eliminar las tablas de Django
BEGIN
  FOR t IN (SELECT table_name FROM user_tables) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
END;
/
commit;