from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Pegawai, Barista, Waiter, Cleaner
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST

def index(request):
    barista_list = Barista.objects.all()
    waiter_list = Waiter.objects.all()
    cleaner_list = Cleaner.objects.all()

    semua_pegawai = []

    for b in barista_list:
        b.total_gaji = b.jam_kerja * b.gaji_per_jam + b.jumlah_jam * b.bonus_per_jam
        semua_pegawai.append({
            "id_pegawai": b.id_pegawai,
            "nama": b.nama,
            "posisi": "Barista",
            "shift": b.shift,
            "gaji_per_jam": b.gaji_per_jam,
            "jam_kerja": b.jam_kerja,
            "total_gaji": b.total_gaji,
            "jenis": "barista",
        })

    for w in waiter_list:
        w.total_gaji = w.jam_kerja * w.gaji_per_jam + w.jumlah_jam * w.bonus_per_jam
        semua_pegawai.append({
            "id_pegawai": w.id_pegawai,
            "nama": w.nama,
            "posisi": "Waiter",
            "shift": w.shift,
            "gaji_per_jam": w.gaji_per_jam,
            "jam_kerja": w.jam_kerja,
            "total_gaji": w.total_gaji,
            "jenis": "waiter",
        })

    for c in cleaner_list:
        c.total_gaji = c.jam_kerja * c.gaji_per_jam + c.jumlah_jam * c.bonus_per_jam
        semua_pegawai.append({
            "id_pegawai": c.id_pegawai,
            "nama": c.nama,
            "posisi": "Cleaner",
            "shift": c.shift,
            "gaji_per_jam": c.gaji_per_jam,
            "jam_kerja": c.jam_kerja,
            "total_gaji": c.total_gaji,
            "jenis": "cleaner",
        })

    context = {
        'semua_pegawai': semua_pegawai,
        'barista_list': barista_list,
        'waiter_list': waiter_list,
        'cleaner_list': cleaner_list,
        'total_pegawai': len(semua_pegawai),
        'total_barista': barista_list.count(),
        'total_waiter': waiter_list.count(),
        'total_cleaner': cleaner_list.count(),
    }
    return render(request, 'pegawai/index.html', context)


model_map = {
    'barista': Barista,
    'waiter': Waiter,
    'cleaner': Cleaner,
}

@require_POST
def add_pegawai(request):
    jenis = request.POST.get('jenis')
    Model = model_map.get(jenis)
    if not Model:
        messages.error(request, 'Jenis pegawai tidak valid')
        return redirect('pegawai:pegawai_index')

    Model.objects.create(
        id_pegawai=request.POST.get('id_pegawai'),
        nama=request.POST.get('nama'),
        shift=request.POST.get('shift'),
        gaji_per_jam=request.POST.get('gaji_per_jam'),
        bonus_per_jam=request.POST.get('bonus_per_jam'),
        jam_kerja=request.POST.get('jam_kerja') or 0,
        jumlah_jam=request.POST.get('jumlah_jam') or 0,
    )
    messages.success(request, f'{jenis.title()} baru ditambahkan.')
    return redirect('pegawai:pegawai_index')


@require_POST
def delete_employee(request):
    jenis = request.POST.get('jenis')
    Model = model_map.get(jenis)
    if not Model:
        messages.error(request, 'Jenis pegawai tidak valid')
        return redirect('pegawai:pegawai_index')

    id_pegawai = request.POST.get('id_pegawai')
    deleted, _ = Model.objects.filter(id_pegawai=id_pegawai).delete()
    if deleted:
        messages.success(request, f'{jenis.title()} {id_pegawai} dihapus.')
    else:
        messages.warning(request, 'ID pegawai tidak ditemukan.')
    return redirect('pegawai:pegawai_index')


@require_http_methods(["GET"])
def list_pegawai(request):
    pegawai = Pegawai.objects.all().values()
    return JsonResponse(list(pegawai), safe=False)

@require_http_methods(["GET"])
def detail_pegawai(request, id_pegawai):
    try:
        peg = Pegawai.objects.get(id_pegawai=id_pegawai)
        return JsonResponse({
            'id_pegawai': peg.id_pegawai,
            'nama': peg.nama,
            'posisi': peg.posisi,
            'shift': peg.shift,
            'gaji_per_jam': float(peg.gaji_per_jam),
            'jam_kerja': peg.jam_kerja,
        })
    except Pegawai.DoesNotExist:
        return JsonResponse({'error': 'Pegawai tidak ditemukan'}, status=404)

@require_http_methods(["POST"])
def create_pegawai(request):
    import json
    data = json.loads(request.body)
    peg = Pegawai.objects.create(
        id_pegawai=data['id_pegawai'],
        nama=data['nama'],
        posisi=data['posisi'],
        shift=data['shift'],
        gaji_per_jam=data['gaji_per_jam']
    )
    return JsonResponse({'status': 'success', 'message': 'Pegawai berhasil ditambahkan'})


@require_http_methods(["PUT"])
def update_pegawai(request, id_pegawai):
    import json
    try:
        peg = Pegawai.objects.get(id_pegawai=id_pegawai)
        data = json.loads(request.body)
        peg.nama = data.get('nama', peg.nama)
        peg.posisi = data.get('posisi', peg.posisi)
        peg.shift = data.get('shift', peg.shift)
        peg.gaji_per_jam = data.get('gaji_per_jam', peg.gaji_per_jam)
        peg.save()
        return JsonResponse({'status': 'success', 'message': 'Pegawai berhasil diupdate'})
    except Pegawai.DoesNotExist:
        return JsonResponse({'error': 'Pegawai tidak ditemukan'}, status=404)


@require_http_methods(["DELETE"])
def delete_pegawai(request, id_pegawai):
    try:
        peg = Pegawai.objects.get(id_pegawai=id_pegawai)
        peg.delete()
        return JsonResponse({'status': 'success', 'message': 'Pegawai berhasil dihapus'})
    except Pegawai.DoesNotExist:
        return JsonResponse({'error': 'Pegawai tidak ditemukan'}, status=404)


@require_http_methods(["GET"])
def list_barista(request):
    barista = Barista.objects.all().values()
    return JsonResponse(list(barista), safe=False)