from django.shortcuts import render

# Views For Contact Admin

def contact_admin(request):
    return render(request, 'contact_admin/form.html', {})
