"use strict";

let messages;
let messagesText;
let nRows;

function createPagination() {
    let pagination = $(".pagination"); 
    let html = '';
    let previousPageNumber = currentPageNumber - 1;
    let nextPageNumber = currentPageNumber + 1;
    let searchText = '&search=' + searchWord;

    if (previousPageNumber >= 1) {
        let prevousHTML = '<a class="pagination__link" href="?page=' + previousPageNumber;

        html += prevousHTML;
        if (searchWord) {
            html += searchText;
        }
        html += '">&lsaquo;</a>';
        html += prevousHTML;
        if (searchWord) {
            html += searchText;
        }
        html += '">' + previousPageNumber + '</a>';
    }

    html += '<span class="pagination__link pagination__link_active">' + currentPageNumber + '</span>';

    if (nextPageNumber <= totalPages) {
        let nextHTML = '<a class="pagination__link" href="?page=' + nextPageNumber;

        html += nextHTML;
        if (searchWord) {
            html += searchText;
        }
        html += '">' + nextPageNumber + '</a>';
        html += nextHTML;
        if (searchWord) {
            html += searchText;
        }
        html += '">&rsaquo;</a>';
    }

    pagination.html(html);
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Change number of glyphs in messages on shows 
function refillMessage(i, maxSymbols, isHide=true) {
    let newMessage = messagesText[i].substring(0, maxSymbols);
    if (maxSymbols < messagesText[i].length) {
        newMessage += '...';
    }

    $(messages[i]).find('p').text(newMessage);
}

function showMessages() {
    let nColumns = Math.floor(parseInt($(messages[0]).css('width'))) / (parseInt($(messages[0]).css('font-size')) / 1.6);

    for (i = 0; i < messages.length; ++i) {
        showMessage($(messages[i]).next(), nColumns, i, true);
    }
}

// Animate show button
function showMessage(self, nColumns, i, isInit=false) {
    let messageContent = $(self).find('strong');
    let message = $(messages[i]);
    let maxSymbols;

    if (messageContent.text() == 'show full' && !isInit) {
        maxSymbols = messagesText[i].length;
        message.css('height', '100%');
        messageContent.text('hide full');
    } else {
        maxSymbols = nRows * nColumns;
        message.css('height', '150px');
        messageContent.text('show full');

        if (maxSymbols < messagesText[i].length) {
            message.next().show();
        } else {
            message.next().hide();
        }
    }

    refillMessage(i, maxSymbols);
}

$(document).ready(function () {
    messages = $('.blog-form__message');
    messagesText = [];
    nRows = Math.floor(parseInt($(messages[0]).css('height')) / parseInt($(messages[0]).css('font-size')));
    let nColumns = Math.floor(parseInt($(messages[0]).css('width'))) / (parseInt($(messages[0]).css('font-size')) / 1.6);
    
    // Refill text and show message initialize
    Array.prototype.forEach.call(messages, message => {
        let nMessage = messagesText.length;
        
        messagesText.push($(message).find('p').text());
        showMessage(message, nColumns, nMessage, true);

        $(message).next().on('click', function(e){
            showMessage(this, nColumns, nMessage);
            e.preventDefault();
        });
    });     

    createPagination();
    $(window).on('resize', function () {
        showMessages();
    });
    $('#search').on('change', function(){
        $(this).text(escapeHtml($(this).text));
    });
});