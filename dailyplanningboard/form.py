from django import forms
from .models import TaskList

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['UnitSystem','Department','Permit','SAPNum','Description','Remarks','Priority','Status','CreatedDate','LastActivity','MonthYearID']