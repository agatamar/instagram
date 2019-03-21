from django.core.files.storage import default_storage, FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm,UserRegisterForm
from .models import Photo

# Create your views here.
from django.views import View


def handle_uploaded_file(f):
    with open('media/images/', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class MainView(View):
    template_name = 'instagram/index.html'

    def get(self, request):
        images = Photo.objects.filter(author=request.user)
        return render(request, self.template_name,{'images': images})



class UploadPhotoView(View):
    template_name = 'instagram/upload_photo.html'

    #działa!!!
    # def get(self,request):
    #     return render(request, self.template_name)

    # def post(self,request):
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         handle_uploaded_file(request.FILES['file'])
    #         return redirect('/')

    # działa!!!
    # def post(self,request):
    #     myfile = request.FILES['myfile']
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
    #     uploaded_file_url = fs.url(filename)
    #     return render(request, self.template_name, {
    #         'uploaded_file_url': uploaded_file_url
    #     })

    def get(self,request):
        form=UploadFileForm()
        photos=Photo.objects.filter(author=request.user)
        return render(request, self.template_name,{'form':form})

    def post(self,request):
        form=UploadFileForm(request.POST,request.FILES)
        photos = Photo.objects.filter(author=request.user)
        if form.is_valid():
            myfile=request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            photo_to_save = Photo(author=request.user, title=form.cleaned_data.get('title'), path=uploaded_file_url)
            photo_to_save.save(force_insert=True)
            return render(request, self.template_name, {
                    'uploaded_file_url': uploaded_file_url,'form':form
                })
        return render(request, self.template_name,{'form':form})

class RegisterView(View):
    template_name = 'instagram/register.html'
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})


