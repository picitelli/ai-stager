from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from models import MultiuploaderImage
from django.core.files.uploadedfile import UploadedFile
from staging.models import CompSlide, Comp
from django.forms.models import inlineformset_factory
from django.template import loader, Context
from django.contrib.admin import widgets, helpers
from stager.staging.admin import CompSlideInline, CompAdmin
from stager.staging.forms import *
from django.db import transaction
from django.contrib import admin
from stager.staging.decorators import superuser_only

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
@superuser_only
def multiuploader(request):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        with transaction.commit_on_success():
            comp_id = request.POST.get('compId', None)
            try:
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
            prepared_filename = os.path.splitext(filename)[0].replace('_', ' ').title()
            slide = CompSlide()
            slide.title = prepared_filename
            slide.image = file
            slide.comp = comp
            slide.name = prepared_filename
            slide.save()
            comp.save()

            log.info ('Got file: "%s"' % str(filename))
            log.info('Content type: "$s" % file.content_type')
            
            log.info('File saving done')
            #settings imports
        with transaction.commit_on_success():
            #get the current site
            admin_site = admin.site
            compAdmin = CompAdmin(Comp, admin_site)
            
            #get all possible inlines for the parent Admin
            inline_instances = compAdmin.get_inline_instances(request)
            prefixes = {}
            
            for FormSet, inline in zip(compAdmin.get_formsets(request, comp), inline_instances):
                #get the inline of interest and generate it's formset
                if isinstance(inline, CompSlideInline):
                    prefix = FormSet.get_default_prefix()
                    prefixes[prefix] = prefixes.get(prefix, 0) + 1
                    if prefixes[prefix] != 1 or not prefix:
                        prefix = "%s-%s" % (prefix, prefixes[prefix])
                    formset = FormSet(instance=comp, prefix=prefix, queryset=inline.queryset(request))
            
            #get possible fieldsets, readonly, and prepopulated information for the parent Admin
            fieldsets = list(inline.get_fieldsets(request, comp))
            readonly = list(inline.get_readonly_fields(request, comp))
            prepopulated = dict(inline.get_prepopulated_fields(request, comp))
            
            #generate the inline formset
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                        fieldsets, prepopulated, readonly, model_admin=compAdmin)

            #render the template
            t = loader.get_template('admin/staging/edit_inline/_comp_slide_drag_upload_ajax.html')
            c = Context({ 'inline_admin_formset': inline_admin_formset })
            rendered = t.render(c)
        result = []
        result.append({"name":filename, 
                       "size":file_size, 
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