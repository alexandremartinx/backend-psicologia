from flask import Blueprint, jsonify, request
from services.jwt_handler import get_token_payload_by_request
from config import db, auth_guard_swag
from services.utils import validate_required_fields_exists
import os
import datetime

psicologos = Blueprint('psicologos', __name__, url_prefix='/psicologos')

"""
TODO:
1. Padronizar nomenclatura dos endpoints e tags do swagger (sugestao endpoints e funcs: ingles)
2. Padronizar consultas para o Supabase, query/functions (sugestao: queries, pois controlamos os campos de retorno)
3. Separar o POST de atendimento em etapas de cadastro 
    - ADD endpoint GetCollaboratorByNameAndCompanyID (match com nome fornecido sem mostrar listagem) - etapa 1
    - endpoint para inserir os dados no db de fato (formik form no front talvez facilite)
"""

@psicologos.route('/colaboradores', methods=['GET'])
@auth_guard_swag('psicologos', 'psicologos/get_colaboradores.yml')
def get_colaboradores():
    auth_payload = get_token_payload_by_request(request)
    empresa_id = auth_payload['empresa_id']

    response = db.from_('colaboradores').select(
        'id_colaborador',
        'nome',
        'setor',
        'cargo',
        'unidade',
        'observacoes'
    ).eq('id_empresa', empresa_id).execute()

    return jsonify(response.data)

@psicologos.route('/services', methods=['GET'])
@auth_guard_swag('psicologos', 'psicologos/get_services.yml')
def get_services():
    auth_payload = get_token_payload_by_request(request)
    user_id = auth_payload['user_id']

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "start_date ou end_date não fornecidas"}), 400

    try:
        response = db.rpc('get_services', {
            'psicologo_id': user_id,
            'start_date': start_date,
            'end_date': end_date
        }).execute()

        return jsonify(response.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@psicologos.route('/actions/total-value', methods=['GET'])
@auth_guard_swag('psicologos', 'psicologos/get_actions_total_value.yml')
def get_actions_total_value():
    auth_payload = get_token_payload_by_request(request)
    user_id = auth_payload['user_id']

    data_atual = datetime.datetime.now()
    primeiro_dia_do_mes = datetime.datetime(data_atual.year, data_atual.month, 1)

    try:
        response_acoes = db.from_('psicologo acoes').select('id_acoes').eq('id_psicologo', user_id).execute()
        id_acoes = [acao['id_acoes'] for acao in response_acoes.data]

        # Busca a remuneração das ações na tabela acoes e calcula o montante total das ações
        montante_total_acoes = sum(db.from_('acoes').select('remuneracao').eq('id', id_acao).execute().data[0]['remuneracao'] for id_acao in id_acoes)

        montante_total = montante_total_acoes
        montante_total_arredondado = round(montante_total, 2)

        return jsonify({
            "actions_total_value": montante_total_arredondado
        })
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}", 500

def _validate_create_service(form_data: dict) -> str|None:
    required_fields = [
        'collaborator_id', 
        'psychologist_id', 
        'company_id', 
        'area', 
        'department', 
        'city',
        'date_of_service',
        'annotations',
        'complaint'
    ]

    err_field = validate_required_fields_exists(required_fields, form_data)
    if err_field:
        return {'error': f'O campo obrigatório "{err_field}" não foi fornecido'}, 400

    return

### TODO revisar esse endpoint
## add validation para evitar repitir dados
## ajustar os nomes, seguir padrao table_atribute, e.g. empresa_id && convem add horario do atendimento na logica da eezycare ?
@psicologos.route('/services', methods=['POST'])
@auth_guard_swag('psicologos', 'psicologos/post_service.yml')
def post_service():
    form_data = request.json
    err = _validate_create_service(form_data)
    if err:
        return err

    try:
        service_insert_form_data = form_data.copy()
        ## rename keys
        service_insert_form_data["fk_collaborator_id"] = service_insert_form_data.pop("collaborator_id")
        service_insert_form_data["fk_psychologist_id"] = service_insert_form_data.pop("psychologist_id")
        service_insert_form_data["fk_company_id"]      = service_insert_form_data.pop("company_id")

        response_valores_empresas = db.from_('valores_empresas').select('valor').eq(
            'id_empresa', service_insert_form_data["fk_company_id"]
            ).single().execute()
        if 'error' in response_valores_empresas:
            return {'error': response_valores_empresas['error']}, 500

        if not response_valores_empresas.data:
            return {'error': f'Valor da empresa com ID "{service_insert_form_data["fk_company_id"]}" não encontrado.'}, 404

        service_insert_form_data['payment_value'] = int(response_valores_empresas.data['valor'])

        response = db.table('services').insert(service_insert_form_data).execute()
        if 'error' in response:
            return {'error': response['error']}, 500

        return {"id": response.data[0]['id']}, 201
    except Exception as e:
        return {'error': str(e)}, 500

@psicologos.route('/actions', methods=['POST'])
@auth_guard_swag('psicologos', 'psicologos/post_actions.yml')
def inserir_acoes_psicologo():
    campos_obrigatorios = ['id_psicologo', 'acao_escolhida', 'data']
    dados_formulario = request.json
    try:
        for campo in campos_obrigatorios:
            if campo not in dados_formulario:
                return {'error': f'O campo obrigatório "{campo}" não foi fornecido.'}, 400

        # Extrai os dados necessários do JSON recebido
        id_psicologo = int(dados_formulario['id_psicologo'])
        id_empresa   = int(dados_formulario['id_empresa'])
        acao_escolhida = dados_formulario['acao_escolhida']
        dia = dados_formulario['data']

        response_id_acao = db.from_('acoes').select('id').eq('acao', acao_escolhida).execute()
        if 'error' in response_id_acao:
            return {'error': response_id_acao['error']}, 500

        id_acao = int(response_id_acao.data[0]['id'])
        
        # Inserir os dados na tabela 'psicologo_acoes'
        data = {'id_psicologo': id_psicologo, 'id_acoes': id_acao, 'data': dia, 'id_empresa': id_empresa}
        response_inserir_acao = db.table('psicologo acoes').insert(data).execute()
        if 'error' in response_inserir_acao:
            return {'error': response_inserir_acao['error']}, 500

        return {}, 201

    except Exception as e:
        return {'error': str(e)}, 500

@psicologos.route('/empresas', methods=['GET'])
@auth_guard_swag('psicologos', 'psicologos/get_empresas.yml')
def get_empresas():
    try:
        response = db.from_("empresas").select('id_empresa', 'empresa').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return {'error': str(e)}, 500

@psicologos.route('/amount', methods=['GET'])
@auth_guard_swag('psicologos', 'psicologos/get_amount.yml')
def ler_valores():
    auth_payload = get_token_payload_by_request(request)
    user_id = auth_payload['user_id']

    data_atual = datetime.datetime.now()
    primeiro_dia_do_mes = datetime.datetime(data_atual.year, data_atual.month, 1)
    try:
        # Converter a data para uma string no formato ISO usando o módulo json
        primeiro_dia_do_mes_str = primeiro_dia_do_mes.isoformat()
    
        # Chamar a função SQL
        response = db.rpc('get_psicologo_montante', {
            'psicologo_id': user_id,
            'primeiro_dia_do_mes': primeiro_dia_do_mes_str
        }).execute()
    
        resultado = response.data[0]
        resultado['montante_total'] = round(resultado['montante_total'], 2)

        # Multiplicar o valor_psi pelo número de atendimentos
        resultado['montante_total_atendimentos'] = resultado['valor_psi'] * resultado['numero_atendimentos']

        resultado['montante_total'] = resultado['montante_total_acoes'] + resultado['montante_total_atendimentos']
        
        # Arredondar o montante total para duas casas decimais
        resultado['montante_total'] = round(resultado['montante_total'], 2)

        return jsonify(resultado)
    except Exception as e:
        return f"Ocorreu um erro: {str(e)}", 500

@psicologos.route('/negotiations', methods=['GET'])
@auth_guard_swag('psicologos', 'psicologos/get_negotiations.yml')
def get_negociacao():
    try:
        response = db.rpc('get_negociacoes').execute()
        negociacoes = response.data
        return negociacoes
    except Exception as e:
        return {'error': str(e)}, 500

@psicologos.route('/actions', methods=['GET'])
@auth_guard_swag('psicologos', 'psicologos/get_actions.yml')
def get_actions():
    try:
        response = db.from_('acoes').select('*').execute()
        acoes = response.data
        return acoes
    except Exception as e:
        return {'error': str(e)}, 500

