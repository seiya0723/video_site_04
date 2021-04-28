from django.shortcuts import render, redirect

from django.views import View
from .models import Video,Category,Tag
from .forms import VideoForm, VideoEditForm

from django.db.models import Q

from django.http.response import JsonResponse


#python-magicで受け取ったファイルのMIMEをチェックする。
#MIMEについては https://developer.mozilla.org/ja/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types を参照。

import magic
ALLOWED_MIME   = ["video/mp4"]

# アップロードの上限
LIMIT_SIZE     = 200 * 1000 * 1000

class IndexView(View):

    def get(self, request, *args, **kwargs):

        
        categories  = Category.objects.all()
        tags        = Tag.objects.all()



        if "search" in request.GET:

            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("tube:index")


            search = request.GET["search"].replace("　", " ")
            search_list = search.split(" ")


            query = Q()
            for word in search_list:

                if "option" in request.GET:
                    query |= Q(comment__contains=word)
                else:
                    query &= Q(comment__contains=word)


            videos = Video.objects.filter(query).order_by("-dt")
        else:
            videos = Video.objects.all().order_by("-dt")


        context = { "videos": videos,
                    "categories":categories,
                    "tags":tags
                }


        return render(request, "tube/index.html", context)

    def post(self, request, *args, **kwargs):

        # TIPS:request.POSTだけでなく、request.FILESも引数に入れる。
        formset = VideoForm(request.POST, request.FILES)

        fileflag  = False


        if "movie" in request.FILES:
            mime_type  = magic.from_buffer(request.FILES["movie"].read(1024),mime=True)

            if request.FILES["movie"].size >= LIMIT_SIZE:

                mb     = str(LIMIT_SIZE / 1000000)
                json= { "error":True,
                        "message":"The maximum file size is " + mb + "MB." }

                return JsonResponse(json)

            if mime_type not in ALLOWED_MIME:

                mime   = str(ALLOWED_MIME)
                json   = { "error":True,
                           "message":"The file you can post is " + mime + "." }

                return JsonResponse(json)

            if mime_type in ALLOWED_MIME:
                fileflag  = True
        else:
            fileflag  = True

        # ↑アップロードされたファイルが許可されているMIMEである、もしくはアップロードされていない場合。リクエストの保存を許可する。

        if formset.is_valid():
            print("バリデーションOK")

            if fileflag:
                formset.save()
            else:
                print("このファイルは許可されていません。")

        else:
            print("バリデーションエラー")


        return redirect("tube:index")

index = IndexView.as_view()


class DeleteView(View):

    def get(self, request, pk, *args, **kwargs):

        video   = Video.objects.filter(id=pk).first()
        context = { "video":video }

        return render(request, "tube/delete.html", context )


    def post(self, request, pk, *args, **kwargs):

        print("削除")

        # .first()で一番上のレコードを1つ取る。
        video    = Video.objects.filter(id=pk).first()
        video.delete()

        # TIPS:すでにurls.pyにてpkが数値型であることがわかっているので、バリデーションをする必要はない。

        return redirect("tube:index")

delete = DeleteView.as_view()


class UpdateView(View):

    def get(self, request, pk, *args, **kwargs):

        video   = Video.objects.filter(id=pk).first()
        context = { "video":video }

        return render(request, "tube/update.html", context )

    def post(self, request, pk, *args, **kwargs):

        # まず、編集対象のレコード特定
        instance    = Video.objects.filter(id=pk).first()

        # 第2引数にinstanceを指定することで、対象の編集ができる。
        formset     = VideoEditForm(request.POST, instance=instance)

        if formset.is_valid():
            print("バリデーションOK")
            formset.save()

            Video.objects.filter(id=pk).update(edited=True)

        else:
            print("バリデーションNG")

        return redirect("tube:index")


update  = UpdateView.as_view()
