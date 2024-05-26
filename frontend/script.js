function validateForm() {
    var form = document.getElementById("sentimentForm");
    var radios = form.querySelectorAll("input[type='radio']");
    var inputs = form.querySelectorAll("textarea[required]");

    // Reset all notifications
    var notifications = form.querySelectorAll(".notification");
    for (var i = 0; i < notifications.length; i++) {
        notifications[i].innerHTML = "";
    }

    var isValid = true;

    // Check if at least one radio button is checked for each question
    for (var i = 0; i < radios.length; i++) {
        var groupName = radios[i].name;
        var groupRadios = form.querySelectorAll("input[name='" + groupName + "']:checked");
        if (groupRadios.length === 0) {
            var notificationId = "notification" + groupName.substring(6); // Extract the question number from the radio button group name
            document.getElementById(notificationId).innerHTML = "This field is required.";
            isValid = false;
        }
    }

    // Check if text inputs are not empty
    // for (var i = 0; i < textInputs.length; i++) {
    //     if (textInputs[i].value.trim() === "") {
    //         var inputName = textInputs[i].name;
    //         var questionNumber = inputName.match(/\d+/)[0]; // Extract the question number from the text input name
    //         var notificationId = "notification" + questionNumber;
    //         document.getElementById(notificationId).innerHTML = "This field is required.";
    //         isValid = false;
    //     }
    // }

    inputs.forEach(function (input) {
        if (!input.value.trim()) {
            isValid = false;
            var notification = input.parentNode.querySelector(".notification");
            notification.textContent = "This field is required.";
        } else {
            var notification = input.parentNode.querySelector(".notification");
            notification.textContent = "";
        }
    });

    // Submit the form if all fields are valid
    if (isValid) {
        form.submit();
        // window.location.href = "result.php";
    }
}





//     var inputs = document.querySelectorAll("input[required]");
//     var isValid = true;

//     inputs.forEach(function(input) {
//         if (!input.value.trim()) {
//             isValid = false;
//             var notification = input.parentNode.querySelector(".notification");
//             notification.textContent = "This field is required.";
//         } else {
//             var notification = input.parentNode.querySelector(".notification");
//             notification.textContent = "";
//         }
//     });
// }