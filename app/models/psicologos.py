# import supabase
# from .model import database_client

# '''
# public.colaboradores (
#     id_colaborador serial,
#     nome character varying null,
#     setor character varying null,
#     cargo character varying null,
#     observacoes character varying null,
#     id_empresa integer null,
#     unidade text null default 'LEME'::text,
#     constraint colaboradores_pkey primary key (id_colaborador),
#     constraint colaboradores_id_empresa_fkey foreign key (id_empresa) references empresas (id_empresa)
#   ) tablespace pg_default;
# '''
# class PsicologosModel:
#     def get_all_colaboradores():
#         return database_client.from_("users").select('''
#             id_colaborador,
#             nome,
#             setor,
#             cargo,
#             observacoes,
#             id_empresa,
#             unidade
#         ''').execute() ## TODO map return


from config import db

class PsicologosModel(db.model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    setor = db.Column(db.String)
    cargo = db.Column(db.String)
    observacoes = db.Column(db.String)
    id_empresa = db.Column(db.Integer)
    unidade = db.Column(db.String)

    def get_all_colaboradores():
        return database_client.from_("users").select('''
            id_colaborador,
            nome,
            setor,
            cargo,
            observacoes,
            id_empresa,
            unidade
        ''').execute() ## TODO map return
