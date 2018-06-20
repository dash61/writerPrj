
// Helper function to get the body height right.
function htmlbodyHeightUpdate() {
    let win_H = $( window ).height();
    let nav_H = $('.nav').outerHeight()+50;
    let mainC_H = $('#main_container').outerHeight();
    let top_H = $('body > h1').outerHeight();
    let footer_H = $('#footer-div').outerHeight();
    let total_H = top_H + mainC_H + footer_H;
    $('html').height(total_H);
    $('body').height(total_H);

}

// Ye old document ready function.
$(document).ready(function () {
    $( window ).scroll(function() {
        height2 = $('#main_container').height()
    });


    // Grab the current href value from the address bar.
    let currentPath = location.pathname;
    let hrefStoredStr = sessionStorage.getItem("href");
    var prevhRef = $('.active').attr('href'); // find *any* active class

    // Find the anchor w/ href matching the current page.
    let objNewLink = $('li').find("[href='" + currentPath + "']");

    // If this is a first time page load, we'll have no stored href,
    // so just add the active class to the home page (ie, href='/').
    // Sometimes the old and new hrefs both = '/' on 1st load (like try going
    // to admin page first, then click 'view site'); in this case we still
    // need to set the active class, hence the check for prevhRef.
    if (!hrefStoredStr || hrefStoredStr == undefined || prevhRef == undefined)
    {
        hrefStoredStr = '/';
        objNewLink.parent().addClass('active');
    }
    else
    {
        // Find the anchor w/ href matching what we stored in session storage.
        let objOldLink = $('li').find("[href='" + hrefStoredStr + "']");

        // If the current href doesn't match the stored href, we changed pages.
        if (currentPath != hrefStoredStr)
        {
            //console.log ("We clicked a different link: old=" + hrefStoredStr + ", new=" + currentPath);
            objOldLink.siblings().removeClass('active'); // remove all old active classes
            objNewLink.parent().addClass('active');      // add active class to current page
        }
    }

    // From greensock's home page, footer.js. This makes the opacity
    // ramp from 1 to 0 or 0 to 1 over time. Used on the social icons
    // to swap between the dark icon and the lighter one and back again
    // as you move your mouse over them.
    $(".social-icons .social").hover(
        function() {
            TweenMax.to($(this).find('img'), 0.25, {autoAlpha:0});
            TweenMax.to($(this).find('.hover'), 0.25, {autoAlpha:1});
            TweenMax.to($(this).find('p'), 0.25, {color:'#4B96FF'}); // bright blue
        }, function() {
            TweenMax.to($(this).find('img'), 0.6, {autoAlpha:1});
            TweenMax.to($(this).find('.hover'), 0.6, {autoAlpha:0});
            TweenMax.to($(this).find('p'), 0.6, {color:'#266CAD'}); // dark blue
        }
    );

});


// We install a click handler for all elements matching the jquery selector.
// Goal is to find the currently selected (ie, the one with the 'active class')
// list item, find it's child (an 'a' link), grab it's href, then store
// that href in sessionStorage. Note that we can't store an object in sessionStorage
// (even if stringify'ed) because when we try to use that later it just doesn't work.
$('.sidebar .nav li a').on('click', function (event) {

    var prevAnchorItem = $('.active a');        // select 'a' under ele w/ 'active' class
    var prevhRef = prevAnchorItem.attr('href'); // get its href attribute (string)
    sessionStorage.setItem("href", prevhRef);   // set href into session storage
});



