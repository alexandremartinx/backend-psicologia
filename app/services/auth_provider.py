from config import db

def authenticate(email, password):
    """
    Authenticate the user on the system
    The supabase client should already sanitize the parameters
    """

    response_user = db.from_("users").select(
        "id", 
        "fk_empresa_id", 
        "name"
    ).eq('email', email).eq('password', password).single().execute()

    if not response_user.data:
        return False
    
    user_info = response_user.data

    response_permission = db.from_("user_permissions").select(
        "permissions(name)"
    ).eq("user_id", user_info['id']).execute()

    if not response_permission.data:
        return False

    return {
        "user_id": user_info['id'],
        "empresa_id": user_info['fk_empresa_id'],
        "name": user_info['name'],
        "scp": [item['permissions']['name'] for item in response_permission.data]
    }