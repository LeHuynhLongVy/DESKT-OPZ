from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
import sys, os
from django.core.paginator import Paginator
from django.core.cache import cache
# from django.conf import settings
sys.path.append(os.path.join(sys.path[0],'demo','build_utility'))

import build_pc
from build_sbs import BuildStepByStep
import data_test
from pc import Pc
from db_utility import GetItemFromDatabase
from utility import utility
from pdf_util import PcToPdf

class CpuForm(forms.Form):
    name = forms.CharField(required=False, label="CPU Name", widget=forms.TextInput(attrs={'placeholder': 'Enter CPU Name'}))
    oc = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No'), ('None', 'Any')), initial='None', label="Overclock?")
    brand_manual = forms.ChoiceField(choices=(('Intel', 'Intel'), ('AMD', 'AMD'), ('None', 'Any')), initial='None',
                                     label="CPU Brand")


class BoardForm(forms.Form):
    name = forms.CharField(required=False, label="Mainboard Name", widget=forms.TextInput(attrs={'placeholder': 'Enter Mainboard Name'}))
    cpu_supported = forms.ChoiceField(choices=(('Intel', 'Intel'), ('AMD', 'AMD'), ('None', 'Any')), initial='None',
                                      label="Supported CPU")
    oc = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No'), ('None', 'Any')), initial='None', label="Overclock?")
    form = forms.ChoiceField(choices=(('ATX', 'ATX'), ('Micro-ATX', 'Micro-ATX'), ('None', 'Any')), initial='None',
                             label="Mainboard Form Factor")


class GpuForm(forms.Form):
    name = forms.CharField(label="GPU Name",required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter GPU Name'}))


class RamForm(forms.Form):
    name = forms.CharField(required=False, label="RAM Name", widget=forms.TextInput(attrs={'placeholder': 'Enter RAM Name'}))
    kit = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No'), ('None', 'Any')), initial='None', label="Ram Kit")
    amount = forms.ChoiceField(choices=(
        ('4', '4GB'), ('8', '8GB'), ('16', '16GB'), ('32', '32GB'), ('64', '64GB'), ('128', '128GB'), ('None', 'Any')),
        initial='None', label="Module")


class SsdForm(forms.Form):
    name = forms.CharField(required=False, label="SSD Name", widget=forms.TextInput(attrs={'placeholder': 'Enter SSD Name'}))
    amount = forms.ChoiceField(choices=(
        ('120gb', '120GB'), ('250gb', '250GB'), ('500gb', '500GB'), ('1tb', '1TB'), ('2tb', '2TB'), ('4tb', '4TB'), ('None', 'Any')),
        initial='None', label="SSD Capacity")


class HddForm(forms.Form):
    name = forms.CharField(required=False, label="HDD Name", widget=forms.TextInput(attrs={'placeholder': 'Enter HDD Name'}))
    amount = forms.ChoiceField(choices=(
        ('100gb', '100GB'), ('200gb', '200GB'), ('500gb', '500GB'), ('1tb', '1TB'), ('2tb', '2TB'), ('3tb', '3TB'),
        ('4tb', '4TB'), ('6tb', '6TB'), ('8tb', '8TB'), ('10tb', '10TB'), ('12tb', '12TB'), ('None', 'Any')),
        initial='None', label="HDD Capacity")


class PsuForm(forms.Form):
    name = forms.CharField(required=False, label="PSU Name", widget=forms.TextInput(attrs={'placeholder': 'Enter PSU Name'}))
    form = forms.ChoiceField(choices=(('ATX', 'ATX'), ('SFX', 'SFX'), ('None', 'Any')), initial='None',
                             label="PSU Form Factor")
    watt = forms.CharField(empty_value='None', required=False, label="PSU Wattage", widget=forms.TextInput(attrs={'placeholder': 'Enter PSU Wattage'}))


class CaseForm(forms.Form):
    name = forms.CharField(required=False, label="Case Name", widget=forms.TextInput(attrs={'placeholder': 'Enter Case Name'}))
    form = forms.ChoiceField(choices=(('ATX', 'ATX'), ('Micro-ATX', 'Micro-ATX'), ('None', 'Any')), initial='None',
                             label="Case Form Factor")


class PcAutoBuildForm(forms.Form):
    purpose = forms.ChoiceField(label='Build Purpose',
                                choices=[('gaming', 'Gaming'), ('desktop', 'Desktop'), ('workstation', 'Workstation')])
    budget = forms.CharField(label="Minimum budget", widget=forms.TextInput(attrs={'placeholder': 'Enter Your Maximum Budget'}))
    budget2 = forms.CharField(label="Maximum budget (optional)", required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter Your Minimum Budget'}))
    overclock = forms.ChoiceField(label="Overclockable Platform",
                                  choices=[(True, 'Yes'), (False, 'No'), ('None', 'Any')],
                                  initial='None',
                                  required=False)
    ram = forms.ChoiceField(label="Ram Type", choices=[(True, 'Kit'), (False, 'Single'), ('None', 'Any')],
                            initial='None')
    ram_amount = forms.ChoiceField(
        choices=(('8gb', '8GB'), ('16gb', '16GB'), ('32gb', '32GB'), ('64gb', '64GB'), ('None', 'Any')),
        initial='None', label="Ram Amount")
    storage_ssd = forms.ChoiceField(choices=(
        ('120gb', '120GB'), ('250gb', '250GB'), ('500gb', '500GB'), ('1tb', '1TB'), ('2tb', '2TB'), ('4tb', '4TB'), ('None', 'Any')),
        initial='None', label="SSD Capacity")
    storage_hdd = forms.ChoiceField(choices=(
        ('100gb', '100GB'), ('200gb', '200GB'), ('500gb', '500GB'), ('1tb', '1TB'), ('2tb', '2TB'), ('3tb', '3TB'),
        ('4tb', '4TB'), ('6tb', '6TB'), ('8tb', '8TB'), ('10tb', '10TB'), ('12tb', '12TB'), ('None', 'Any')),
        initial='None', label="HDD Capacity")
    form_factor = forms.ChoiceField(label='Platform Form Factor',
                                    choices=[('ATX', 'Standard ATX'), ('SFX', 'Mini-ATX'), ('None', 'Any')],
                                    initial='None')

    psu = forms.ChoiceField(label="PSU Modularity",
                            choices=[('Modular', 'Modular'), ('Non-modular', 'Non modular'), ('None', 'Any')],
                            initial='None')
    brand = forms.ChoiceField(label="Brand", choices=[('Intel', 'Intel'), ('AMD', 'AMD'), ('None', 'Any')],
                              initial='None')

    def __init__(self, *args, **kwargs):
        super(PcAutoBuildForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



def check_input(x):
    if x == "None":
        return None
    elif x == 'True':
        return True
    elif x == 'False':
        return False
    elif x.isnumeric():
        return int(x)
    else:
        return x


# 	0		self.cpu = None
# 	1		self.board = None
# 	2		self.gpu = None
# 	3		self.ram = None list
# 	4		self.storage_ssd = None list
# 	5		self.storage_hdd = None list
# 	6		self.psu = None
# 	7		self.case = None

# pc list in section will be in short form
# pc list to put to pc will be in long form


def convert_list_pc_to_session(pc_list):
    return_list = list(pc_list)
    return_list[3] = full_list_to_short_list(pc_list[3])
    return_list[4] = full_list_to_short_list(pc_list[4])
    return_list[5] = full_list_to_short_list(pc_list[5])
    return return_list


def convert_list_session_to_pc(session_l):
    return_list = list(session_l)
    return_list[3] = short_list_to_full(session_l[3])
    return_list[4] = short_list_to_full(session_l[4])
    return_list[5] = short_list_to_full(session_l[5])
    # print(return_list[5])
    return return_list


def full_list_to_short_list(l):
    if l is None:
        return None
    return_list = []
    for item in l:
        if len(return_list) == 0:
            return_list.append({'item': item, 'quantity': 1})
        else:
            for i in return_list:
                if i['item']['name'] == item['name']:
                    i['quantity'] = i['quantity'] + 1
                    break
    return return_list


def short_list_to_full(l):
    if l is None:
        return None
    return_list = []
    for item in l:
        return_list.append(item['item'])
        for i in range(1, item['quantity']):
            return_list.append(item['item'])
    return return_list


def add_sub_quantity(op, index, item_list):
    try:
        if op == 'a':
            item_list[index]['quantity'] += 1
        elif op == 's':
            item_list[index]['quantity'] -= 1
    except IndexError:
        print("wrong index when +/- quantity")
    except:
        print("something is wrong")


def first_update_pc_score_to_db(pc, interact_point, point_type):
    id = GetItemFromDatabase.insert_to_rec_table(convert_for_update_db(pc), interact_point, point_type)
    return id


def convert_for_update_db(session_pc):
    cpu = {'id': session_pc[0]['id']}
    board = {'id': session_pc[1]['id']}
    if session_pc[2] is None:
        gpu = {'id': None}
    else:
        gpu = {'id': session_pc[2]['id']}
    ram = []
    for item in session_pc[3]:
        ram.append({'id': item['item']['id'], 'amount': str(item['quantity'] * utility.get_ram_total_size(item['item'])) + "gb"})
    if session_pc[4] is None:
        ssd = None
    else:
        ssd = []
        for item in session_pc[4]:
            ssd.append({'id': item['item']['id'], 'quantity': item['quantity']})
    if session_pc[5] is None:
        hdd = None
    else:
        hdd = []
        for item in session_pc[5]:
            hdd.append({'id': item['item']['id'], 'quantity': item['quantity']})
    psu = {'id': session_pc[6]['id']}
    if session_pc[7] is None:
        case = None
    else:
        case = {'id': session_pc[7]['id']}

    return {'cpu': cpu,
            'board': board,
            'gpu': gpu,
            'ram': ram,
            'ssd': ssd,
            'hdd': hdd,
            'psu': psu,
            'case': case
            }


def get_pc_if_auto_not_found(popular_pc_list, purpose, budget):
    if isinstance(budget, list):
        budget = budget[1]
    pc_list = popular_pc_list['pc_list']
    return_list = []
    for pc in pc_list:
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(pc)))
        case_list = current_pc.get_case_list(case_list=popular_pc_list['comp_info']['case'])
        if len(case_list) == 0:
            continue
        else:
            current_pc.add_case(case_list[0])
            current_pc.pc.storage_ssd = current_pc.pc.storage_ssd[0]
            return_list.append(current_pc.pc)
    return_list.sort(key=lambda x: abs(x.get_total_price() - budget))
    if len(return_list) > 10:
        return_list = return_list[0:10]
    # return_list.sort(reverse=True, key=lambda x: utility.get_pc_score(x, purpose))
    # return_list.sort(key=lambda x: x.get_total_price())
    return return_list



def get_data_cpu_list():
    if cache.get('cpu_list') is None:
        data = GetItemFromDatabase.get_cpu_list_from_db()
        json_data = json.dumps(data)
        cache.set('cpu_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('cpu_list'))
    return data


def get_data_board_list():
    if cache.get('board_list') is None:
        data = GetItemFromDatabase.get_board_list_from_db()
        json_data = json.dumps(data)
        cache.set('board_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('board_list'))
    return data


def get_data_gpu_list():
    if cache.get('gpu_list') is None:
        data = GetItemFromDatabase.get_gpu_list_from_db()
        json_data = json.dumps(data)
        cache.set('gpu_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('gpu_list'))
    return data


def get_data_ram_list():
    if cache.get('ram_list') is None:
        data = GetItemFromDatabase.get_ram_list_from_db()
        json_data = json.dumps(data)
        cache.set('ram_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('ram_list'))
    return data


def get_data_ssd_list():
    if cache.get('ssd_list') is None:
        data = GetItemFromDatabase.get_ssd_list_from_db()
        json_data = json.dumps(data)
        cache.set('ssd_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('ssd_list'))
    return data


def get_data_hdd_list():
    if cache.get('hdd_list') is None:
        data = GetItemFromDatabase.get_hdd_list_from_db()
        json_data = json.dumps(data)
        cache.set('hdd_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('hdd_list'))
    return data


def get_data_psu_list():
    if cache.get('psu_list') is None:
        data = GetItemFromDatabase.get_psu_list_from_db()
        json_data = json.dumps(data)
        cache.set('psu_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('psu_list'))
    return data


def get_data_case_list():
    if cache.get('case_list') is None:
        data = GetItemFromDatabase.get_case_list_from_db()
        json_data = json.dumps(data)
        cache.set('case_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('case_list'))
    return data


def get_popular_pc_list():
    if cache.get('popular_pc_list') is None:
        data = GetItemFromDatabase.get_pc_for_recommend(100)
        json_data = json.dumps(data)
        cache.set('popular_pc_list', json_data, timeout=86400)
    else:
        data = json.loads(cache.get('popular_pc_list'))
    return data
#########################################################################################################################################################
# start of route

def build(request):
    index = request.GET.get('index', None)
    if index is None:
        # if "pc" not in request.session:
        request.session["pc"] = [None, None, None, None, None, None, None, None]
        picked_pc = request.session["pc"]
        return render(request, 'build.html', {
            "cpu_form": CpuForm(),
            "board_form": BoardForm(),
            "gpu_form": GpuForm(),
            "ram_form": RamForm(),
            "ssd_form": SsdForm(),
            "hdd_form": HddForm(),
            "psu_form": PsuForm(),
            "case_form": CaseForm(),
            "picked_pc": picked_pc
        })
    else:
        # print(request.META['HTTP_REFERER'])
        index = int(index) - 1
        picked_pc_1 = list(request.session['res'][index])
        cpu = picked_pc_1[0][1]
        board = picked_pc_1[1][1]
        gpu = picked_pc_1[2][1]
        ram = full_list_to_short_list(picked_pc_1[3][1])
        if picked_pc_1[4][1] is None:
            ssd = None
        else:
            ssd = full_list_to_short_list([picked_pc_1[4][1]])
        if picked_pc_1[5][1] is None:
            hdd = None
        else:
            hdd = full_list_to_short_list([picked_pc_1[5][1]])
        psu = picked_pc_1[6][1]
        case = picked_pc_1[7][1]
        request.session["pc"] = [cpu, board, gpu, ram, ssd, hdd, psu, case]

        picked_pc = [[{'id': 'cpu'}, cpu], [{'id': 'board'}, board], [{'id': 'gpu'}, gpu], [{'id': 'ram'}, picked_pc_1[3][1]],
                     [{'id': 'ssd'}, [picked_pc_1[4][1]]], [{'id': 'hdd'}, [picked_pc_1[5][1]]], [{'id': 'psu'}, psu],
                     [{'id': 'case'}, case], [{'id': 'price'}, {'value': picked_pc_1[8][1]['value']}], [{'id': 'bench_score'}, {'value': picked_pc_1[8][1]['value']}]]

        return render(request, 'build.html', {
            "cpu_form": CpuForm(),
            "board_form": BoardForm(),
            "gpu_form": GpuForm(),
            "ram_form": RamForm(),
            "ssd_form": SsdForm(),
            "hdd_form": HddForm(),
            "psu_form": PsuForm(),
            "case_form": CaseForm(),
            "picked_pc": picked_pc
        })


# @csrf_exempt
def pick_cpu(request):
    form = CpuForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        oc = check_input(form.cleaned_data["oc"])
        brand = check_input(form.cleaned_data["brand_manual"])
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        cpu_list = current_pc.get_cpu_list(cpu_list=get_data_cpu_list(), overclock=oc, brand=brand)
        cpu_list = GetItemFromDatabase.search_dic(name, cpu_list)
        request.session['cpu_list'] = cpu_list
        return JsonResponse({'info': cpu_list})
    else:
        return JsonResponse({'info': []})


# @csrf_exempt
def add_cpu(request):
    post_data = json.loads(request.body.decode("utf-8"))
    index = int(post_data['index'])
    cpu = request.session['cpu_list'][index]
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    check = current_pc.add_cpu(cpu)
    if check:
        request.session["pc"][0] = request.session['cpu_list'][int(post_data['index'])]
        return JsonResponse({'mess': '0', 'item': cpu, 'price': current_pc.get_pc().get_total_price()})
    else:
        return JsonResponse({'mess': '1'})


def remove_cpu(request):
    request.session["pc"][0] = None
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    return JsonResponse({'mess': '0', 'price': current_pc.get_pc().get_total_price()})


def pick_board(request):
    form = BoardForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        cpu_supported = check_input(form.cleaned_data["cpu_supported"])
        oc = check_input(form.cleaned_data["oc"])
        form = check_input(form.cleaned_data["form"])
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        board_list = current_pc.get_board_list(board_list=get_data_board_list(),cpu_supported=cpu_supported, overclock=oc, form_factor=form)
        board_list = GetItemFromDatabase.search_dic(name, board_list, True)
        request.session['board_list'] = board_list
        return JsonResponse({'info': board_list})
    else:
        return JsonResponse({'info': []})


# @csrf_exempt
def add_board(request):
    post_data = json.loads(request.body.decode("utf-8"))
    board = request.session['board_list'][int(post_data['index'])]
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    check = current_pc.add_board(board)
    if check:
        request.session["pc"][1] = request.session['board_list'][int(post_data['index'])]
        request.session["pc"][3] = None
        request.session["pc"][4] = None
        request.session["pc"][5] = None
        request.session["pc"][7] = None
        return JsonResponse({'mess': '0', 'item': board, 'price': current_pc.get_pc().get_total_price()})
    else:
        return JsonResponse({'mess': '1'})


def remove_board(request):
    request.session["pc"][1] = None
    request.session["pc"][3] = None
    request.session["pc"][4] = None
    request.session["pc"][5] = None
    request.session["pc"][7] = None
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    return JsonResponse({'mess': '0', 'price': current_pc.get_pc().get_total_price()})


def pick_gpu(request):
    form = GpuForm(request.POST)
    if form.is_valid():
        # current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        gpu_name = str(check_input(form.cleaned_data["name"]))
        # gpu_list_tuple = GetItemFromDatabase.search(gpu_name, GetItemFromDatabase.search_gpu(brand=[], bench=["",""], price=["", ""]))
        # gpu_list = GetItemFromDatabase.convert_gpu_db_to_dic(gpu_list_tuple)
        gpu_list = GetItemFromDatabase.search_dic(gpu_name, get_data_gpu_list())
        request.session['gpu_list'] = gpu_list
        return JsonResponse({'info': gpu_list})
    else:
        return JsonResponse({'info': []})


# @csrf_exempt
def add_gpu(request):
    post_data = json.loads(request.body.decode("utf-8"))
    gpu = request.session['gpu_list'][int(post_data['index'])]
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    check = current_pc.add_gpu(gpu)
    if check:
        request.session["pc"][2] = request.session['gpu_list'][int(post_data['index'])]
        return JsonResponse({'mess': '0', 'item': gpu, 'price': current_pc.get_pc().get_total_price()})
    else:
        return JsonResponse({'mess': '1'})


def remove_gpu(request):
    request.session["pc"][2] = None
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    return JsonResponse({'mess': '0', 'price': current_pc.get_pc().get_total_price()})


def pick_ram(request):
    form = RamForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        kit = check_input(form.cleaned_data["kit"])
        amount = check_input(form.cleaned_data["amount"])
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        ram_list = current_pc.get_ram_list(ram_list=get_data_ram_list(),kit=kit, amount=amount)
        ram_list = GetItemFromDatabase.search_dic(name, ram_list)
        request.session['ram_list'] = ram_list
        return JsonResponse({'info': ram_list})
    else:
        return JsonResponse({'info': []})


# @csrf_exempt
def add_ram(request):
    post_data = json.loads(request.body.decode("utf-8"))
    ram = request.session['ram_list'][int(post_data['index'])]
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    check = current_pc.add_ram(ram)
    if check['stat']:
        if request.session["pc"][3] is None:
            request.session["pc"][3] = [{'item': request.session['ram_list'][int(post_data['index'])], 'quantity': 1}]
            return JsonResponse({'stat': '0', 'mess': check['mess'], 'item': request.session["pc"][3],
                                 'price': current_pc.get_pc().get_total_price()})
        else:
            dup = False
            for item in request.session["pc"][3]:
                if item['item']['name'] == ram['name']:
                    item['quantity'] += 1
                    dup = True
                    break
            if not dup:
                request.session["pc"][3].append({'item': ram, 'quantity': 1})
        # request.session['pc'][3] [{'item': ram A, 'quantity': 1}, {'item': ram B, 'quantity': 2}]
            return JsonResponse({'stat': '0', 'mess': check['mess'], 'item': request.session["pc"][3],
                             'price': current_pc.get_pc().get_total_price()})
    else:
        return JsonResponse({'stat': '1', 'mess': check['mess'], 'item': request.session["pc"][3],
                             'price': current_pc.get_pc().get_total_price()})


# @csrf_exempt
def increase_decrease_ram(request):
    post_data = json.loads(request.body.decode("utf-8"))
    operation = post_data['op']
    index = int(post_data['index'])
    ram = request.session["pc"][3][index]['item']
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    if operation == 'a':
        check = current_pc.add_ram(ram)
    else:
        check = current_pc.remove_ram(pos=index)
    if check['stat']:
        add_sub_quantity(operation, index, request.session["pc"][3])
        return JsonResponse({'stat': '0', 'mess': check['mess'], 'len': len(request.session["pc"][3]), 'price': current_pc.get_pc().get_total_price(),
                             'price_r': float(request.session["pc"][3][index]['item']['price']) * request.session["pc"][3][index]['quantity']})
    else:
        return JsonResponse({'stat': '1', 'mess': check['mess']})


# @csrf_exempt
def remove_ram(request):
    post_data = json.loads(request.body.decode("utf-8"))
    index = int(post_data['index'])
    if index == -1:
        request.session["pc"][3] = None
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        return JsonResponse({'stat': '0', 'mess': 'OK', 'len': 0, 'price': current_pc.get_pc().get_total_price()})
    else:
        try:
            del request.session["pc"][3][index]
        except IndexError:
            current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
            print("wrong index")
            return JsonResponse({'stat': '1', 'mess': 'wrong index', 'len': len(request.session["pc"][3]), 'price': current_pc.get_pc().get_total_price()})
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        return JsonResponse({'stat': '0', 'mess': 'OK', 'len': len(request.session["pc"][3]), 'price': current_pc.get_pc().get_total_price()})


def pick_ssd(request):
    form = SsdForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        amount = check_input(form.cleaned_data["amount"])
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        ssd_list = current_pc.get_ssd_list(ssd_list=get_data_ssd_list(), amount=amount)
        ssd_list = GetItemFromDatabase.search_dic(name, ssd_list)
        request.session['ssd_list'] = ssd_list
        return JsonResponse({'info': ssd_list})
    else:
        return JsonResponse({'info': []})


# @csrf_exempt
def add_ssd(request):
    post_data = json.loads(request.body.decode("utf-8"))
    ssd = request.session['ssd_list'][int(post_data['index'])]
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    check = current_pc.add_ssd(ssd)
    if check['stat']:
        if request.session["pc"][4] is None:
            request.session["pc"][4] = [{'item': request.session['ssd_list'][int(post_data['index'])], 'quantity': 1}]
            return JsonResponse({'stat': '0', 'mess': check['mess'], 'item': request.session["pc"][4],
                                 'price': current_pc.get_pc().get_total_price()})
        else:
            dup = False
            for item in request.session["pc"][4]:
                if item['item']['name'] == ssd['name']:
                    item['quantity'] += 1
                    dup = True
                    break
            if not dup:
                request.session["pc"][4].append({'item': ssd, 'quantity': 1})
            return JsonResponse({'stat': '0', 'mess': check['mess'], 'item': request.session["pc"][4],
                             'price': current_pc.get_pc().get_total_price()})
    else:
        return JsonResponse({'stat': '1', 'mess': check['mess'], 'item': request.session["pc"][4],
                             'price': current_pc.get_pc().get_total_price()})


# @csrf_exempt
def increase_decrease_ssd(request):
    post_data = json.loads(request.body.decode("utf-8"))
    operation = post_data['op']
    index = int(post_data['index'])
    ssd = request.session["pc"][4][index]['item']
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    if operation == 'a':
        check = current_pc.add_ssd(ssd)
    else:
        check = current_pc.remove_ssd(pos=index)
    if check['stat']:
        add_sub_quantity(operation, index, request.session["pc"][4])
        return JsonResponse({'stat': '0', 'mess': check['mess'], 'len': len(request.session["pc"][4]),
                             'price': current_pc.get_pc().get_total_price(),
                             'price_r': float(request.session["pc"][4][index]['item']['price']) *
                                        request.session["pc"][4][index]['quantity']})
    else:
        return JsonResponse({'stat': '1', 'mess': check['mess']})


# @csrf_exempt
def remove_ssd(request):
    post_data = json.loads(request.body.decode("utf-8"))
    index = int(post_data['index'])
    if index == -1:
        request.session["pc"][4] = None
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        return JsonResponse({'stat': '0', 'mess': 'OK', 'len': 0, 'price': current_pc.get_pc().get_total_price()})
    else:
        try:
            del request.session["pc"][4][index]
        except IndexError:
            current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
            print("wrong index")
            return JsonResponse({'stat': '1', 'mess': 'wrong index', 'len': len(request.session["pc"][4]), 'price': current_pc.get_pc().get_total_price()})
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        return JsonResponse({'stat': '0', 'mess': 'OK', 'len': len(request.session["pc"][4]), 'price': current_pc.get_pc().get_total_price()})



def pick_hdd(request):
    form = HddForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        amount = check_input(form.cleaned_data["amount"])
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        hdd_list = current_pc.get_hdd_list(hdd_list=get_data_hdd_list() ,amount=amount)
        hdd_list = GetItemFromDatabase.search_dic(name, hdd_list)
        request.session['hdd_list'] = hdd_list
        return JsonResponse({'info': hdd_list})
    else:
        return JsonResponse({'info': []})


# @csrf_exempt
def add_hdd(request):
    post_data = json.loads(request.body.decode("utf-8"))
    hdd = request.session['hdd_list'][int(post_data['index'])]
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    check = current_pc.add_hdd(hdd)
    if check['stat']:
        if request.session["pc"][5] is None:
            request.session["pc"][5] = [{'item': request.session['hdd_list'][int(post_data['index'])], 'quantity': 1}]
            return JsonResponse({'stat': '0', 'mess': check['mess'], 'item': request.session["pc"][5],
                                 'price': current_pc.get_pc().get_total_price()})
        else:
            dup = False
            for item in request.session["pc"][5]:
                if item['item']['name'] == hdd['name']:
                    item['quantity'] += 1
                    dup = True
                    break
            if not dup:
                request.session["pc"][5].append({'item': hdd, 'quantity': 1})
            return JsonResponse({'stat': '0', 'mess': check['mess'], 'item': request.session["pc"][5],
                             'price': current_pc.get_pc().get_total_price()})
    else:
        return JsonResponse({'stat': '1', 'mess': check['mess'], 'item': request.session["pc"][5],
                             'price': current_pc.get_pc().get_total_price()})


# @csrf_exempt
def increase_decrease_hdd(request):
    post_data = json.loads(request.body.decode("utf-8"))
    operation = post_data['op']
    index = int(post_data['index'])
    hdd = request.session["pc"][5][index]['item']
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    if operation == 'a':
        check = current_pc.add_hdd(hdd)
    else:
        check = current_pc.remove_hdd(pos=index)
    if check['stat']:
        add_sub_quantity(operation, index, request.session["pc"][5])
        return JsonResponse({'stat': '0', 'mess': check['mess'], 'len': len(request.session["pc"][5]),
                             'price': current_pc.get_pc().get_total_price(),
                             'price_r': float(request.session["pc"][5][index]['item']['price']) *
                                        request.session["pc"][5][index]['quantity']})
    else:
        return JsonResponse({'stat': '1', 'mess': check['mess']})


# @csrf_exempt
def remove_hdd(request):
    post_data = json.loads(request.body.decode("utf-8"))
    index = int(post_data['index'])
    if index == -1:
        request.session["pc"][5] = None
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        return JsonResponse({'stat': '0', 'mess': 'OK', 'len': 0, 'price': current_pc.get_pc().get_total_price()})
    else:
        try:
            del request.session["pc"][5][index]
        except IndexError:
            current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
            print("wrong index")
            return JsonResponse({'stat': '1', 'mess': 'wrong index', 'len': len(request.session["pc"][5]), 'price': current_pc.get_pc().get_total_price()})
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        return JsonResponse({'stat': '0', 'mess': 'OK', 'len': len(request.session["pc"][5]), 'price': current_pc.get_pc().get_total_price()})


def pick_psu(request):
    form = PsuForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        form_fac = check_input(form.cleaned_data["form"])
        watt = check_input(form.cleaned_data["watt"])
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        psu_list = current_pc.get_psu_list(psu_list=get_data_psu_list(), form_factor=form_fac, watt=watt)
        psu_list = GetItemFromDatabase.search_dic(name, psu_list)
        request.session['psu_list'] = psu_list
        return JsonResponse({'info': psu_list})
    else:
        return JsonResponse({'info': []})


# @csrf_exempt
def add_psu(request):
    post_data = json.loads(request.body.decode("utf-8"))
    psu = request.session['psu_list'][int(post_data['index'])]
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    check = current_pc.add_psu(psu)
    if check['stat']:
        request.session["pc"][6] = psu
        return JsonResponse({'mess': '0', 'item': psu, 'price': current_pc.get_pc().get_total_price()})
    else:
        return JsonResponse(
            {'stat': '1', 'item': request.session["pc"][6], 'price': current_pc.get_pc().get_total_price()})


# @csrf_exempt
def remove_psu(request):
    request.session["pc"][6] = None
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    return JsonResponse({'mess': '0', 'price': current_pc.get_pc().get_total_price()})


def pick_case(request):
    form = CaseForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data["name"]
        form_fac = check_input(form.cleaned_data["form"])
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        case_list = current_pc.get_case_list(case_list=get_data_case_list(), form_factor=form_fac)
        case_list = GetItemFromDatabase.search_dic(name, case_list, True)
        request.session['case_list'] = case_list
        return JsonResponse({'info': case_list})
    else:
        return JsonResponse({'info': []})


# @csrf_exempt
def add_case(request):
    post_data = json.loads(request.body.decode("utf-8"))
    case = request.session['case_list'][int(post_data['index'])]
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    check = current_pc.add_case(case)
    if check['stat']:
        request.session["pc"][7] = request.session['case_list'][int(post_data['index'])]
        return JsonResponse({'mess': '0', 'item': case, 'price': current_pc.get_pc().get_total_price()})
    else:
        return JsonResponse({'stat': '1', 'item': request.session["pc"][7]})


def remove_case(request):
    request.session["pc"][7] = None
    current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
    return JsonResponse({'mess': '0', 'price': current_pc.get_pc().get_total_price()})


def pc_builder_auto(request):
    return render(request, 'builder/pc_builder_auto.html', {
        "form": PcAutoBuildForm()
    })


def pc_builder_sets(request):
    if request.method == "POST":
        form = PcAutoBuildForm(request.POST)
        if form.is_valid():
            purpose = form.cleaned_data["purpose"]
            budget1 = float(form.cleaned_data["budget"].replace(',', ''))
            if form.cleaned_data["budget2"]:
                budget2 = float(form.cleaned_data["budget2"].replace(',', ''))
            else:
                budget2 = None
            overclock = check_input(form.cleaned_data["overclock"])
            form_factor = check_input(form.cleaned_data["form_factor"])
            ram = check_input(form.cleaned_data["ram"])
            ram_amount = check_input(form.cleaned_data["ram_amount"])
            storage_ssd = check_input(form.cleaned_data["storage_ssd"])
            storage_hdd = check_input(form.cleaned_data["storage_hdd"])
            psu = check_input(form.cleaned_data["psu"])
            brand = check_input(form.cleaned_data["brand"])

            # if overclock == 'None':
            #     overclock = None
            # elif overclock == 'True':
            #     overclock = True
            # else:
            #     overclock = False
            # if form_factor == 'None':
            #     form_factor = None
            # if ram == 'None': ram = None
            # if ram_amount == 'None': ram_amount = None
            # if psu == 'None': psu = None
            # if brand == 'None': brand = None
            if budget2 is None:
                budget = budget1
            else:
                if budget2 > budget1:
                    budget = [budget1, budget2]
                else:
                    budget = [budget2, budget1]

            res = build_pc.build(purpose=purpose, total_budget=budget,
                                 cpu_list=get_data_cpu_list(), board_list=get_data_board_list(), gpu_list=get_data_gpu_list(),
                                 ram_list=get_data_ram_list(), ssd_list=get_data_ssd_list(), hdd_list=get_data_hdd_list(),
                                 psu_list=get_data_psu_list(), case_list=get_data_case_list(),
                                 overclock=overclock, req_ram=ram_amount, storage_ssd=storage_ssd, storage_hdd=storage_hdd, form_factor=form_factor, kit=ram,
                                 modular=psu, psu_eff=None, preference=brand)

            request.session['requirement'] = {
                'purpose': purpose,
                'budget1': budget1,
                'budget2': budget2,
                'overclock': overclock,
                'form_factor': form_factor,
                'ram': ram,
                'ram_amount': ram_amount,
                'storage_ssd': storage_ssd,
                'storage_hdd': storage_hdd,
                'psu': psu,
                'cpu_brand': brand,
            }
            request.session['found_auto'] = 0
            if len(res) == 0:
                res = get_pc_if_auto_not_found(get_popular_pc_list(), purpose, budget)
                request.session['found_auto'] = 1
            elif len(res) > 100:
                res = res[0:100]
            res = build_pc.convert_for_web(res, purpose)

            if len(res) > 100:
                res = res[0:100]

            request.session["res"] = res
            paginator = Paginator(res, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, "builder/pc_builder_sets.html", {'page_obj': page_obj, "res": res, 'stat': request.session['found_auto'], 'requirement': request.session['requirement']})
        else:
            return render(request, "builder/pc_builder_auto.html", {
                "form": form
            })
    elif request.GET.get('page'):
        res = request.session["res"]
        paginator = Paginator(res, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(page_obj)
        return render(request, "builder/pc_builder_sets.html", {'page_obj': page_obj, "res": res, 'stat': request.session['found_auto'], 'requirement': request.session['requirement']})
    return render(request, "builder/pc_builder_auto.html", {
        "form": PcAutoBuildForm()
    })


def welcome(request):
    return render(request, "builder/welcome.html")


@login_required(login_url='http://127.0.0.1:8000/demo/login/')
def pc_detail(request):
    index = int(request.GET.get('index', None)) - 1
    if 'interacted_pc' not in request.session: # [picked pc, pdf download check, interaction point, pc main comp id]
        request.session['interacted_pc'] = []
    if index >= 0: #picked from auto build (send from auto site begin from 1 so have to -1)
        picked_pc = list(request.session['res'][index])
        cpu = picked_pc[0][1]
        board = picked_pc[1][1]
        gpu = picked_pc[2][1]
        ram = full_list_to_short_list(picked_pc[3][1])
        if picked_pc[4][1] is None:
            ssd = None
        else:
            ssd = full_list_to_short_list([picked_pc[4][1]])
        if picked_pc[5][1] is None:
            hdd = None
        else:
            hdd = full_list_to_short_list([picked_pc[5][1]])
        psu = picked_pc[6][1]
        case = picked_pc[7][1]
        request.session["pc"] = [cpu, board, gpu, ram, ssd, hdd, psu, case]
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        request.session['current_pc_req'] = request.session['requirement']
        request.session['point_type'] = 'auto'
    else:
        if request.session["pc"][4] is None and request.session["pc"][5] is None:
            return redirect('http://127.0.0.1:8000/demo/build/')
        for i in range(len(request.session["pc"])):
            if i in [0, 1, 2, 3, 6] and request.session["pc"][i] is None:
                return redirect('http://127.0.0.1:8000/demo/build/')
        current_pc = BuildStepByStep(Pc(convert_list_session_to_pc(request.session["pc"])))
        request.session['current_pc_req'] = None
        request.session['point_type'] = 'custom'
    score = current_pc.get_score()
    picked_pc = [[{'id': 'cpu'}, request.session["pc"][0]],
                 [{'id': 'board'}, request.session["pc"][1]],
                 [{'id': 'gpu'}, request.session["pc"][2]],
                 [{'id': 'ram'}, request.session["pc"][3]],
                 [{'id': 'ssd'}, request.session["pc"][4]],
                 [{'id': 'hdd'}, request.session["pc"][5]],
                 [{'id': 'psu'}, request.session["pc"][6]],
                 [{'id': 'case'}, request.session["pc"][7]],
                 [{'id': 'price'}, current_pc.pc.get_total_price()],
                 [{'desktop': score[0],'gaming': score[1],'workstation': score[2]}]]
    if 'current_picked_pc' not in request.session:
        request.session['current_picked_pc'] = picked_pc
        request.session['check_pdf_point'] = False
        request.session['interact_point'] = 0
        request.session['pc_id_in_db'] = first_update_pc_score_to_db(request.session["pc"],
                                                                     request.session['interact_point'],
                                                                     request.session['point_type'])
        request.session['interacted_pc'].append([request.session['current_picked_pc'], request.session['check_pdf_point'], request.session['interact_point'], request.session['pc_id_in_db']])
        print("pick the new pc, id of the main_comp: ", request.session['pc_id_in_db'],  ", score is: ", request.session['interact_point'])
    else:
        if request.session['current_picked_pc'] != picked_pc:
            # check if the pc has been viewed before in this session
            for pc in request.session['interacted_pc']:
                if picked_pc == pc[0]:
                    # update the current one to the list
                    for pc1 in request.session['interacted_pc']:
                        if pc1[0] == request.session['current_picked_pc']:
                            pc1[1] = request.session['check_pdf_point']
                            pc1[2] = request.session['interact_point']
                            break
                    # update the one in the session
                    request.session['current_picked_pc'] = pc[0]
                    request.session['check_pdf_point'] = pc[1]
                    request.session['interact_point'] = pc[2] + 1
                    request.session['pc_id_in_db'] = pc[3]
                    print("picked pc is in the interacted list, id of main comp is: ", request.session['pc_id_in_db'], ", score is: ", request.session['interact_point'])
                    return render(request, "builder/pc_detail.html", {"picked_pc": picked_pc})
            # update the current one to the list
            for pc1 in request.session['interacted_pc']:
                if pc1 == request.session['current_picked_pc']:
                    pc1[1] = request.session['check_pdf_point']
                    pc1[2] = request.session['interact_point']
                    break
            # replace the new one to the session
            request.session['current_picked_pc'] = picked_pc
            request.session['check_pdf_point'] = False
            request.session['interact_point'] = 0
            request.session['pc_id_in_db'] = first_update_pc_score_to_db(request.session["pc"],
                                                                         request.session['interact_point'],
                                                                         request.session['point_type'])
            # add new one to the list
            request.session['interacted_pc'].append(
                [request.session['current_picked_pc'], request.session['check_pdf_point'],
                 request.session['interact_point'], request.session['pc_id_in_db']])
            print("pick the new pc, id of the main_comp: ", request.session['pc_id_in_db'],  ", score is: ", request.session['interact_point'])
    return render(request, "builder/pc_detail.html", {"picked_pc": picked_pc})


# @csrf_exempt
def clicked_link(request):
    post_data = json.loads(request.body.decode("utf-8"))
    request.session['interact_point'] = request.session['interact_point'] + 1
    update = GetItemFromDatabase.update_score(request.session['pc_id_in_db'], request.session['interact_point'], request.session['point_type'])
    if update:
        print("updated point, current interact point:    ", request.session['interact_point'])
    return JsonResponse({"stat": '0'})


def product_cpu(request):
    data = GetItemFromDatabase.search_cpu([], [], [], ["",""], ["",""])
    request.session['product_cpu'] = {
        'cpuname': '',
        'cpuseries': [],
        'cpubrand': [],
        'cpusocket': [],
        'cpubench': ['',''],
        'cpuprice': ['',''],
        'data': data
    }
    return render(request, "builder/product_cpu.html", {"cpu_list": GetItemFromDatabase.convert_cpu_db_to_dic(data)})


def product_cpu_search(request):

    if request.POST:
        same_name = True
        same_tick = True
# cpu name
        name = request.POST.get('cpuname')
# cpu series
        series_list = request.POST.getlist('cpuseries')
        if series_list[0] == '':
            series_list = []
        else:
            for item in series_list:
                item = item.replace('Intel ', '').replace('AMD ', '')
# cpu brand
        brand_list = request.POST.getlist('cpubrand')
        if brand_list[0] == '':
            brand_list = []

# cpu socket
        socket_list = request.POST.getlist('cpusocket')
        if socket_list[0] == '':
            socket_list = []
# cpu bench
        bench_park = request.POST.get('cpubench', ['','']).split(' ')
        bench_list = [bench_park[0], bench_park[2]]
# cpu price
        price_part = request.POST.get('cpuprice', ['','']).split(' ')
        price_list = [price_part[0].split('\xa0')[0].replace('.', ''),
                                                      price_part[2].split('\xa0')[0].replace('.', '')]
# compare
        if request.session['product_cpu']['cpuname'] != name:
            same_name = False
            request.session['product_cpu']['cpuname'] = name
        if request.session['product_cpu']['cpuseries'] !=  series_list:
            same_tick = False
            request.session['product_cpu']['cpuseries'] = series_list
        if request.session['product_cpu']['cpubrand'] != brand_list:
            same_tick = False
            request.session['product_cpu']['cpubrand'] = brand_list
        if request.session['product_cpu']['cpusocket'] != socket_list:
            same_tick = False
            request.session['product_cpu']['cpusocket'] = socket_list
        if request.session['product_cpu']['cpubench'] != bench_list:
            same_tick = False
            request.session['product_cpu']['cpubench'] = bench_list
        if request.session['product_cpu']['cpuprice'] != price_list:
            same_tick = False
            request.session['product_cpu']['cpuprice'] = price_list
        if same_name and same_tick:
            return JsonResponse({"cpu_list": GetItemFromDatabase.convert_cpu_db_to_dic(request.session['product_cpu']['data'])})
        elif not same_tick:
            print(name, series_list, brand_list, socket_list, bench_list, price_list)
            db_data = GetItemFromDatabase.search_cpu(series=request.session['product_cpu']['cpuseries'],
                                              brand=request.session['product_cpu']['cpubrand'],
                                              socket=request.session['product_cpu']['cpusocket'],
                                              bench=request.session['product_cpu']['cpubench'],
                                              price=request.session['product_cpu']['cpuprice'])
            request.session['product_cpu']['data'] = db_data
            return JsonResponse({"cpu_list": GetItemFromDatabase.convert_cpu_db_to_dic(GetItemFromDatabase.search(request.session['product_cpu']['cpuname'], db_data))})
        elif not same_name and same_tick:
            return JsonResponse({"cpu_list": GetItemFromDatabase.convert_cpu_db_to_dic(GetItemFromDatabase.search(request.session['product_cpu']['cpuname'], request.session['product_cpu']['data']))})


def product_mainboard(request):
    data = GetItemFromDatabase.search_mb(brand=[], socket=[], chipset=[], form=[], memtype=[],
                                       ramslot=[], m2=[], sata=[], price=["", ""])
    request.session['product_board'] = {
        'boardname': '',
        'boardbrand': [],
        'boardsocket': [],
        'boardchipset': [],
        'boardformfactor': [],
        'boardmemorytype': [],
        'boardramslot': [],
        'boardm2slots': [],
        'boardsataports': [],
        'boardprice': ["", ""],
        'data': data
    }
    return render(request, "builder/product_mainboard.html", {"mainboard_list": GetItemFromDatabase.convert_board_db_to_dic(data)})


def product_board_search(request):
    if request.POST:
# board name
        name = request.POST.get('boardname', '')
# board brand
        brand_list = request.POST.getlist('boardbrand')
        if brand_list[0] == 'all':
            brand_list = []
# board socket
        socket_list = request.POST.getlist('boardsocket')
        if socket_list[0] == 'all':
            socket_list = []
# board chipset
        chipset_list = request.POST.getlist('boardchipset')
        if chipset_list[0] == 'all':
            chipset_list = []
# board form factor
        form_list =  request.POST.getlist('boardformfactor')
        if form_list[0] == 'all':
            form_list = []
# board memory type
        mem_list = request.POST.getlist('boardformfactor')
        if mem_list[0] == 'all':
            mem_list = []
# board ram slot
        ram_slot_list = request.POST.getlist('boardramslot')
        if ram_slot_list[0] == 'all':
            ram_slot_list = []
# board m2 slot
        m2_part = request.POST.get('boardm2slots').split(' ')
        m2_list =   [m2_part[0], m2_part[2]]
# board sata ports
        sata_part = request.POST.get('boardsataports').split(' ')
        sata_list =  [sata_part[0], sata_part[2]] # ['0', '12']
# board price
        price_part = request.POST.get('boardprice').split(' ')
        price_list = [price_part[0].split('\xa0')[0].replace('.', ''),
                      price_part[2].split('\xa0')[0].replace('.', '')]
# compare
        check_list = [name, brand_list, socket_list, chipset_list, form_list, mem_list, ram_slot_list, m2_list, sata_list, price_list]
        print(check_list)
        current_list = list(request.session['product_board'].values())
        same_name = check_list[0] == current_list[0]
        same_tick = check_list[1:] == current_list[1:len(current_list) - 1]
        if same_name and same_tick:
            print('same search - board')
            return JsonResponse({"mainboard_list": GetItemFromDatabase.convert_board_db_to_dic(request.session['product_board']['data'])})
        elif not same_tick:
            print('new tick search - board')
            db_data = GetItemFromDatabase.search_mb(brand=brand_list, socket=socket_list, chipset=chipset_list, form=form_list, memtype=mem_list,
                                               ramslot=ram_slot_list, m2=m2_list, sata=sata_list, price=["", ""])
            request.session['product_board']['boardname'] = name
            request.session['product_board']['boardbrand'] = brand_list
            request.session['product_board']['boardsocket'] = socket_list
            request.session['product_board']['boardchipset'] = chipset_list
            request.session['product_board']['boardformfactor'] = form_list
            request.session['product_board']['boardmemorytype'] = mem_list
            request.session['product_board']['boardramslot'] = ram_slot_list
            request.session['product_board']['boardm2slots'] = m2_list
            request.session['product_board']['boardsataports'] = sata_list
            request.session['product_board']['boardprice'] = price_list
            request.session['product_board']['data'] = db_data
            return JsonResponse({"mainboard_list": GetItemFromDatabase.convert_board_db_to_dic(
                GetItemFromDatabase.search(request.session['product_board']['boardname'], db_data, no_brand=True))})
        elif not same_name and same_tick:
            print('new name same tick search - board')
            request.session['product_board']['boardname'] = name
            return JsonResponse({"mainboard_list": GetItemFromDatabase.convert_board_db_to_dic(
                GetItemFromDatabase.search(request.session['product_board']['boardname'], request.session['product_board']['data'], no_brand=True))})


def product_gpu(request):
    data = GetItemFromDatabase.search_gpu(brand=[], bench=["",""], price=["", ""])
    request.session['product_gpu'] = {
        'gpuname': '',
        'gpubrand': [],
        'gpubench': [],
        'gpuprice':  ["", ""],
        'data': data
    }
    return render(request, "builder/product_gpu.html", {"gpu_list": GetItemFromDatabase.convert_gpu_db_to_dic(data)})


def product_gpu_search(request):
    if request.POST:
# gpu name
        name = request.POST.get('gpuname', '')
# gpu brand
        brand_list = request.POST.getlist('gpubrand')
        if brand_list[0] == 'all':
            brand_list = []
# gpu bench
        bench_part = request.POST.get('gpubench').split(' ')
        bench_list = [bench_part[0], bench_part[2]]
# gpu price
        price_part = request.POST.get('gpuprice', ['', '']).split(' ')
        price_list = [price_part[0].split('\xa0')[0].replace('.', ''),
                      price_part[2].split('\xa0')[0].replace('.', '')]
        # compare
        check_list = [name, brand_list, bench_list, price_list]
        print(check_list)
        current_list = list(request.session['product_gpu'].values())
        same_name = check_list[0] == current_list[0]
        same_tick = check_list[1:] == current_list[1:len(current_list) - 1]
        if same_name and same_tick:
            print('same search - gpu')
            return JsonResponse(
                {"gpu_list": GetItemFromDatabase.convert_gpu_db_to_dic(request.session['product_gpu']['data'])})
        elif not same_tick:
            print('new tick search - gpu')
            db_data = GetItemFromDatabase.search_gpu(brand=brand_list, bench=bench_list, price=price_list)
            request.session['product_gpu']['gpuname'] = name
            request.session['product_gpu']['gpubrand'] = brand_list
            request.session['product_gpu']['gpubench'] = bench_list
            request.session['product_gpu']['gpuprice'] = price_list
            request.session['product_gpu']['data'] = db_data
            return JsonResponse({"gpu_list": GetItemFromDatabase.convert_gpu_db_to_dic(
                GetItemFromDatabase.search(request.session['product_gpu']['gpuname'], db_data))})
        elif not same_name and same_tick:
            print('new name same tick search - gpu')
            request.session['product_gpu']['gpuname'] = name
            return JsonResponse({"gpu_list": GetItemFromDatabase.convert_gpu_db_to_dic(
                GetItemFromDatabase.search(request.session['product_gpu']['gpuname'],   request.session['product_gpu']['data']))})


def product_ram(request):
    data = GetItemFromDatabase.search_ram(brand=[], memtype=[], rambus=[], size=[],
                                         quant=[], bench=["", ""], price=["", ""])
    request.session['product_ram'] = {
        'ramname': '',
        'rambrand': [],
        'ramtype': [],
        'rambus': [],
        'ramsize': [],
        'ramquantity': [],
        'rambench': ["", ""],
        'ramprice': ["", ""],
        'data': data
    }
    return render(request, "builder/product_ram.html", {"ram_list": GetItemFromDatabase.convert_ram_db_to_dic(data)})

def product_ram_search(request):
    if request.POST:
# ram name
        name = request.POST.get('ramname')
# ram brand
        brand_list = request.POST.getlist('rambrand')
        if brand_list[0] == 'all':
            brand_list = []
# ram type
        type_list = request.POST.getlist('ramtype')
        if type_list[0] == 'all':
            type_list = []
# ram bus
        bus_list = request.POST.getlist('rambus')
        if bus_list[0] == 'all':
            bus_list = []
        else:
            for item in bus_list:
                item = item.replace('MHz', '')
# ram size
        size_list = request.POST.getlist('ramsize')
        if size_list[0] == 'all':
            size_list = []
# ram quantity
        quant_list = request.POST.getlist('ramquantity')
        if quant_list[0] == 'all':
            quant_list = []
        else:
            for i in range (0, len(quant_list)):
                if quant_list[i] == 'Single':
                    quant_list[i] = '1'
                elif quant_list[i] == 'Kit 2':
                    quant_list[i] = '2'
                elif quant_list[i] == 'Kit 4':
                    quant_list[i] = '4'
# ram bench
        bench_park = request.POST.get('rambench', ['','']).split(' ')
        bench_list = [bench_park[0], bench_park[2]]
# ram price
        price_part = request.POST.get('ramprice', ['','']).split(' ')
        price_list = [price_part[0].split('\xa0')[0].replace('.', ''), price_part[2].split('\xa0')[0].replace('.', '')]

# compare
        check_list = [name, brand_list, type_list, bus_list, size_list, quant_list, bench_list, price_list]
        print(check_list)
        current_list = list(request.session['product_ram'].values())
        same_name = check_list[0] == current_list[0]
        same_tick = check_list[1:] == current_list[1:len(current_list) - 1]
        if same_name and same_tick:
            print('same search - ram')
            return JsonResponse({"ram_list": GetItemFromDatabase.convert_ram_db_to_dic(
                request.session['product_ram']['data'])})
        elif not same_tick:
            print('new tick search - ram')
            db_data = GetItemFromDatabase.search_ram(brand=brand_list, memtype=type_list, rambus=bus_list, size=size_list,
                                         quant=quant_list, bench=bench_list, price=price_list)
            request.session['product_ram']['ramname'] = name
            request.session['product_ram']['rambrand'] = brand_list
            request.session['product_ram']['ramtype'] = type_list
            request.session['product_ram']['rambus'] = bus_list
            request.session['product_ram']['ramsize'] = size_list
            request.session['product_ram']['ramquantity'] = quant_list
            request.session['product_ram']['rambench'] = bench_list
            request.session['product_ram']['ramprice'] = price_list
            request.session['product_ram']['data'] = db_data
            return JsonResponse({"ram_list": GetItemFromDatabase.convert_ram_db_to_dic(
                GetItemFromDatabase.search(request.session['product_ram']['ramname'], db_data))})
        elif not same_name and same_tick:
            print('new name same tick search - ran')
            request.session['product_ram']['ramname'] = name
            return JsonResponse({"ram_list": GetItemFromDatabase.convert_ram_db_to_dic(
                GetItemFromDatabase.search(request.session['product_ram']['ramname'],  request.session['product_ram']['data']))})


def product_ssd(request):
    data = GetItemFromDatabase.search_ssd(brand=[], comp=[], bench=["", ""], price=["", ""])
    request.session['product_ssd'] = {
        'ssdname': '',
        'ssdbrand': [],
        'ssdcapacity': [],
        'ssdbench': ["", ""],
        'ssdprice': ["", ""],
        'data': data
    }
    return render(request, "builder/product_ssd.html", {"ssd_list": GetItemFromDatabase.convert_ssd_db_to_dic(data)})


def product_ssd_search(request):
    if request.POST:
# ssd name
        name = request.POST.get('ssdname')
# ssd brand
        brand_list = request.POST.getlist('ssdbrand')
        if brand_list[0] == 'all':
            brand_list = []
# ssd capacity
        cap_list = request.POST.getlist('ssdcapacity')
        if cap_list[0] == 'all':
            cap_list = []
# ssd bench
        bench_park = request.POST.get('ssdbench', ['', '']).split(' ')
        bench_list = [bench_park[0], bench_park[2]]
# ssd price
        price_part = request.POST.get('ssdprice', ['', '']).split(' ')
        price_list = [price_part[0].split('\xa0')[0].replace('.', ''), price_part[2].split('\xa0')[0].replace('.', '')]
# compare
        check_list = [name, brand_list, cap_list, bench_list, price_list]
        current_list = list(request.session['product_ssd'].values())
        same_name = check_list[0] == current_list[0]
        same_tick = check_list[1:] == current_list[1:len(current_list) - 1]
        if same_name and same_tick:
            print('same search - ssd')
            return JsonResponse({"ssd_list": GetItemFromDatabase.convert_ssd_db_to_dic(
                request.session['product_ssd']['data'])})
        elif not same_tick:
            print('new tick search - ssd')
            db_data = GetItemFromDatabase.search_ssd(brand=brand_list, comp=cap_list, bench=bench_list, price=price_list)
            request.session['product_ssd']['ssdname'] = name
            request.session['product_ssd']['ssdbrand'] = brand_list
            request.session['product_ssd']['ssdcapacity'] = cap_list
            request.session['product_ssd']['ssdbench'] = bench_list
            request.session['product_ssd']['ssdprice'] = price_list
            request.session['product_ssd']['data'] = db_data
            return JsonResponse({"ssd_list": GetItemFromDatabase.convert_ssd_db_to_dic(
                GetItemFromDatabase.search(request.session['product_ssd']['ssdname'], db_data))})
        elif not same_name and same_tick:
            print('new name same tick search - ssd')
            request.session['product_ssd']['ssdname'] = name
            return JsonResponse({"ssd_list": GetItemFromDatabase.convert_ssd_db_to_dic(
                GetItemFromDatabase.search(request.session['product_ssd']['ssdname'],
                                           request.session['product_ssd']['data']))})


def product_hdd(request):
    data = GetItemFromDatabase.search_hdd(brand=[], comp=[], bench=["", ""], price=["", ""])
    request.session['product_hdd'] = {
        'hddname': '',
        'hddbrand': [],
        'hddcapacity': [],
        'hddbench': ["", ""],
        'hddprice': ["", ""],
        'data': data
    }
    return render(request, "builder/product_hdd.html", {"hdd_list": GetItemFromDatabase.convert_hdd_db_to_dic(data)})


def product_hdd_search(request):
    if request.POST:
# hdd name
        name = request.POST.get('hddname')
# hdd brand
        brand_list = request.POST.getlist('hddbrand')
        if brand_list[0] == 'all':
            brand_list = []
# hdd capacity
        cap_list = request.POST.getlist('hddcapacity')
        if cap_list[0] == 'all':
            cap_list = []
# hdd bench
        bench_park = request.POST.get('hddbench', ['', '']).split(' ')
        bench_list = [bench_park[0], bench_park[2]]
# hdd price
        price_part = request.POST.get('hddprice', ['', '']).split(' ')
        price_list = [price_part[0].split('\xa0')[0].replace('.', ''), price_part[2].split('\xa0')[0].replace('.', '')]
# compare
        check_list = [name, brand_list, cap_list, bench_list, price_list]
        current_list = list(request.session['product_hdd'].values())
        same_name = check_list[0] == current_list[0]
        same_tick = check_list[1:] == current_list[1:len(current_list) - 1]
        if same_name and same_tick:
            print('same search - hdd')
            return JsonResponse({"hdd_list": GetItemFromDatabase.convert_hdd_db_to_dic(
                request.session['product_hdd']['data'])})
        elif not same_tick:
            print('new tick search - hdd')
            db_data = GetItemFromDatabase.search_hdd(brand=brand_list, comp=cap_list, bench=bench_list, price=price_list)
            request.session['product_hdd']['hddname'] = name
            request.session['product_hdd']['hddbrand'] = brand_list
            request.session['product_hdd']['hddcapacity'] = cap_list
            request.session['product_hdd']['hddbench'] = bench_list
            request.session['product_hdd']['hddprice'] = price_list
            request.session['product_hdd']['data'] = db_data
            return JsonResponse({"hdd_list": GetItemFromDatabase.convert_hdd_db_to_dic(
                GetItemFromDatabase.search(request.session['product_hdd']['hddname'], db_data))})
        elif not same_name and same_tick:
            print('new name same tick search - hdd')
            request.session['product_hdd']['hddname'] = name
            return JsonResponse({"hdd_list": GetItemFromDatabase.convert_hdd_db_to_dic(
                GetItemFromDatabase.search(request.session['product_hdd']['hddname'],
                                           request.session['product_hdd']['data']))})

def product_psu(request):
    data = GetItemFromDatabase.search_psu(brand=[], eff=[], watt=[], modul=[], form=[], price=["", ""])
    request.session['product_psu'] = {
        'psuname': '',
        'psubrand': [],
        'psuefficientrating': [],
        'psuwattage': [],
        'psumodularity': [],
        'psuformfactor': [],
        'psuprice': ["", ""],
        'data': data
    }
    return render(request, "builder/product_psu.html", {"psu_list": GetItemFromDatabase.convert_psu_db_to_dic(data)})


def product_psu_search(request):
    if request.POST:
# psu name
        name = request.POST.get('psuname')
# psu brand
        brand_list = request.POST.getlist('psubrand')
        if brand_list[0] == 'all':
            brand_list = []
# psu efficient
        eff_list = request.POST.getlist('psuefficientrating')
        if eff_list[0] == 'all':
            eff_list = []
# psu wattage
        watt_list = request.POST.getlist('psuwattage')
        if watt_list[0] == 'all':
            watt_list = []
# psu modularity
        modul_list = request.POST.getlist('psumodularity')
        if modul_list[0] == 'all':
            modul_list = []
# psu form factor
        form_list = request.POST.getlist('psuformfactor')
        if form_list[0] == 'all':
            form_list = []
# psu price
        price_part = request.POST.get('psuprice', ['', '']).split(' ')
        price_list = [price_part[0].split('\xa0')[0].replace('.', ''), price_part[2].split('\xa0')[0].replace('.', '')]
        # compare
        check_list = [name, brand_list, eff_list, watt_list, modul_list, form_list, price_list]
        current_list = list(request.session['product_psu'].values())
        same_name = check_list[0] == current_list[0]
        same_tick = check_list[1:] == current_list[1:len(current_list) - 1]
        if same_name and same_tick:
            print('same search - psu')
            return JsonResponse({"psu_list": GetItemFromDatabase.convert_psu_db_to_dic(
                request.session['product_psu']['data'])})
        elif not same_tick:
            print('new tick search - psu')
            db_data = GetItemFromDatabase.search_psu(brand=brand_list, eff=eff_list, watt=watt_list, modul=modul_list, form=form_list,
                                                     price=price_list)
            request.session['product_psu']['psuname'] = name
            request.session['product_psu']['psubrand'] = brand_list
            request.session['product_psu']['psuefficientrating'] = eff_list
            request.session['product_psu']['psuwattage'] = watt_list
            request.session['product_psu']['psumodularity'] = modul_list
            request.session['product_psu']['psuformfactor'] = form_list
            request.session['product_psu']['psuprice'] = price_list
            request.session['product_psu']['data'] = db_data
            return JsonResponse({"psu_list": GetItemFromDatabase.convert_psu_db_to_dic(
                GetItemFromDatabase.search(request.session['product_psu']['psuname'], db_data))})
        elif not same_name and same_tick:
            print('new name same tick search - psu')
            request.session['product_psu']['psuname'] = name
            return JsonResponse({"psu_list": GetItemFromDatabase.convert_psu_db_to_dic(
                GetItemFromDatabase.search(request.session['product_psu']['psuname'],
                                           request.session['product_psu']['data']))})


def product_case(request):
    data = GetItemFromDatabase.search_case(brand=[], typ=[], form=[], price=["", ""])
    request.session['product_case'] = {
        'casename': '',
        'casebrand': [],
        'casetype': [],
        'caseformfactor': [],
        'caseprice': ["", ""],
        'data': data
    }
    return render(request, "builder/product_case.html", {"case_list": GetItemFromDatabase.convert_case_db_to_dic(data)})


def product_case_search(request):
    if request.POST:
# case name
        name = request.POST.get('casename')
# case brand
        brand_list = request.POST.getlist('casebrand')
        if brand_list[0] == 'all':
            brand_list = []
# case type
        type_list = request.POST.getlist('casetype')
        if type_list[0] == 'all':
            type_list = []
# case form factor
        form_list = request.POST.getlist('caseformfactor')
        if form_list[0] == 'all':
            form_list = []
# case price
        price_part = request.POST.get('caseprice').split(' ')
        price_list = [price_part[0].split('\xa0')[0].replace('.', ''), price_part[2].split('\xa0')[0].replace('.', '')]
# compare
        check_list = [name, brand_list, type_list, form_list, price_list]
        current_list = list(request.session['product_case'].values())
        same_name = check_list[0] == current_list[0]
        same_tick = check_list[1:] == current_list[1:len(current_list) - 1]
        if same_name and same_tick:
            print('same search - case')
            return JsonResponse({"psu_list": GetItemFromDatabase.convert_case_db_to_dic(
                request.session['product_case']['data'])})
        elif not same_tick:
            print('new tick search - case')
            db_data = GetItemFromDatabase.search_case(brand=brand_list, typ=type_list,
                                                     form=form_list,
                                                     price=price_list)
            request.session['product_case']['casename'] = name
            request.session['product_case']['casebrand'] = brand_list
            request.session['product_case']['casetype'] = type_list
            request.session['product_case']['caseformfactor'] = form_list
            request.session['product_case']['psuprice'] = price_list
            request.session['product_case']['data'] = db_data
            return JsonResponse({"case_list": GetItemFromDatabase.convert_case_db_to_dic(
                GetItemFromDatabase.search(request.session['product_case']['casename'], db_data, no_brand=True))})
        elif not same_name and same_tick:
            print('new name same tick search - case')
            request.session['product_case']['casename'] = name
            return JsonResponse({"case_list": GetItemFromDatabase.convert_case_db_to_dic(
                GetItemFromDatabase.search(request.session['product_case']['casename'],
                                           request.session['product_case']['data'], no_brand=True))})


def pc_to_pdf(request):
    if 'check_pdf_point' not in request.session:
        return JsonResponse({'mess': 0})
    else:
        if not request.session['check_pdf_point']:
            GetItemFromDatabase.update_score(request.session['pc_id_in_db'], request.session['interact_point'], 'confirm')
            request.session['check_pdf_point'] = True
    return PcToPdf.pc_to_pdf(request.session['pc'])


def login_page(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            print('valid user')
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('http://127.0.0.1:8000/demo/')
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            messages.error(request, "Wrong username or password")
    return render(request, 'builder/login.html')


def logout_page(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/demo/login/')


def register_page(request):
    form = createUserForm()
    if request.method == "POST":
        form = createUserForm(request.POST)
        if form.is_valid():
            # print("valid form")
            messages.success(request, "Account created successfully. Log in with your newly created account!")
            form.save()
            return redirect('http://127.0.0.1:8000/demo/login/')
        else:
            print('invalid form')
    return render(request, 'builder/register.html', {'form': form})


@csrf_exempt
def testing(request):
    if cache.get('cpu_list') is None:
        cpu_list = GetItemFromDatabase.get_cpu_list_from_db()
        json_cpu_list = json.dumps(cpu_list)
        cache.set('cpu_list', json_cpu_list)
        print('get list from db with length', len(cpu_list))
    else:
        cpu_list = json.loads(cache.get('cpu_list'))
        print('get list from cache with length', len(cpu_list))
    return render(request, 'testing.html')

