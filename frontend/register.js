async function register(){
    const username=document.getElementById('usernameReg').value
    const password=document.getElementById('passwordReg').value

    body={
        'username':username,
        'password':password
    }

    data= await fetch("/registration",{
        method:'POST',
        headers:{
            'content-type': 'application/json',
        },
        
        body:JSON.stringify(body)
    })

    usable_data=await data.json()

    if (data.status==200){
        window.location.href="/login"
    }

    else if(data.status==409){
        const errmsg=document.getElementById("errmsg")
        errmsg.innerHTML="Username already exists. Opt a different username please."
    }

    else{
        const errmsg=document.getElementById("errmsg")
        errmsg.innerHTML="ERROR. Please do the registration again"
    }
}

const buton=document.getElementById('butonReg')
buton.addEventListener('click', register)