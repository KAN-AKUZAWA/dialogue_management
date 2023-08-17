from django import forms
from .models import FileUpload, dialogue

class FileUploadForm(forms.ModelForm):
    uploaded_file = forms.FileField(
        label='ファイルアップロード',
        help_text='<br><br>※ 許可されているファイル形式は.docxです。'
    )
    created_at = forms.DateTimeField(
        label='ファイルの作成日',
        widget=forms.widgets.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = FileUpload
        fields = ['uploaded_file', 'created_at']

    def clean_uploaded_file(self):
        uploaded_file = self.cleaned_data.get('uploaded_file')
        if uploaded_file:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension != "docx":
                raise forms.ValidationError("許可されていないファイル形式です。.docxファイルをアップロードしてください。")
        return uploaded_file
    
class SearchForm(forms.Form):
    keyword = forms.CharField(label='キーワード', max_length=100)
    character = forms.CharField(label='キャラクター', max_length=100, required=False)
    filename = forms.CharField(label='ファイル名', max_length=100, required=False)
    dialogue = forms.CharField(label='台詞', max_length=100, required=False)
    place = forms.CharField(label='場面', max_length=100, required=False)
    created_from = forms.DateField(label='作成日（開始）', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    created_to = forms.DateField(label='作成日（終了）', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def get_search_results(self):
        keyword = self.cleaned_data.get('keyword')
        character = self.cleaned_data.get('character')
        filename = self.cleaned_data.get('filename')
        Dialogue = self.cleaned_data.get('dialogue')
        place = self.cleaned_data.get('place')
        created_from = self.cleaned_data.get('created_from')
        created_to = self.cleaned_data.get('created_to')

        results = dialogue.objects.filter(dialogue__icontains=keyword)
        if character:
            results = results.filter(character__icontains=character)
        if filename:
            results = results.filter(filename__icontains=filename)
        if Dialogue:
            results = results.filter(dialogue__icontains=Dialogue)
        if place:
            results = results.filter(place__icontains=place)
        if created_from and created_to:
            results = results.filter(created_date__range=(created_from, created_to))

        return results