from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Pegawai, Barista, Waiter, Cleaner
from django.shortcuts import render

def index(request):
    pegawai_list= Pegawai.objects.all() 
    barista_list= Barista.objects.all() 
    waiter_list= Waiter.objects.all() 
    cleaner_list= Cleaner.objects.all()

    semua_pegawai = []

    for peg in pegawai_list:
        peg.total_gaji = peg.jam_kerja * peg.gaji_per_jam

    for bar in barista_list:
        gaji_dasar = bar.jam_kerja * bar.gaji_per_jam
        bonus = bar.jumlah_jam * bar.bonus_per_jam
        bar.total_gaji = gaji_dasar + bonus
        bar.posisi = "Barista"
        bar.is_barista = True
        bar.is_waiter = False
        bar.is_cleaner = False
        semua_pegawai.append(bar)

    for wait in waiter_list:
        gaji_dasar = bar.jam_kerja * bar.gaji_per_jam
        bonus = wait.jam_kerja * bar.bonus_per_jam
        wait.total_gaji = gaji_dasar + bonus
        wait.posisi = "Waiter"
        wait.is_barista = False
        wait.is_waiter = True
        wait.is_cleaner = False
        semua_pegawai.append(wait)
        
    for clean in cleaner_list:
        gaji_dasar = bar.jam_kerja * bar.gaji_per_jam
        bonus = clean.jam_kerja * bar.bonus_per_jam
        clean.total_gaji = gaji_dasar + bonus
        clean.posisi = "Cleaner"
        clean.is_barista = False
        clean.is_waiter = False
        clean.is_cleaner = True
        semua_pegawai.append(clean)

    context = {
        'pegawai_list': pegawai_list,
        'barista_list': barista_list,
        'waiter_list': waiter_list,
        'cleaner_list': cleaner_list,
        'total_pegawai': len(semua_pegawai),
        'total_barista': len(barista_list),
        'total_waiter': len(waiter_list),
        'total_cleaner': len(cleaner_list)
    }
    return render(request, 'pegawai/index.html', context)

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