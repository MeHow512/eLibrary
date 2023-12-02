$(document).ready(function() {
    /*Listens for event if user fills all input-boxes in register form and if pesel has correct fill */
    $('#loginRegisterBox, #emailRegisterBox, #passwordRegisterBox, #peselRegisterBox').on('input', function() {
        const loginValue = $('#loginRegisterBox').val().trim();
        const emailValue = $('#emailRegisterBox').val().trim();
        const passwordValue = $('#passwordRegisterBox').val().trim();
        const peselValue = $('#peselRegisterBox').val().trim();
        const peselRegex = /^[0-9]+$/;
        let registerButtonState = true;

        if (loginValue !== '' && emailValue !== '' && passwordValue !== '' && peselValue !== '') {
            if (peselRegex.test(peselValue) && peselValue.length === 11) {
                registerButtonState = false;
            }
        }
        $('#registerButton').prop('disabled', registerButtonState);
    });
});
