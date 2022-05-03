function autoLoad(elementId) {
    document.forms[elementId].submit();
}

function rootCheck(key) {
    let password = prompt('비밀번호 입력', '***')
        if(password === key){

        } else {
            window.history.back()
        }
}

function buttonDetection(val_index, val_name, input_name, input_hidden) {
    let food = {val_index, val_name}
    document.getElementById(input_hidden).value = food.val_index;
    document.getElementById(input_name).value = food.val_name;
}
