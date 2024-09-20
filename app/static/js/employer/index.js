const employee_search_form = $('.js-employee-search')
const employee_results = $('.js-employee-results')
let subscribe_button
if(subscribed){
    subscribe_button = $('.js-unsubscribe')
}else{
    subscribe_button = $('.js-subscribe')
}

function subscribe(){
    $.ajax({
    url: '/ajax/employer/' + employer_id + '/subscribe/' + user_id,
        method: 'post',
        dataType: 'json',

        success: function (data) {
        },

        error: function (data) {
            alert(`${data.responseJSON["message"]}`)
        }
    }).always(()=>{
        subscribe_button.unbind("click")
        subscribe_button.text('Отписаться')
        subscribe_button.on("click", unsubscribe)
        subscribe_button.removeClass("btn-danger").addClass("btn-secondary")
    });
}
function unsubscribe(){
    $.ajax({
    url: '/ajax/employer/' + employer_id + '/unsubscribe/' + user_id,
        method: 'post',
        dataType: 'json',

        success: function (data) {
        },

        error: function (data) {
            alert(`${data.responseJSON["message"]}`)
        }
    }).always(() => {
        subscribe_button.unbind("click")
        subscribe_button.text('Подписаться')
        subscribe_button.on("click", subscribe)
        subscribe_button.removeClass("btn-secondary").addClass("btn-danger")
    });
}

function serializeForm(formNode) {
    const { elements } = formNode

    const data = new FormData()

    Array.from(elements)
        .filter((item) => !!item.name)
        .forEach((element) => {
            const { name, type } = element
            const value = type === 'checkbox'
            ? element.checked
            : element.value

    data.append(name, value)
    })

    return data
}

function search_employees(event){
    event.preventDefault()
    const data_send = serializeForm(employee_search_form[0])
    $.ajax({
    url: '/ajax/users/get_by_name/' + data_send["username"],
        method: 'post',
        dataType: 'json',

        success: function (data) {
            $(".js-employee-result").detach()
            for(const user of data["users"]){
                const button = $('<button type="button" class="btn-outline-success">✔</button>').on("click", ()=>{
                    $.ajax({
                        url: '/ajax/employer/' + employer_id + '/add_user/' + user["id"],
                            method: 'post',
                            dataType: 'json',

                            success: function (data) {
                                alert("Успешно добавлен")
                            },

                            error: function (data) {
                                alert(`${data.responseJSON["message"]}`)
                            }
                        })
                })
                const candidate_name = $(`<div class="form-control w-75">${user["name"]}</div>`)
                const res = $('<div class="d-inline-flex w-100 justify-content-around mb-1 js-employee-result">').append(candidate_name).append(button)
                employee_results.append(res)
            }
        },

        error: function (data) {
            alert(`${data.responseJSON["message"]}`)
        }
    })
}

if(subscribed){
    subscribe_button.on("click", unsubscribe)
}else{
    subscribe_button.on("click", subscribe)
}
employee_search_form.on('submit', search_employees)
