const apply_buttons = $('.js-apply-reply')

apply_buttons.each(function() {
    $(this).on("click", ()=>{
        $.ajax({url: '/ajax/replies/' + $(this)[0].value + '/apply',
            method: 'post',
            dataType: 'json',

            success: function (data) {
                alert('Заявка одобрена')
            },

            error: function (data) {
                alert(`${data.responseJSON["message"]}`)
            }
        })
    })
})