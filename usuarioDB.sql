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



GRANT ALL PRIVILEGES TO C##novashiftadmin;