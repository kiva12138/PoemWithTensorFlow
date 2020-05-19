
jQuery(document).ready(function() {
	
    /*
        Fullscreen background
    */
    $.backstretch("/static/assets/img/backgrounds/2.jpg");
    
    $('#top-navbar-1').on('shown.bs.collapse', function(){
    	$.backstretch("resize");
    });
    $('#top-navbar-1').on('hidden.bs.collapse', function(){
    	$.backstretch("resize");
    });
    
    /*
        Form
    */
    $('.registration-form fieldset:first-child').fadeIn('slow');
    
    $('.registration-form input[type="text"], .registration-form input[type="password"], .registration-form textarea').on('focus', function() {
    	$(this).removeClass('input-error');
    });
    
    // next step
    $('.registration-form .btn-next').on('click', function() {
    	var parent_fieldset = $(this).parents('fieldset');
    	var next_step = true;
    	
    	parent_fieldset.find('input[type="text"], input[type="password"], textarea').each(function() {
    		if( $(this).val() == "" ) {
    			$(this).addClass('input-error');
    			next_step = false;
    		}
    		else {
    			$(this).removeClass('input-error');
    		}
    	});
    	
    	if( next_step ) {
    		parent_fieldset.fadeOut(400, function() {
	    		$(this).next().fadeIn();
	    	});
    	}
    	
    });
    
    // previous step
    $('.registration-form .btn-previous').on('click', function() {
    	$(this).parents('fieldset').fadeOut(400, function() {
    		$(this).prev().fadeIn();
    	});
    });

    $('#form-facebook-id').on('change', function(e) {
    	if ($(this).val() == "random") {
    	    $('#form-twitter-id').addClass('input-disabled')
    	}else{
    	    $('#form-twitter-id').removeClass('input-disabled')
    	}
    });

    function get_result(){
        if($('#form-twitter-id').val() == "" && $('#form-facebook-id').val() != "random"){
            return
        }
        $('#loading-show').addClass('current-loading')
        $.get("/write", { 'type': $('#form-facebook-id').val(), 'content': $('#form-twitter-id').val()}, function(data){
            $('#result_show').html(data)
            $('#loading-show').removeClass('current-loading')
        });
    }
    // submit
    $('.registration-form').on('submit', function(e) {
        if ($('#form-facebook-id').val() != 'random') {
             $(this).find('input[type="text"], select').each(function() {
                if( $(this).val() == "" ) {
                    $(this).addClass('input-error');
                }
                else {
                    $(this).removeClass('input-error');
                }
            });
        }
        get_result()
        e.preventDefault();
    });

    
});
