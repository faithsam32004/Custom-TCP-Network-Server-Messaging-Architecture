function chatLogic(){

    const message=document.getElementById('messageBox')
    const button=document.getElementById('send_button')
    
    finalized_token=localStorage.getItem('token')
    const socket=new WebSocket(`ws://localhost:8000?token=${finalized_token}`)

    button.addEventListener("click", function(){

        if(message.value.trim().length === 0){
            message.value=""
            return
        }
        else{
            socket.send(message.value)

            const container=document.getElementById('inbox')

            const sendMessage=document.createElement('div')
            sendMessage.className='sMessage'
            sendMessage.textContent=message.value

            message.value=""

            container.prepend(sendMessage)
        }
    })



    socket.onmessage=(event)=>{
        // const inbox=document.getElementById('inbox')
        // inbox.innerHTML+=event.data
        const container=document.getElementById('inbox')

        const newMessage=document.createElement('div')
        newMessage.className='newMessage'
        newMessage.textContent=event.data

        container.prepend(newMessage)
    }



}


window.onload=chatLogic()


