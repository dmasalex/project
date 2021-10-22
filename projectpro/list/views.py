from django.contrib.auth import authenticate, login, logout
from django.forms import inlineformset_factory
from django.http import HttpResponse, FileResponse
from django.views.generic import View
from .forms import OrganizationForm, PersonForm
from .forms import LoginForm
from django.forms.models import model_to_dict
from docxtpl import DocxTemplate
import subprocess
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime

from .models import *
from .utils import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


def persons_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        persons = Person.objects.filter(name__icontains=search_query)
    else:
        persons = Person.objects.all()

    paginator = Paginator(persons, 10)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        "is_paginated": is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    if request.user.is_authenticated:
        return render(request, 'list/index.html', context=context)
    else:
        return redirect('login')


class PersonDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Person
    template = 'list/person_detail.html'
    raise_exception = True


class PersonCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = PersonForm
    template = 'list/person_create_form.html'
    raise_exception = True


class PersonUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Person
    model_form = PersonForm
    template = 'list/person_update_form.html'
    raise_exception = True


class PersonDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Person
    template = 'list/person_delete_form.html'
    redirect_url = 'persons_list_url'
    raise_exception = True


class OrganizationDetail(LoginRequiredMixin, ObjectDetailMixin, View):
    model = Organization
    template = 'list/organization_detail.html'
    raise_exception = True


class OrganizationUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Organization
    model_form = OrganizationForm
    template = 'list/organization_update_form.html'
    raise_exception = True


class OrganizationCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    model_form = OrganizationForm
    template = 'list/organization_create.html'
    raise_exception = True


class OrganizationDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Organization
    template = 'list/organization_delete_form.html'
    redirect_url = 'organizations_list_url'
    raise_exception = True


def organizations_list(request):
    organizations = Organization.objects.all()

    paginator = Paginator(organizations, 15)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        "is_paginated": is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    if request.user.is_authenticated:
        return render(request, 'list/organizations_list.html', context=context)
    else:
        return redirect('login')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('persons_list_url')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'list/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contacts_list(request):
    contacts = Contacts.objects.all()

    paginator = Paginator(contacts, 15)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    context = {
        'page_object': page,
        "is_paginated": is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    if request.user.is_authenticated:
        return render(request, 'list/contacts_list.html', context=context)
    else:
        return redirect('login')


def modification(request, slug):
    organization = Organization.objects.get(slug=slug)
    ContactsFormset = inlineformset_factory(Organization, Contacts, fields=('email',), extra=1)

    if request.method == 'POST':
        formset = ContactsFormset(request.POST, instance=organization)
        if formset.is_valid():
            formset.save()
            return redirect('modification_url', slug=organization.slug)

    formset = ContactsFormset(instance=organization)

    return render(request, "list/modification.html", {'formset': formset})


def createlist(request, slug):
    now = datetime.now().date()
    date_now = now.strftime('%d.%m.%Y')

    organisation = Organization.objects.get(slug=slug)  # оргнанизация
    pers_org = model_to_dict(organisation)['name']  # название организации
    persons = Person.objects.all()
    pdf_name = model_to_dict(organisation)['slug'] + '.docx'

    pers = persons.filter(organization__name=pers_org)  # список сотрудников имеющих доступ к организации

    # В папке tempdoc лежат шаблоны
    #tempdir = r'C:\Users\DAnilovAV\PycharmProjects\new_project\projectpro\projectpro\tempdoc'
    tempdir = '/home/admsrv/new_project.v2/projectpro/projectpro/tempdoc'
    doc = DocxTemplate(os.path.join(tempdir, pdf_name))

    lst_pers = []

    for p in pers:
        lst_pers.append(model_to_dict(p))

    for row in lst_pers:
        date_is = row['date_of_issue']
        date_bir = row['date_of_birth']
        if date_is == None:
            row['date_of_issue'] = ''
            date_birth = '.'.join((str(date_bir).split('-'))[::-1])
            row['date_of_birth'] = date_birth
        else:
            date_issue = '.'.join((str(date_is).split('-'))[::-1])
            date_birth = '.'.join((str(date_bir).split('-'))[::-1])
            row['date_of_birth'] = date_birth
            row['date_of_issue'] = date_issue

    data_print = {'pers': lst_pers, 'today': date_now}

    doc.render(data_print)
    pdf_name = model_to_dict(organisation)['slug'] + 'PDF' + '.docx'
    doc.save(os.path.join(pdf_name))

    #subprocess.call(f'"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf {pdf_name} --outdir ./')

    subprocess.call(['libreoffice', '--headless', '--convert-to', 'pdf', f'{pdf_name}'])

    pdf_name = model_to_dict(organisation)['slug'] + 'PDF' + '.pdf'

    context = {'slug': slug}

    response = FileResponse(open(pdf_name, 'rb'))
    return response


def sendmail(request, slug):
    date_now = datetime.now().date()
    organisation = Organization.objects.get(slug=slug)  # получили организацию
    name_org = model_to_dict(organisation)['name']  # название организации
    org_sender = model_to_dict(organisation)['sender']
    cont = Contacts.objects.all()
    cont_mail = cont.filter(organization__name=name_org)

    send_to = []  # список адресов для отправки
    for c in cont_mail:
        send_to.append(model_to_dict(c)['email'])

    user = 'dav@it-service.io'
    password = '8aacyE8B'

    server = "mx.gblnet.ru"
    mail_username = "rvv@gblnet.ru"  # адрес отправителя

    context = {'slug': slug}

    if send_to == []:
        return render(request, "list/notsendmail.html", context=context)

    cc = ["rvv@gblnet.ru", 'svg@gblnet.ru', 'sechkin@gblnet.ru', 'dav@it-service.io']
    msg = MIMEMultipart()
    msg['From'] = mail_username
    msg['To'] = ",".join(send_to)
    msg['Cc'] = ",".join(cc)
    msg['Subject'] = f'Список доступа на {date_now.year} г. от {org_sender}.'
    text = f'Добрый день. Просьба принять список доступа на {date_now.year} г. от {org_sender}.\n\nBest regards,\nRusin Vladimir.\n"GlobalNet" LLC.\ntel.: +7 (950)027-79-77\n+7 (921)858-00-24\ne-mail: rvv@gblnet.ru\nTelegram: @RusinVladimir'

    msg.attach(MIMEText(text))

    try:
        pdf_name = model_to_dict(organisation)['slug'] + 'PDF' + '.pdf'  # ищем файл для отправки
        files = []
        files.append(pdf_name)

        for f in files:
            with open(f, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=os.path.basename(f))
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
            msg.attach(part)

    except Exception:
        return render(request, "list/notfilemail.html", context=context)

    try:
        smtp = smtplib.SMTP(server)
        smtp.ehlo()

        if smtp.has_extn('STARTTLS'):
            smtp.starttls()
            smtp.ehlo()

        send_to.extend(cc)
        smtp.login(user, password)
        smtp.sendmail(mail_username, send_to, msg.as_string())
        smtp.close()
    except:
        return render(request, "list/notlogin.html", context=context)

    return render(request, "list/sendmail.html", context=context)
