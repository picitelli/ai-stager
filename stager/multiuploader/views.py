from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from models import MultiuploaderImage
from django.core.files.uploadedfile import UploadedFile
from staging.models import CompSlide, Comp
from django.forms.models import inlineformset_factory
from django.template import loader, Context
from django.contrib.admin import widgets, helpers
from stager.staging.admin import CompSlideInline 
from stager.staging.forms import *

#importing json parser to generate jQuery plugin friendly json response
from django.utils import simplejson

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail


from django.views.decorators.csrf import csrf_exempt

import logging
log = logging

@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. image id='+str(pk))
        image = get_object_or_404(MultiuploaderImage, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def multiuploader(request):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        print "HIIIII"
        comp_id = request.POST.get('compId', None)
        print comp_id
        try:
            print comp_id
            comp = Comp.objects.get(id=comp_id)
        except:
            return HttpResponseBadRequest('Comp Does Not Exist')
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        
        slide = CompSlide()
        slide.title = filename
        slide.image = file
        slide.comp = comp
        slide.name = "NAME"
        slide.save()
        
        log.info ('Got file: "%s"' % str(filename))
        log.info('Content type: "$s" % file.content_type')
        

        

        #writing file manually into model
        #because we don't need form of any type.
        image = MultiuploaderImage()
        image.filename=str(filename)
        image.image=file
        image.key_data = image.key_generate
        #image.save()
        log.info('File saving done')

        #getting thumbnail url using sorl-thumbnail
        #if 'image' in file.content_type.lower():
        #    im = get_thumbnail(image, "80x80", quality=50)
        #    thumb_url = im.url
        #else:
        thumb_url = ''

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
            file_url = settings.MULTI_IMAGE_URL+'/'+image.key_data+'/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/'+image.key_data+'/'
        slide_fields = ('name','image','alignment','backgroundfield', 'remove_background', 'background_colorfield', 'active', 'ordering')
        InlineAdminFormSetFactory = inlineformset_factory(Comp, CompSlide, extra=0, can_order=True, can_delete=True, fields=slide_fields)
        inline_admin_formset = InlineAdminFormSetFactory(instance=comp)
                #inline_admin_formset.opts.sortable_field_name = "ordering"
        """from django.contrib import admin
                admin_site = admin.site
                inline = CompSlideInline(Comp, admin_site)
                prefix = FormSet.get_default_prefix()
                formset = FormSet(instance=self.model(), prefix=prefix,
                                          queryset=inline.queryset(request))
                inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                        fieldsets, prepopulated, readonly, model_admin=self)
                """
                #print inline_admin_formset
                #print "%s" % inline_admin_formset
        t = loader.get_template('admin/staging/edit_inline/_comp_slide_drag_upload_ajax.html')
        c = Context({ 'inline_admin_formset': inline_admin_formset, 'slide_fields': slide_fields })
        rendered = t.render(c)
        # print rendered
        print 'got rendered?'

        #generating json response array
        result = []
        result.append({"name":filename, 
                       "size":file_size, 
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       #"delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",
                       "html": rendered })
        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')

def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(MultiuploaderImage, key_data=key)
    url = settings.MEDIA_URL+image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})