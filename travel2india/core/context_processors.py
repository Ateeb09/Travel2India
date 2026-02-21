from datetime import datetime

def site_context(request):
    return {'year': datetime.now().year}
