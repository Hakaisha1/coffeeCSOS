from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Pegawai, Barista, Waiter, Cleaner, Absensi
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from core.decorators import role_required
from django.utils import timezone
from collections import defaultdict
from datetime import datetime


@role_required(['GENERAL_MANAGER'])
def index(request):
    barista_list = Barista.objects.all()
    waiter_list = Waiter.objects.all()
    cleaner_list = Cleaner.objects.all()

    # --- REKAP ABSENSI BULAN INI ---
    today = timezone.now().date()
    absensi_bulan_ini_qs = Absensi.objects.filter(
        tanggal__year=today.year,
        tanggal__month=today.month,
    )

    # key: (jenis, id_pegawai) -> {jam, gaji}
    rekapan = defaultdict(lambda: {'jam_kerja': 0, 'jam_lembur': 0, 'gaji_total': 0})
    for a in absensi_bulan_ini_qs:
        k = (a.jenis, a.id_pegawai)
        rekapan[k]['jam_kerja'] += a.jam_kerja
        rekapan[k]['jam_lembur'] += a.jam_lembur_malam
        rekapan[k]['gaji_total'] += a.gaji_harian

    semua_pegawai = []

    total_gaji_barista_bulan_ini = int('0')
    total_gaji_waiter_bulan_ini = int('0')
    total_gaji_cleaner_bulan_ini = int('0')

    for b in barista_list:
        key = ('barista', b.id_pegawai)
        data = rekapan.get(key, {'jam_kerja': 0, 'jam_lembur': 0, 'gaji_total': 0})
        b.total_jam_bulan_ini = data['jam_kerja']
        b.total_jam_lembur_bulan_ini = data['jam_lembur']
        b.total_gaji_bulan_ini = data['gaji_total']
        total_gaji_barista_bulan_ini += b.total_gaji_bulan_ini

        semua_pegawai.append({
            "id_pegawai": b.id_pegawai,
            "nama": b.nama,
            "posisi": "Barista",
            "shift": b.shift,
            "gaji_per_jam": b.gaji_per_jam,
            "jam_kerja": b.total_jam_bulan_ini,
            "total_gaji": b.total_gaji_bulan_ini,
            "jenis": "barista",
        })

    for w in waiter_list:
        key = ('waiter', w.id_pegawai)
        data = rekapan.get(key, {'jam_kerja': 0, 'jam_lembur': 0, 'gaji_total': 0})
        w.total_jam_bulan_ini = data['jam_kerja']
        w.total_jam_lembur_bulan_ini = data['jam_lembur']
        w.total_gaji_bulan_ini = data['gaji_total']
        total_gaji_waiter_bulan_ini += b.total_gaji_bulan_ini

        semua_pegawai.append({
            "id_pegawai": w.id_pegawai,
            "nama": w.nama,
            "posisi": "Waiter",
            "shift": w.shift,
            "gaji_per_jam": w.gaji_per_jam,
            "jam_kerja": w.total_jam_bulan_ini,
            "total_gaji": w.total_gaji_bulan_ini,
            "jenis": "waiter",
        })

    for c in cleaner_list:
        key = ('cleaner', c.id_pegawai)
        data = rekapan.get(key, {'jam_kerja': 0, 'jam_lembur': 0, 'gaji_total': 0})
        c.total_jam_bulan_ini = data['jam_kerja']
        c.total_jam_lembur_bulan_ini = data['jam_lembur']
        c.total_gaji_bulan_ini = data['gaji_total']
        total_gaji_cleaner_bulan_ini += c.total_gaji_bulan_ini
        
        semua_pegawai.append({
            "id_pegawai": c.id_pegawai,
            "nama": c.nama,
            "posisi": "Cleaner",
            "shift": c.shift,
            "gaji_per_jam": c.gaji_per_jam,
            "jam_kerja": c.total_jam_bulan_ini,
            "total_gaji": c.total_gaji_bulan_ini,
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
        'absensi_bulan_ini': absensi_bulan_ini_qs.order_by('-tanggal', '-created_at'),
        'total_gaji_barista_bulan_ini': total_gaji_barista_bulan_ini,
        'total_gaji_waiter_bulan_ini': total_gaji_waiter_bulan_ini,
        'total_gaji_cleaner_bulan_ini': total_gaji_cleaner_bulan_ini,
    }
    return render(request, 'pegawai/index.html', context)


model_map = {
    'barista': Barista,
    'waiter': Waiter,
    'cleaner': Cleaner,
}

@role_required(['GENERAL_MANAGER'])
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
    )
    messages.success(request, f'{jenis.title()} baru ditambahkan.')
    return redirect('pegawai:pegawai_index')


@role_required(['GENERAL_MANAGER'])
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


@role_required(['GENERAL_MANAGER'])
@require_http_methods(["GET"])
def list_pegawai(request):
    pegawai = Pegawai.objects.all().values()
    return JsonResponse(list(pegawai), safe=False)

@role_required(['GENERAL_MANAGER'])
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

@role_required(['GENERAL_MANAGER'])
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


@role_required(['GENERAL_MANAGER'])
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


@role_required(['GENERAL_MANAGER'])
@require_http_methods(["DELETE"])
def delete_pegawai(request, id_pegawai):
    try:
        peg = Pegawai.objects.get(id_pegawai=id_pegawai)
        peg.delete()
        return JsonResponse({'status': 'success', 'message': 'Pegawai berhasil dihapus'})
    except Pegawai.DoesNotExist:
        return JsonResponse({'error': 'Pegawai tidak ditemukan'}, status=404)


@role_required(['GENERAL_MANAGER'])
@require_http_methods(["GET"])
def list_barista(request):
    barista = Barista.objects.all().values()
    return JsonResponse(list(barista), safe=False)


@role_required(['GENERAL_MANAGER'])
@require_POST
def add_absensi(request):
    jenis = request.POST.get('jenis')
    id_pegawai = request.POST.get('id_pegawai')
    tanggal_str = request.POST.get('tanggal')
    jam_masuk_str = request.POST.get('jam_masuk')
    jam_pulang_str = request.POST.get('jam_pulang')

    if not all([jenis, id_pegawai, tanggal_str, jam_masuk_str, jam_pulang_str]):
        messages.error(request, 'Data absensi belum lengkap.')
        return redirect('pegawai:pegawai_index')

    # convert string ke date & time
    tanggal = datetime.strptime(tanggal_str, '%Y-%m-%d').date()
    jam_masuk = datetime.strptime(jam_masuk_str, '%H:%M').time()
    jam_pulang = datetime.strptime(jam_pulang_str, '%H:%M').time()

    Absensi.objects.create(
        jenis=jenis,
        id_pegawai=id_pegawai,
        tanggal=tanggal,
        jam_masuk=jam_masuk,
        jam_pulang=jam_pulang,
    )  # jam_kerja & gaji_harian otomatis dihitung di model

    messages.success(request, f'Absensi {id_pegawai} pada {tanggal} tersimpan.')
    return redirect('pegawai:pegawai_index')