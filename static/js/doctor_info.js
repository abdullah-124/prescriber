const doctor_info_modal = document.getElementById('doctor_info_modal')
const doctor_info_form = document.getElementById('doctor_info_form')
const doctor_info = {}
const stored_doctor_info = JSON.parse(localStorage.getItem('doctor_info'))
console.log(stored_doctor_info)

window.addEventListener('DOMContentLoaded', ()=>{
    if(stored_doctor_info) initialize_form()
        // else doctor_info_modal_toggle()
})

function doctor_info_modal_toggle(){
    doctor_info_modal.classList.toggle('hidden')
}

doctor_info_form.addEventListener('submit',(e)=>{
    e.preventDefault()
    save_to_localstorage()
})
function save_to_localstorage(){
    const form = new FormData(doctor_info_form)
    form.forEach((value, key) => {
        doctor_info[key] = value
    });
    localStorage.setItem('doctor_info', JSON.stringify(doctor_info))
    location.reload()
}
function initialize_form(){
    const form = doctor_info_form.querySelectorAll('input')
    form.forEach(elm=>{
        // console.log(elm)
        elm.value = stored_doctor_info[elm.name]
    })
}