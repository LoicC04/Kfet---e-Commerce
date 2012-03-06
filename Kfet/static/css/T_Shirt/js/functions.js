$(function() {
	$('.field, textarea').focus(function() {
        if(this.title==this.value) {
            this.value = '';
        }
    }).blur(function(){
        if(this.value=='') {
            this.value = this.title;
        }
    });
    
	$('#slider ul.slider-items').jcarousel({
		'speed': 'slow',
		'scroll': 1,
		'auto': 4,
		'wrap': 'both',
        initCallback: mycarousel_initCallback,
        buttonNextHTML: null,
        buttonPrevHTML: null,
        itemVisibleInCallback: {
			onAfterAnimation: function(c, o, i, s) {
				jQuery('.slider-controls li').removeClass('active');
				jQuery('.slider-controls li:eq('+ (i-1) +')').addClass('active');
			}
		}
	});
	
	$('#pr-slider').jcarousel({
		'speed': 'slow',
		'scroll': 1,
		'auto': 3,
		'wrap': 'both'
	});
	
	if ($.browser.msie && $.browser.version == 6) {
		DD_belatedPNG.fix('.inner, #wrapper, h1#logo a, #header, .header-inner, a.view-account, .widget h2, .search-button , .search-button input, .search-options li a, #navigation li a, #navigation li a span, .slider-frame, .pr-info, .pr-price, .jcarousel-prev, .jcarousel-next, p.more a, #footer, .box-title img, .box-title h4, #sidebar');
	}
	
});

function mycarousel_initCallback(carousel) {
    var i = 1;
    $('.slider-items li').each(function(){
    	$('.slider-controls ul').append('<li><a href="#">' + i + '</a></li>');
    	i++;
    });
    $('.slider-controls a').bind('click', function() {
        carousel.scroll(jQuery.jcarousel.intval(jQuery(this).text()));
        return false;
    });
	$('.slider-controls').css('margin-left', function(){
		return -($(this).find('ul').width() / 2 + 7) + 'px';
	});
};