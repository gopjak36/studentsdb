# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import forms
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# switch on status message:
from django.contrib import messages    #Not use with FormView
from django.contrib.messages.views import SuccessMessageMixin

from studentsdb.settings import ADMIN_EMAIL

# Class for Contact Admin:
class ContactForm(forms.Form):

    def __init__(self,*args,**kwargs):
    # Crispy Forms settings for contact form

        # call originall initializator:
        super(ContactForm, self).__init__(*args, **kwargs)

        # this helper object allows us to customize form:
        self.helper = FormHelper()

        # form tag attrubutes:
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.from_action = reverse('contact_admin')

        # bootstrap styles:
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # form button:
        self.helper.add_input(Submit('send_button', u"Надіслати"))

    from_email = forms.EmailField(
                label=u"Ваша Емейл Адресса")

    subject = forms.CharField(
                label=u"Заголовок Листа",
                max_length=128)

    message = forms.CharField(
                label=u"Текст Повідомлення",
                max_length=2560,
                widget=forms.Textarea)

    def send_mail(self):

        # add data using the self.cleaned_data dictionary:
        subject = self.cleaned_data['subject']
        from_email = self.cleaned_data['from_email']
        message = self.cleaned_data['message'] # Not necessary in SendGrid, can see from email + u"  From Email: " + from_email

        # send email:
        send_mail(subject, message, from_email, [ADMIN_EMAIL])

# Views For Contact Admin:
class ContactView(SuccessMessageMixin,FormView):

    template_name = 'contact_admin/form.html'
    form_class = ContactForm
    success_url = '/contact-admin/'
    # status message of send mail:
    success_message = 'Повідомлення успішно надіслане!'

    def form_valid(self, form):
        # valid form:
        form.send_mail()
        
        return super(ContactView, self).form_valid(form)

'''
# Just a method for ContactForm class

# Views For Contact Admin:
def contact_admin(request):

    # Check if form posted:
    if request.method == 'POST':

        # Create a form instance and populate it with data from request:
        form = ContactForm(request.POST)

        # Check whether user data is valid:
        if form.is_valid():

            # add data:
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] # Not necessary in SendGrid, can see from email + u"  From Email: " + from_email

            # send email:
            try:
                send_mail(subject, message, from_email, [ADMIN_EMAIL])
            except Exception:
                messages.error(request,"Під час відправки листа виникла непередбачувана помилка. Спробуйте скористатись даною формою пізніше.")
            else:
                messages.error (request,"Повідомлення успішно надіслане!")

            # Redirect to contact page with message:
            return HttpResponseRedirect(reverse('contact_admin'))

    # if there not Post render blank form:
    else:
        form = ContactForm()

    return render(request, 'contact_admin/form.html', {'form': form})
'''
