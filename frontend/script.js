const API = "http://localhost:8000"

async function uploadFile(){

let file = document.getElementById("fileInput").files[0]

let formData = new FormData()
formData.append("file", file)

let res = await fetch(API + "/upload/upload/upload",{
method:"POST",
body:formData
})

let data = await res.json()

document.getElementById("result").innerText = JSON.stringify(data)

}


async function verifyFile(){

let id = document.getElementById("fileId").value

let res = await fetch(API + "/download/download/verify",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
file_id:id
})

})

let data = await res.json()

document.getElementById("verifyResult").innerText = JSON.stringify(data)

}