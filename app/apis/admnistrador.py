from flask import Blueprint, jsonify, request
from services.utils import validate_required_fields_exists
from config import db, auth_guard_swag

"""
TODO: 
1. Refatorar nomenclatura (sugestao: seguir com ingles)
"""

admnistrador = Blueprint('admnistrador', __name__, url_prefix='/admnistrador')

def _validate_negociation_form(form_data: dict) -> str|None:
    required_fields = ['id_empresa', 'consultas_pagas']
    err_field = validate_required_fields_exists(required_fields, form_data)
    if err_field:
        return {'error': f'O campo obrigatório "{err_field}" não foi fornecido'}, 400

    return

## TODO: review this
def _validate_user_form(form_data: dict) -> str|None:
    required_fields = ['email', 'senha', 'nome', 'ocupacao', 'id_empresa', 'valor']
    err_field = validate_required_fields_exists(required_fields, form_data)
    if err_field:
        return {'error': f'O campo obrigatório "{err_field}" não foi fornecido'}, 400

    return

@admnistrador.route('/negociations', methods=['POST'])
@auth_guard_swag('admin', 'admin/post_negotiations.yml')
def post_negociation():
    form_data = request.json
    err = _validate_negociation_form(form_data)
    if err:
        return err

    response = db.from_('negociacoes_empresa').insert(form_data).execute()
    if 'error' in response:
        return jsonify({'error': response['error']}), 500

    return {"id": response.data[0]['id']}, 201

@admnistrador.route('/users', methods=['POST'])
@auth_guard_swag('admin', 'admin/post_user.yml')
def post_user():
    form_data = request.json
    err = _validate_user_form(form_data)
    if err:
        return err

    response = db.from_('users').insert(form_data).execute()
    if 'error' in response:
        return {'error': response['error']}, 500

    return {'id': response.data[0]['id']}, 200
        
@admnistrador.route('/users/<ID>', methods=['PUT'])
@auth_guard_swag('admin', 'admin/put_user.yml')
def put_user(ID: str):
    try:
        ID = int(ID)
    except TypeError:
        return {"error": "path param ID should be a integer"}, 400
    
    form_data = request.json
    err = _validate_user_form(form_data)
    if err:
        return err

    response = db.from_('users').update(form_data).eq('id', ID).execute()
    if 'error' in response:
        return jsonify({'error': response['error']}), 500

    return {}, 204

@admnistrador.route('/colaboradores/<colaboradorID>/services', methods=['GET'])
@auth_guard_swag('admin', 'admin/get_collaborator_services.yml')
def get_collaborator_services(colaboradorID: str):
    try:
        colaboradorID = int(colaboradorID)
    except TypeError:
        return {"error": "path param colaboradorID should be a integer"}, 400

    try:
        response_atendimentos = db.from_('atendimentos').select(
            'id_atendimento',
            'psicologo',
            'empresa',
            'area',
            'setor',
            'cidade',
            'atendimento',
            'observacoes',
            'queixa_inicial',
        ).eq('colaborador', colaboradorID).execute()

        response_colaborador = db.from_('colaboradores').select(
            'nome'
        ).eq('id_colaborador', colaboradorID).single().execute()

        for atendimento in response_atendimentos.data:
            atendimento['colaborador'] = response_colaborador.data['nome']

        return jsonify(atendimentos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
