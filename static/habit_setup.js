"use strict";

function showHabitForms(evt) {
    // let numberOfForms = Number($('#new_habits').html());
    //show form numberOfForms times
    let numberOfForms = $('#new_habits').val();
    // make an Ajax request to the server to get the habit detail form.
    $.get('/someroute', (data) => {
        let habitDetailForm = data; // partial HTML
        // select the div with the id foo
        // empty that div
        // create a new form element and attach it to the foo div. Give it an id.
        // loop numberOfForms times
        // each time through the loop, attach habitDetailForm as a child of the new form.
        // attach a submit button to the VERY BOTTOM of the form
        // create an event listener for the form. 
            // when the form is submitted, make an ajax request to the server at some route
            // send along the form data
           
    });
}

$('#new_habits').on('submit', () =>{
    showHabitForms();

})