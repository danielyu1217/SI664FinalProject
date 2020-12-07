from django import forms
from restaurants.models import Restaurant
from django.core.files.uploadedfile import InMemoryUploadedFile
from restaurants.humanize import naturalsize

# strip means to remove whitespace from the beginning and the end before storing the column
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)


# Create the form class.
# class CreateForm(forms.ModelForm):
#     max_upload_limit = 2 * 1024 * 1024
#     max_upload_limit_text = naturalsize(max_upload_limit)

#     # Call this 'picture' so it gets copied from the form to the in-memory model
#     # It will not be the "bytes", it will be the "InMemoryUploadedFile"
#     # because we need to pull out things like content_type
#     picture = forms.FileField(required=False, label='File to Upload <= '+max_upload_limit_text)
#     upload_field_name = 'picture'

#     class Meta:
#         model = Restaurant
#         fields = ['name', 'description',  'location', 'category', 'tag1', 'tag2', 'tag3', 'rating', 'price']

#     # Validate the size of the picture
#     def clean(self):
#         cleaned_data = super().clean()
#         pic = cleaned_data.get('picture')
#         if pic is None:
#             return
#         if len(pic) > self.max_upload_limit:
#             self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

#     # Convert uploaded File object to a picture
#     def save(self, commit=True):
#         instance = super(CreateForm, self).save(commit=False)

#         # We only need to adjust picture if it is a freshly uploaded file
#         f = instance.picture   # Make a copy
#         if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
#             bytearr = f.read()
#             instance.content_type = f.content_type
#             instance.picture = bytearr  # Overwrite with the actual image data

#         if commit:
#             instance.save()

#         return instance