import os
import supabase

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
database_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)