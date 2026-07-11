from django.shortcuts import render
from maintenance.models import Alert
from datetime import datetime

def dashboard_view(request):
    return render(request, "dashboard.html")

def alerts_view(request):
    # This might fail if the user hasn't run the migrations yet.
    # We should handle it gracefully just in case.
    try:
        alerts = Alert.objects.all()
        
        # Filter by urgency
        urgency = request.GET.get('urgency')
        if urgency:
            alerts = alerts.filter(urgency=urgency)
            
        # Filter by date
        date_str = request.GET.get('date')
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                alerts = alerts.filter(timestamp__date=date_obj)
            except ValueError:
                pass
    except Exception:
        alerts = []
        urgency = None
        date_str = None
        
    context = {
        'alerts': alerts,
        'current_urgency': urgency,
        'current_date': date_str,
    }
    return render(request, "alerts_list.html", context)
