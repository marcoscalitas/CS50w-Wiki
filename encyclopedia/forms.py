from django import forms

class EntryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        hidden_title = kwargs.pop('hidden_title', False)
        super(EntryForm, self).__init__(*args, **kwargs)
        
        if hidden_title:
            self.fields['title'].widget = forms.HiddenInput()
        else:
            self.fields['title'].widget = forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter title"
            })
         
    
    title = forms.CharField(
        label="Title", 
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter title"
        }))
    
    content = forms.CharField(
        label="Content", 
        max_length=5000, 
        required=True,
        widget=forms.Textarea(attrs={
            "name": "content",
            "class": "form-control form-control-height",
            "rows": 4,
            "cols": 10,
            "placeholder": "Enter markdown content",
        }))