# -*- coding:utf-8 -*-
from django.shortcuts import render
from django import forms
from django.core.mail import mail
from django.http import HttpResponseRedirect
from django.core.urlresolves import reverse

from studentsdb.settings import ADMIN_EMAIL

# Class for Contact Admin
class ContacForm(forms.form):

    from_email = forms.EmailField(
                label=u"Ваша Емейл Адресса")

    subject = forms.CharField(
                label=u"Заголовок Листа",
                max_length=128)

    message = forms.CharField(
                label=u"Текст Повідомлення",
                max_length=2560,
                widget=forms.Textarea)

# Views For Contact Admin
def contact_admin(request):

    # Check if form posted:
    if request.method == 'POST':

        # Create a form instance and populate it with data from request:
        form = ContactForm(request.POST)

        # Check whether user data is valid:
        if form.is_valid():

            # add data:
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']

            # send email:
            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                message = u"Під час відправки листа виникла непередбачувана помилка. Спробуйте скористатись даною формою пізніше."
            else:
                message = u"’Повідомлення успішно надіслане!"

            # Redirect to contact page with message:
            return HttpResponseRedirect(u"%?status_message=%" % (reverse('contac_admin'), message))

    # if there not Post render blank form:
    else:
        form = ContactForm()

    return render(request, 'contact_admin/form.html', {'form': form})
