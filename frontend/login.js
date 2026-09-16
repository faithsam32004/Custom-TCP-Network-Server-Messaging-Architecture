

async function log(){

    const username = document.getElementById("username").value
    const password = document.getElementById("password").value
    const indicator= document.getElementById("indicator")

    indicator.innerText=""

    if (username.trim().length === 0 || password.trim().length === 0){
        indicator.innerText="Please fill both username and password."
    }

    else{

        localStorage.setItem('name', username)

        body={
                'username':username,
                'password':password,
            }



        data=await fetch("/login", {method:'POST',
            headers:{
                'content-type': "application/json",
            },
            body:JSON.stringify(body)
        })

        if (data.status==200){

            usable_data= await data.json()

            //revised_data=JSON.parse(usable_data) i commented this line because the line above and this line does the same thing which is parsing.

            usable_token= usable_data.token

            localStorage.setItem('token', usable_token)

            window.location.href="/chatlogic"
        }
        else{
            indicator.innerText="Invalid Credentials. Please check you username and Password."
        }
    }

}

const buton=document.getElementById('buton')
buton.addEventListener('click', log)