from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def analytics(request):
    return render(request, 'analytics/web-analytics-real-time.html')

def overview(request):
    return render(request, 'analytics/web-analytics-overview')

