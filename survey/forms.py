from django import forms



class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


# class HorizontalRadioRenderer(forms.RadioSelect.renderer):
#     def render(self):
#         return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

#
# class SurveyForm(models.ModelForm):
#     class Meta:
#         model = SurveyQuestion
#         fields = ('survey', 'question')
#
#     def __init__(self, *args, **kwargs):
#         # expects a survey object to be passed in initially
#         survey = kwargs.pop('survey')
#         self.survey = survey
#         super(SurveyForm, self).__init__(*args, **kwargs)
#
#         # add a field for each survey question, corresponding to the question
#         # type as appropriate.
#         data = kwargs.get('data')
#         for q in Survey.questions():
#             if q.question_type == Question.TEXT:
#                 self.fields["question_%d" % q.pk] = forms.CharField(label=q.text,
#                                                                     widget=forms.Textarea)
#             elif q.question_type == Question.RADIO:
#                 question_choices = q.get_choices()
#                 self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text,
#                                                                       widget=forms.RadioSelect(
#                                                                                                 ),
#                                                                       choices=question_choices)
#             elif q.question_type == Question.SELECT:
#                 question_choices = q.get_choices()
#                 # add an empty option at the top so that the user has to
#                 # explicitly select one of the options
#                 question_choices = tuple([('', '-------------')]) + question_choices
#                 self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text,
#                                                                       widget=forms.Select, choices=question_choices)
#             elif q.question_type == Question.SELECT_MULTIPLE:
#                 question_choices = q.get_choices()
#                 self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(label=q.text,
#                                                                               widget=forms.CheckboxSelectMultiple,
#                                                                               choices=question_choices)
#             elif q.question_type == Question.INTEGER:
#                 self.fields["question_%d" % q.pk] = forms.IntegerField(label=q.text)
#
#             # if the field is required, give it a corresponding css class.
#             if q.required:
#                 self.fields["question_%d" % q.pk].required = True
#                 self.fields["question_%d" % q.pk].widget.attrs["class"] = "required"
#             else:
#                 self.fields["question_%d" % q.pk].required = False
#
#
