// basic modification
const contentEditable_fields = document.querySelectorAll('.content_editable')
const doctor = JSON.parse(localStorage.getItem("doctor_info"));
// console.log(doctor);
// Helper: Move caret to end
function placeCaretAtEnd(el) {
    const range = document.createRange();
    const sel = window.getSelection();
    range.selectNodeContents(el);
    range.collapse(false);
    sel.removeAllRanges();
    sel.addRange(range);
}
contentEditable_fields.forEach(input => {
    input.contentEditable = true;
    input.classList.add('click_to_edit')
    input.addEventListener('focus', () => {
        input.classList.remove('click_to_edit')
        if (input.innerHTML.trim() === '') {
            input.innerHTML = '\u200B'
            placeCaretAtEnd(input);
        }
    })
    // input.setAttribute('placeholder', `Type ${input.innerText}`)
    const attr = input.getAttribute('name')
    if (attr && doctor) {
        input.innerText = doctor[attr]
    }
})
// zoom and zoom-out 
// 
const zoom_label_input = document.getElementById('zoom_label_input')
const zoom_label_indicator = document.getElementById('zoom_label_indicator')
zoom_label_input.addEventListener('input',()=>{
    const prescription = document.getElementById('demo_prescription_wrapper')
    let val = zoom_label_input.value
    zoom_label_indicator.innerText = val
    prescription.style.transform = `scale(${val}%)`
})
// drugs and other operation

let drugs_input = document.getElementById('drugs')
const results_box = document.getElementById('search-results')
const expanded_field = document.getElementById('expanded_field')
const expand_btn = document.getElementById('expand_btn')
let form = document.getElementById('medicine_form')
let inputs = document.querySelectorAll('#medicine_form input')
let medicines = [];
let timeout;
function update_data() {
    medicine_container = document.getElementById('medicine_container');
    medicine_container.innerHTML = '';
    medicines.forEach((m, index) => {
        medicine_container.innerHTML += `
            <tr class=" border-b border-[#ccc]">
                <td class="text-start">${index + 1}. ${m.drugs}</td>
                <td class="text-sm py-2">${m.frequency} <br> ${m.timing}</td>
                <td>${m.instruction}</td>
                <td class="hide_on_print text-xs text-end">
                <a onclick="action_modal(${index},'update')" class="hover:bg-indigo-600 bg-indigo-500 p-1 px-2 rounded text-white"><i class="fa-solid fa-pencil"></i></a>
                <a onclick="action_modal(${index},'delete')" class="hover:bg-red-600 bg-red-500 p-1 px-2 rounded text-white"><i class="fa-solid fa-trash"></i></a>
                </td> 
            </tr>
        `
    });
}
drugs_input.addEventListener('input', (e) => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
        let q = e.target.value
        if (q.length > 2) {
            search(q)
        }
        else {
            results_box.classList.add('hidden')
        }
    }, 800);
})
async function search(q) {
    const url = `/drugs/search/?q=${encodeURIComponent(q)}`
    console.log(url)
    const res = await fetch(url);
    const data = await res.json()
    console.log(data)
    show_data(data)
}
function show_data(data) {
    results_box.classList.remove('hidden')
    results_box.innerHTML = ""
    data.map(m => {
        results_box.innerHTML += `
            <li class="text-xs p-2 hover:bg-gray-200" onclick="set_medicine('${m.name}','${m.dosage}')">
                <p class="font-semibold">${m.name} <span class="font-normal text-[10px]">${m.dosage} (${m.use_for})</span></p>   
                <p>${m.generic}(${m.strength})</p> 
                <p>${m.manufacturer}</p> 
            </li>
            `
    })
}
function set_medicine(name, dosage) {
    drugs_input.value = `${dosage}. ${name}`
    results_box.innerHTML = ""
    results_box.classList.add('hidden')
    expand_form()
}
function expand_form() {
    expanded_field.classList.replace('hidden', 'inline-flex')
    expand_btn.classList.add('hidden')
    drugs_input.classList.replace('w-full', 'w-1/2')
}

// MEDICINES OPERATION: 
// add 
form.addEventListener('submit', (e) => {
    e.preventDefault()
    if (!e.target.checkValidity()) {
        e.target.reportValidity(); // show built-in validation
        return false;
    }
    const medicine = {}
    inputs.forEach(i => {
        medicine[i.name] = i.value;
    })
    medicine.status = 'add'
    medicines.push(medicine)
    console.log(medicines)
    form.reset()

    document.getElementById('medicine_form_parent').classList.add('hidden')
    expanded_field.classList.replace('inline-flex', 'hidden')
    drugs_input.classList.replace('w-1/2', 'w-full')
    expand_btn.classList.remove('hidden')

    update_data()
})
// update and delete
const action_modal_div = document.getElementById('action_modal_div')
const show_update = document.getElementById('show_update')
const show_delete = document.getElementById('show_delete')
const drugs = document.getElementById('drugs_field')
const frequency = document.getElementById('frequency_field')
const timing = document.getElementById('timing_field')
const instruction = document.getElementById('instruction_field')
function action_modal(idx, status) {
    action_modal_div.classList.toggle('hidden')
    if (status == 'update') {
        show_update.innerHTML = `
       <form id="medicine_update_form" class="py-2">
       <h1 class="text-lg text-indigo-500 font-bold border-b border-gray-200 pb-1 mb-2">Update</h1>
                <input value='${medicines[idx]['drugs']}' class="input" type="text" name="drugs" placeholder="Enter Drugs name">
                <input value='${medicines[idx]['frequency']}' class="input" type="text" name="frequency" placeholder="Frequency (1+0+1)">
                <input value='${medicines[idx]['timing']}' class="input" type="text" name="timing" placeholder="Timing">
                <input value='${medicines[idx]['instruction']}' class="input" type="text" name="instruction" placeholder="Instruction">
                <div class="flex justify-between my-5">
                    <a 
                        onclick="update_medicine(${idx})"
                        class=" font-medium px-2 bg-indigo-500 hover:bg-indigo-600 border text-white p-1 rounded">Update</a>
                    <a
                    onclick="action_modal_div.classList.toggle('hidden')"
                        class=" font-medium px-2 border border-red-500 text-red-500 hover:bg-red-600 hover:text-white p-1 rounded">Close</a>
                </div>
            </form>
       `
        show_update.classList.remove('hidden')
        show_delete.classList.add('hidden')

    }
    else {
        show_delete.innerHTML = `
            <div>
                <h1 class="text-center text-xl text-red-500 font-bold">Are you sure you want to delete?</h1>
                <div class="flex justify-center my-5">
                    <a onclick="delete_medicine(${idx})"
                        class="me-5 font-medium px-2 bg-red-500 hover:bg-red-600 border text-white p-1 rounded">Delete</a>
                    <a onclick="action_modal_div.classList.toggle('hidden')"
                        class="ms-5 font-medium px-2 border border-red-500 text-red-500 hover:bg-red-600 hover:text-white p-1 rounded">Close</a>
                </div>
            </div>
        `
        show_update.classList.add('hidden')
        show_delete.classList.remove('hidden')
    }
}
function update_medicine(idx) {
    const medicine_update_form = document.getElementById('medicine_update_form')
    const form_data = new FormData(medicine_update_form)
    const new_medicine = medicines[idx]
    console.log(new_medicine)
    for (let [key, value] of form_data.entries()) {
        new_medicine[key] = value;
    }
    console.log(new_medicine)
    medicines[idx] = new_medicine
    // console.log(medicines)
    update_data()
    action_modal_div.classList.toggle('hidden')
}


function delete_medicine(idx) {
    // console.log('i am form delete', idx)

    medicines.splice(idx, 1)
    update_data()
    console.log(medicines)
    action_modal_div.classList.toggle('hidden')
}

// prescription download and format
const prescription_wrapper = document.getElementById('demo_prescription_wrapper')
function print_prescription() {
    const originalContents = document.body.innerHTML;
    document.body.innerHTML = prescription_wrapper.innerHTML;
    window.print();
    document.body.innerHTML = originalContents;
    location.reload();
}
function downloadAsImage() {
    document.querySelectorAll('.hide_on_print').forEach(a => {
        a.classList.add('hidden')
    })
    const patient_name = document.getElementById('patient_name').innerText
    html2canvas(prescription_wrapper, {
        width: prescription_wrapper.offsetWidth,
        height: prescription_wrapper.offsetHeight,
        scale: 2,
        backgroundColor: null,
    }).then(canvas => {
        const link = document.createElement('a');
        link.download = `${patient_name}_prescription.png`;
        link.href = canvas.toDataURL();
        link.click();
    });
    document.querySelectorAll('.hide_on_print').forEach(a => {
        a.classList.remove('hidden')
    })
}