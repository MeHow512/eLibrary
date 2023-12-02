$(document).ready(function() {
    /*Listens for event if user fills all input-boxes in login form */
    $('#emailLoginBox, #passwordLoginBox').on('input', function() {
        const emailValue = $('#emailLoginBox').val().trim();
        const passwordValue = $('#passwordLoginBox').val().trim();

        if (emailValue !== '' && passwordValue !== '') {
            $('#loginButton').prop('disabled', false);
        } else {
            $('#loginButton').prop('disabled', true);
        }
    });
});
