from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage, FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm,UserRegisterForm,AddCommentForm
from .models import Photo, Preference,Comment

# Create your views here.
from django.views import View

# class MainView(View):
#     template_name = 'instagram/index.html'
#
#     def get(self, request):
#         if request.user.is_authenticated:
#             images = Photo.objects.filter(author=request.user).order_by('-creation_date')
#         else:
#             images = Photo.objects.all().order_by('-creation_date')
#         return render(request, self.template_name,{'images': images})

class MainView(View):
    template_name = 'instagram/index.html'

    def get(self, request):
        images = Photo.objects.all().order_by('-creation_date')
        return render(request, self.template_name, {'images': images})

class ProfileView(LoginRequiredMixin, View):
    template_name = 'instagram/profile.html'

    def get(self, request):

        if request.user.is_authenticated:
            form = UploadFileForm()
            images = Photo.objects.filter(author=request.user).order_by('-creation_date')
        else:
            images = Photo.objects.all().order_by('-creation_date')
            return render(request, self.template_name, {'images': images})
        return render(request, self.template_name, {'images': images, 'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        images = Photo.objects.filter(author=request.user).order_by('-creation_date')
        if form.is_valid():
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            photo_to_save = Photo(author=request.user, title=form.cleaned_data.get('title'), path=uploaded_file_url)
            photo_to_save.save(force_insert=True)
            return render(request, self.template_name, {
                'uploaded_file_url': uploaded_file_url, 'form': form, 'images': images
            })
        return render(request, self.template_name, {'form': form, 'images': images})


class UploadPhotoView(LoginRequiredMixin,View):
    template_name = 'instagram/upload_photo.html'

    def get(self,request):
        form=UploadFileForm()
        return render(request, self.template_name,{'form':form})

    def post(self,request):
        form=UploadFileForm(request.POST,request.FILES)
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


class PhotoDetailView(LoginRequiredMixin,View):
    template_name = 'instagram/photo_details.html'

    def get(self, request, pk):
        photo=get_object_or_404(Photo, pk=pk)
        add_comment = AddCommentForm()
        return render(request, self.template_name,
                      {'photo': photo,'add_comment':add_comment})

    def post(self, request, pk):
        add_comment = AddCommentForm(request.POST)
        photo = Photo.objects.get(pk=pk)
        if add_comment.is_valid():
            content = add_comment.cleaned_data.get('content')
            new_comment = Comment(
                text=content, author=request.user, photo=photo)
            new_comment.save()
            add_comment = AddCommentForm()
        return render(request, self.template_name,
                      {'photo': photo, 'add_comment': add_comment})

class PostPreferenceView(LoginRequiredMixin,View):
    template_name = 'instagram/photo_details.html'
    def get(self,request,photo_id,preference_type):
        photo = get_object_or_404(Photo, id=photo_id)
        add_comment = AddCommentForm()
        ctx = {'photo': photo,'add_comment': add_comment}
        return render(request, self.template_name, ctx)

    def post(self,request,photo_id,preference_type):
        photo=get_object_or_404(Photo,id=photo_id)
        #add_comment = AddCommentForm()

        # if 'addbtn' in request.POST:
        #     add_comment = AddCommentForm(request.POST)
        #     if add_comment.is_valid():
        #         content = add_comment.cleaned_data.get('content')
        #         new_comment = Comment(
        #             text=content, author=request.user, photo=photo)
        #         new_comment.save()
        #         add_comment = AddCommentForm()
        #     ctx={'photo':photo,'add_comment':add_comment}
        #     return render(request, self.template_name, ctx)


        try:
            preference=Preference.objects.get(user=request.user, photo=photo)
            preference_value=int(preference.value)
            preference_type=int(preference_type)

            if preference_value != preference_type:
                preference.delete()
                new_preference = Preference(user=request.user,photo=photo,value=preference_type)

                if preference_type == 1 and preference_value != 1:
                    photo.likes += 1
                    photo.dislikes -= 1
                elif preference_type == 2 and preference_value != 2:
                    photo.dislikes += 1
                    photo.likes -= 1
                new_preference.save()
                photo.save()

                #ctx = {'photo': photo, 'add_comment': add_comment}
                ctx = {'photo': photo}

                # return render(request, self.template_name, ctx)
                return redirect('instagram:photo-details', pk=photo.pk)

            elif preference_value == preference_type:
                preference.delete()

                if preference_type == 1:
                    photo.likes -= 1
                elif preference_type == 2:
                    photo.dislikes -= 1

                photo.save()
                #ctx = {'photo': photo, 'add_comment': add_comment}
                ctx = {'photo': photo}

                # return render(request, self.template_name, ctx)
                return redirect('instagram:photo-details', pk=photo.pk)

        except Preference.DoesNotExist:

            new_preference = Preference(user=request.user,photo=photo,value=preference_type)
            preference_type = int(preference_type)

            if preference_type == 1:
                photo.likes += 1
            elif preference_type == 2:
                photo.dislikes += 1

            new_preference.save()
            photo.save()
            #ctx = {'photo': photo, 'add_comment': add_comment}
            ctx = {'photo': photo}
            #return render(request, self.template_name, ctx)
            return redirect('instagram:photo-details', pk=photo.pk)


