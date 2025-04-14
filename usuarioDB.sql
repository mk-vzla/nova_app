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


-------------------------------------------------------------
--Población de tabla rol
insert into core_rol (identificador,nombre) values (1,'ADMINISTRADOR');
insert into core_rol (identificador,nombre) values (2,'JUGADOR');
insert into core_rol (identificador,nombre) values (3,'DESARROLLADOR');

-------------------------------------------------------------
--Query consulta de usuarios
SELECT * FROM core_usuario usu JOIN core_rol rol ON usu.rol_id = rol.identificador;