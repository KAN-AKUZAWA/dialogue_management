from django.shortcuts import render, redirect
from .forms import FileUploadForm, SearchForm
from word_to_db import Word_to_DB
from Register_and_Search.models import dialogue, Character
from .models import FileUpload
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.http import HttpResponse
import urllib.parse
import hashlib

def frontpage(request):
    return render(request, "dialogue/frontpage.html")

def upload_success(request):
    return render(request, 'dialogue/upload_success.html')

def v_error(request):
    return render(request, 'dialogue/v_error.html')

def f_error(request):
    return render(request, 'dialogue/f_error.html')

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():

            def delete_file_and_db(filename, filepath):
                os.remove(filepath)
                file_upload_exists = FileUpload.objects.filter(file_name=filename).exists()
                dialogue_exists = dialogue.objects.filter(filename=filename).exists()
                if file_upload_exists:
                    records_to_delete = FileUpload.objects.filter(file_name=filename)
                    records_to_delete.delete()
                if dialogue_exists:
                    records_to_delete = dialogue.objects.filter(filename=filename)
                    records_to_delete.delete()
            
            uploaded_file = form.cleaned_data['uploaded_file']
            file_content = uploaded_file.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            hash_list = FileUpload.objects.values_list('file_hash', flat=True)
            if file_hash in hash_list:
                return redirect('v_error/')
            else:
                pattern = "新規登録"
                uploaded_file = form.cleaned_data['uploaded_file']
                filename_list = FileUpload.objects.values_list('file_name', flat=True).distinct()
                filename = uploaded_file.name
                if filename in filename_list:
                        file_obj = FileUpload.objects.get(file_name = filename)
                        filepath = file_obj.uploaded_file.path
                        delete_file_and_db(filename, filepath)
                        pattern = "上書き"
                created_at = form.cleaned_data['created_at']
                form.save(commit=False)
                file_obj = FileUpload(uploaded_file=uploaded_file, file_name=filename)
                file_obj.created_at = created_at
                file_obj.file_hash = file_hash
                file_obj.save()
                # アップロードが成功した後の処理
                def get_file_path_by_hash(file_hash):        
                    file_obj = FileUpload.objects.get(file_hash=file_hash)
                    return file_obj.uploaded_file.path
                file_path = get_file_path_by_hash(file_hash)
                character_list = Character.objects.values_list('character', flat=True)
                run = Word_to_DB(file_path, filename, created_at, character_list)
                flag = run.run()
                if flag == 0:
                    # 想定外のフォーマットであることを通知するエラー画面を表示
                    delete_file_and_db(filename, file_path)
                    return redirect('f_error/')
                else:
                    # アップロード成功画面を表示
                    return redirect(f'success/?pattern={pattern}')

    else:
        form = FileUploadForm()
    
    return render(request, 'dialogue/upload.html', {'form': form})

def search_dialogue(request):
    form = SearchForm(request.GET or None)
    if form.is_valid():
        results = form.get_search_results()
    else:
        results = None

    context = {
        'form': form,
        'results': results
    }
    return render(request, 'dialogue/search_dialogue.html', context)

def download_file(request, file_path, filename):
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    quoted_filename = urllib.parse.quote(filename)
    if os.path.exists(file_full_path):
        with open(file_full_path, 'rb') as file:
            file_content = file.read()  # ファイルの内容を変数に読み込む
        response = HttpResponse(file_content, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename="{quoted_filename}"; filename*=UTF-8"{quoted_filename}"'
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        return response
    else:
        raise Http404("ファイルが見つかりません。")
