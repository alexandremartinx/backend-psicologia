--- EMPRESA ---
-- Rename existing columns
ALTER TABLE empresas RENAME COLUMN id_empresa TO id;
ALTER TABLE empresas RENAME COLUMN empresa TO trade_name;
ALTER TABLE empresas RENAME COLUMN representante TO responsible;
ALTER TABLE empresas RENAME COLUMN cnpj TO document;
ALTER TABLE empresas RENAME COLUMN plano TO subscription;

-- Add new columns
ALTER TABLE empresas ADD COLUMN social_reason VARCHAR(255);
ALTER TABLE empresas ADD COLUMN document_type VARCHAR(50);

-- Set current document type
UPDATE empresas
SET document_type = 'CNPJ'
WHERE document IS NOT NULL;

-- Document shall be unique
ALTER TABLE empresas ADD CONSTRAINT UX_document_with_type UNIQUE (document, document_type);\

-- Empresas shall be SOFT delete to not lose data of other tables
ALTER TABLE empresas ADD COLUMN deleted_at TIMESTAMP with time zone;
ALTER TABLE empresas ADD COLUMN fk_deleted_by_user_id INTEGER;
ALTER TABLE empresas ADD CONSTRAINT FK_empresas_users_fk_deleted_by_user_id FOREIGN KEY(fk_deleted_by_user_id) REFERENCES users(id);

--- PROFESSIONS ---
ALTER TABLE profissoes RENAME TO professions;
ALTER TABLE professions RENAME COLUMN id_profissao TO id;
ALTER TABLE professions RENAME COLUMN profissao TO name;

---- USUARIOS ----
-- Users cannot have same email
ALTER TABLE usuarios ADD CONSTRAINT UX_users_email UNIQUE (email);

-- Rename existing columns
ALTER TABLE usuarios RENAME COLUMN nome TO name;
ALTER TABLE usuarios RENAME COLUMN senha TO password;
ALTER TABLE usuarios RENAME COLUMN ocupacao TO fk_profession_id;
ALTER TABLE usuarios RENAME COLUMN id_empresa TO fk_empresa_id;
ALTER TABLE usuarios RENAME COLUMN valor TO monthly_payment_value;

-- Rename constrains
ALTER TABLE usuarios DROP CONSTRAINT usuarios_ocupacao_fkey;
ALTER TABLE usuarios ADD CONSTRAINT FK_users_professions_fk_profession_id FOREIGN KEY(fk_profession_id) REFERENCES professions(id);

-- Rename Table
ALTER TABLE usuarios RENAME TO users;

-- Removing old token
ALTER TABLE users DROP COLUMN token; 


---- ATENDIMENTOS ----
ALTER TABLE atendimentos RENAME TO services;

-- Rename existing columns
ALTER TABLE services RENAME COLUMN id_atendimento TO id;
ALTER TABLE services RENAME COLUMN colaborador TO fk_collaborator_id;
ALTER TABLE services RENAME COLUMN psicologo TO fk_psychologist_id;
ALTER TABLE services RENAME COLUMN empresa TO fk_company_id;
ALTER TABLE services RENAME COLUMN setor TO department;
ALTER TABLE services RENAME COLUMN cidade TO city;
ALTER TABLE services RENAME COLUMN atendimento TO date_of_service;
ALTER TABLE services RENAME COLUMN observacoes TO annotations;
ALTER TABLE services RENAME COLUMN queixa_inicial TO complaint;
ALTER TABLE services RENAME COLUMN valor TO payment_value;


