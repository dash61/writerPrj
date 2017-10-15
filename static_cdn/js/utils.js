
function htmlbodyHeightUpdate(){
    let win_H = $( window ).height();
    let nav_H = $('.nav').outerHeight()+50; // orig: +50
    let mainC_H = $('#main_container').outerHeight();
    let top_H = $('body > h1').outerHeight();
    let footer_H = $('#footer-div').outerHeight();
    console.log ("win H=" + win_H + ", ftr H=" + footer_H + ", mainC H=" + mainC_H + ", topH=" + top_H);
    let total_H = top_H + mainC_H + footer_H;
    $('html').height(total_H);
    $('body').height(total_H);

    // if(mainC_H > win_H){
    //     $('html').height(Math.max(nav_H,win_H,mainC_H)-0); // orig: +10 for both
    //     $('body').height(Math.max(nav_H,win_H,mainC_H)-0);
    // }
    // else
    // {
    //     $('html').height(Math.max(nav_H,win_H,mainC_H)); // orig: nothing added or subed
    //     $('body').height(Math.max(nav_H,win_H,mainC_H));
    // }
    
}

// ALTERNATE ways of checking for the document being ready or the
// window being loaded:

// document.addEventListener('readystatechange', function()
// {
//     if (document.readyState === 'complete')
//         console.log('ready');
// }, false);

// window.addEventListener('load', function()
// {
//     console.log('window loaded');
// }, false);

// TRADITIONAL way of running code when document is ready.
$(document).ready(function () {
    //console.log("inside document ready function in utils.js")
    //htmlbodyHeightUpdate()
    $( window ).resize(function() {
        //htmlbodyHeightUpdate()
    });
    $( window ).scroll(function() {
        height2 = $('#main_container').height()
        //htmlbodyHeightUpdate()
    });


    // Grab the current href value from the address bar.
    let currentPath = location.pathname;
    let hrefStoredStr = sessionStorage.getItem("href");
    var prevhRef = $('.active').attr('href'); // find *any* active class
    //console.log ("prev active items = " + hrefStoredStr + ", prevhRef = " + prevhRef);

    // Find the anchor w/ href matching the current page.
    let objNewLink = $('li').find("[href='" + currentPath + "']");
    //console.log ("links: old=" + hrefStoredStr + ", new=" + currentPath);

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

// Original function. Works if hrefs DON'T take you to a new page.
// But if you go to a new page, it resets the html to what it was in the file,
// not to what you changed it to here. In other words, changes to the DOM here
// get lost if you navigate away.
// $(function () {
//     $('.sidebar .nav li a').click(function (e) {
//     //$('.nav.list-group li a').bind('click', function (e) {
//         //e.preventDefault();  // causes clicks to not change page, but let's next line work
//         //alert ("button clicked");
//         $(this).closest('li').addClass('active').siblings().removeClass('active');
//         //to load new content using ajax
//         //you could wish to show user, some content is loading
//         //$('#myContainer').html('<img src="loading.gif>').load(this.href);
//     };

// });


// We install a click handler for all elements matching the jquery selector.
// Goal is to find the currently selected (ie, the one with the 'active class')
// list item, find it's child (an 'a' link), grab it's href, then store
// that href in sessionStorage. Note that we can't store an object in sessionStorage
// (even if stringify'ed) because when we try to use that later it just doesn't work.
$('.sidebar .nav li a').on('click', function (event) {

    var prevAnchorItem = $('.active a');        // select 'a' under ele w/ 'active' class
    var prevhRef = prevAnchorItem.attr('href'); // get its href attribute (string)
    //console.log ("prev sel href = " + prevhRef);
    sessionStorage.setItem("href", prevhRef);   // set href into session storage
    //alert ("stop here"); // uncomment so we can see the console.log from this fn
});



