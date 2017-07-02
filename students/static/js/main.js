function initJournal() {
  var indicator = $('#ajax-progress-indicator');

  $('.day-box input[type="checkbox"]').click(function(event){
    var box = $(this);
    $.ajax(box.data('url'), {
      'type': 'POST',
      'async': true,
      'dataType': 'json',
      'data': {
        'pk': box.data('student-id'),
        'date': box.data('date'),
        'present': box.is(':checked') ? '1': '',
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      },
      'beforeSend': function(xhr, settings){
        indicator.show();
      },
      'error': function(xhr, status, error){
        alert(error);
        indicator.hide();
      },
      'success': function(data, status, xhr){
        indicator.hide();
      }
    });
  });
}

function initGroupSelector(){
  // llok up select element with group and attach out even handler on field 'change event':
  $('#group-selector select').change(function(event) {
      // get value if currently selected group option:
      var group = $(this).val();

      if (group) {
        // set cookie with expiration data 1 year since now,
        // cookie creation function takes period in days:
        $.cookie('current_group', group, {'path': '/', 'expires': 365});
      } else {
        // otherwise we delete the cookie:
        $.removeCookie('current_group', {'path': '/'});
      }

      // reload a page:
      location.reload(true);

      return true;
  });
}

function initDateFields() {
  $('input.dateinput').datetimepicker({
    'format': 'YYYY-MM-DD'
  }).on('dp.hide', function(event){
    $(this).blur();
  });
}

function initEditStudentpage() {
  $('a.student-edit-form-link').click(function(event){
    var modal = $('#myModal');
    modal.modal('show');
    return false;
  });
}

$(document).ready(function(){
  initJournal();
  initGroupSelector();
  initDateFields();
  initEditStudentpage();
});
