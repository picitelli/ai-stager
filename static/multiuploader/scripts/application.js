/*
 * jQuery File Upload Plugin JS Example 5.0.2
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://creativecommons.org/licenses/MIT/
 */

/*jslint nomen: true */
/*global $ */

$(function () {
    'use strict';
    var $tempAjax = $('<div id="tempAjax" style="visibility:hidden"><div>'),
    	$inline = $('#ajax_inline_slides_group');
    $('body').append($tempAjax);
    console.log($inline);
    // Initialize the jQuery File Upload widget:
    $('#fileupload')
    	.fileupload({'url': '/multi/', 'formData': {'compId': $('#id_slides-__prefix__-comp').val() } })
    	.bind('fileuploaddone', function (e, data) {
    		$tempAjax.html(data.result[0].html);
    	})
    	.bind('fileuploadstart', function (e) {
    		$inline.fadeTo('slow', 0.25);
    	})
    	.bind('fileuploadstop', function (e) {
    		$inline.fadeTo('slow', 0, function() {
    			var $sib = $inline.find('.grp-module grp-tbody:last');
    			$sib.prev().remove();
    			$sib.prev().remove();
    			$sib.remove();
    			$inline.html($tempAjax.html());
    			rebindSorter();
    			$inline.fadeTo('slow', 1);
    		});
    		//window.location = window.location;
    	})
    	;

 
    // Load existing files:
    //console.log($('#fileupload').data('action'));
   /* $.getJSON($('#fileupload').data('action'), function (files) {
        var fu = $('#fileupload').data('fileupload');
        fu._adjustMaxNumberOfFiles(-files.length);
        fu._renderDownload(files)
            .appendTo($('#fileupload .files'))
            .fadeIn(function () {
                // Fix for IE7 and lower:
                $(this).show();
            });
    });*/

    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
    	console.log('click');
    	console.log($(this));
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });

});