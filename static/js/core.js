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