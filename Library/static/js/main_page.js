/*Display alert*/
export function showAlert(message, type) {
    const alertDiv = $('<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">'
        + message + '</div>');

    $('#alertContainer').append(alertDiv);

    alertDiv.css('opacity', 1);

    /*Set new alert relative to last one ( if existing )*/
    if ($('.alert').length > 1) {
        const lastAlert = $('.alert').eq(-2);
        const lastAlertTop = parseInt(lastAlert.css('top'));
        alertDiv.css('top', (lastAlertTop) + 'px');
    }

    /*Delay of hiding alert*/
    setTimeout(function() {
        alertDiv.css('opacity', 0);
        alertDiv.alert('close');
    }, 3000);
}

/*Handle if exist communicates to display which directed by flash function*/
$(document).ready(function() {
    const displayMessage = $('#alertContainer').attr('data-display');

    if (displayMessage !== '' && displayMessage !== null) {
        showAlert(displayMessage, 'success');
    }
});
