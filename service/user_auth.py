from service.supabase_client import get_supabase_client


def login_user(email: str, password: str) -> dict:
    sb = get_supabase_client()
    

def register_user(email: str, password: str) -> dict:
    sb = get_supabase_client()
    sb.auth.sign_up(email=email.lower().strip(), password=password)
    doc = {"email": email.lower().strip(), "password": password}
    result = sb.table("users").insert(doc).execute()
    
