from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Pegawai, Barista


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