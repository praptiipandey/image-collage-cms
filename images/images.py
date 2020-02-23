
from django.shortcuts import render, redirect
from dashboard import context_processors
# Create your views here.
from account.decorators import my_login_required
from django.views import View
from base64 import b64encode
# import mstream as mStream
# import cStringIO
from io import StringIO
import base64
from pymongo import MongoClient
from gridfs import GridFS
import os
import mimetypes
import numpy as np
import cv2
from skimage.util import montage
from os import listdir
from os import stat
from heapq import nsmallest
from django.http import HttpResponse


client = MongoClient('localhost', 27017)
db = client['local']


fs = GridFS(db)

class Images(View):

    @my_login_required
    def get(self, request):
        # if 'user' in request.session:
        img_path = '/home/nishchit/data/images/predictions/'
        files = os.listdir(img_path)
        img = []
        all_images = []
        all_name=[]
        # mos =[]
        data = {}
        filename = []
        for file in files:
            img_r = []
            img_b = []
            img_g = []
            date = '2019-05-20'
            path = img_path + file + '/' + date + '/'
            if os.path.exists(path):
                listfile = listdir(path)
                smallest = nsmallest(9, listfile)
                # print(smallest)
                if smallest != []:
                    for image in smallest:
                        abs_path = path + image
                        img_r.append(cv2.imread(abs_path)[:, :, 0])
                        img_b.append(cv2.imread(abs_path)[:, :, 1])
                        img_g.append(cv2.imread(abs_path)[:, :, 2])
                    # print(img_b)
                    mos_r = montage(np.asarray(img_r))
                    mos_b = montage(np.asarray(img_b))
                    mos_g = montage(np.asarray(img_g))

                    mos = []
                    mos.append(mos_r)
                    mos.append(mos_b)
                    mos.append(mos_g)

                    cv2.imwrite("/home/data/r4.jpg", mos_r)
                    cv2.imwrite("/home/data/b4.jpg", mos_b)
                    cv2.imwrite("/home/data/g4.jpg", mos_g)

                    mos = np.stack(np.asarray(mos), -1)
                    # print(mos.shape)
                    mon = ('/home/nishchit/data/images/' + '%s.jpg') % file
                    cv2.imwrite(mon, mos)
                    all_images.append(mon)
            # print(all_images)
        # for image in all_images:
        #     name = (image[-7:-4])

            with open(mon, "rb") as image_file:
                # print(image_file)
                fs.put(image_file, content_type="image/jpeg", filename=file)
                f_id = db.fs.files.find_one({'filename' :file })
                image = (b64encode((fs.get(f_id['_id']).read())).decode('utf8'))
                img.append(image)
                filename.append(file)
        global img,filename
        context = context_processors.base_variables_all(request)
        context['img'] = img

        return render(request, 'images.html',context)
        # else:
        #     return redirect('login')
class Selected(View):

    def get(self, request, user_id):
        img_path = '/home/nishchit/data/images/predictions/'+ filename[int(user_id)]
        files = os.listdir(img_path)
        filelist = []
        for file in files:
                filelist.append([file,filename[int(user_id)]])
        context = context_processors.base_variables_all(request)
        context['image'] = img[int(user_id)]
        context['filelist'] = filelist
        context['id'] = user_id
        # i = user_id
        # print(img[i])
        return render(request, 'selected_image.html', context)

class ListFiles(View):

    def get(self, request, user_date):
        print(user_date)
        context = context_processors.base_variables_all(request)
        return render(request, 'dashboard.html', context)