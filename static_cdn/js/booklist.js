/**
 * booklist.js v1.0.0, taken from bookshelf.js v1.0.0, and modified by drl on 10/17/2017
 * Originally from:
 * http://www.codrops.com
 *
 * Licensed under the MIT license.
 * http://www.opensource.org/licenses/mit-license.php
 * 
 * Copyright 2014, Codrops
 * http://www.codrops.com
 */
(function() {

    var scrollWrap = document.getElementById( 'scroll-wrap' ),
        docscroll = 0,
        books = document.querySelectorAll( '#bookshelf > .book-tile' );

    function scrollY() {
        return window.pageYOffset || window.document.documentElement.scrollTop;
    }

    function Book( el ) {
        this.el = el;
        this.book = this.el.querySelector( '.book' );
        this.ctrls = this.el.querySelector( '.buttons' );
        this.details = this.el.querySelector( '.details' );
        // create the necessary structure for the books to rotate in 3d
        this._layout();
        this._initEvents();
    }

    Book.prototype._layout = function() {
        this.closeDetailsCtrl = document.createElement( 'span' )
        this.closeDetailsCtrl.className = 'close-details';
        this.details.appendChild( this.closeDetailsCtrl );
    }

    Book.prototype._initEvents = function() {
        var self = this;
        if( !this.ctrls ) return;

        this.ctrls.querySelector( 'a' ).addEventListener( 'click', function( ev ) { ev.preventDefault(); self._showDetails(); } );
        this.closeDetailsCtrl.addEventListener( 'click', function() { self._hideDetails(); } );
    }

    Book.prototype._open = function() {
        docscroll = scrollY();
        classie.add( this.el, 'open' );
    }

    Book.prototype._close = function() {
        classie.remove( scrollWrap, 'hide-overflow' );
        setTimeout( function() { document.body.scrollTop = document.documentElement.scrollTop = docscroll; }, 25 );
        classie.remove( this.el, 'open' );
        classie.add( this.el, 'close' );
    }

    Book.prototype._showDetails = function() {
        classie.remove( this.el, 'details-close' );
        classie.add( this.el, 'details-open' );
    }

    Book.prototype._hideDetails = function() {
        classie.remove( this.el, 'details-open' );
        classie.add( this.el, 'details-close' );
    }

    function init() {
        [].slice.call( books ).forEach( function( el ) {
            new Book( el );
        } );
    }

    init();

})();

