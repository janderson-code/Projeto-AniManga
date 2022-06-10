window.onload = () => {
    createProgressBar()
    const btnAutoComplete = document.getElementById("id_auto_complete")
    document.querySelector("#div_id_auto_complete > div > i").onclick = autoComplete
    btnAutoComplete.addEventListener("click",autoComplete)
    btnAutoComplete.disabled = true
    btnAutoComplete.parentElement.classList.add("disabled")
    const kitsuInput  = document.getElementById('id_kitsu_link')
    document.getElementById('id_kitsu_link').oninput = (_) => {
        if(kitsuInput.value){
            btnAutoComplete.disabled = false
            btnAutoComplete.parentElement.classList.remove("disabled")
        }else{
            btnAutoComplete.disabled = true
            btnAutoComplete.parentElement.classList.add("disabled")
        }
    }
}



function createProgressBar(){
    const loadHtml = 
    `
    <div class="progress">
        <div class="indeterminate"></div>
    </div>
    `
    const div = document.createElement("div")
    div.innerHTML = loadHtml;
    document.querySelector("#div_id_auto_complete > div > i").parentElement.appendChild(div);
    hideProgressBar()
}
function hideProgressBar(hide=true) {
    const progressBar = document.querySelector(".progress")
    if(hide){
        progressBar.style.display = "none"
    }else{
        progressBar.style.display = ""
    }
}
function autoComplete(){

    const onsuccess = (response) => {
        const kitsuResponse = JSON.parse(response)
        const manga = {}
        const getAnimangaStatus = (responseStatus) => {
        
            /*
              Animanga Status - Mangas
                0: 'Em andamento',
                1: 'Finalizado',
                2: 'Não lançado',
                3: 'Cancelado',
                4: 'Pausado',
                5: 'Desconhecido'
            */
            const animangaStatus = Array.from(document.querySelectorAll('#id_status option')
            ).map((option,index) => {return {index,value: option.value}})
            const kitsuStatus = {
                "current": animangaStatus[0],
                "finished": animangaStatus[1],
                "unreleased": animangaStatus[2],
                "upcoming": animangaStatus[2],
                "tba": animangaStatus[2]
            }
            console.log(animangaStatus)
            console.log(responseStatus)
            console.log()
            if(!Object.keys(kitsuStatus).includes(responseStatus)){
                return animangaStatus[5]
            }
            return kitsuStatus[responseStatus]
        }
        const getAnimangaSubtypes = (responseSubtype) => {
        
            /*
              Animanga Subtypes - Mangas
                0: 'Manga',
                1: 'One-shot',
            */
            const animangaStatus =  Array.from(document.querySelectorAll('#id_subtype option')
            ).map((option,index) => {return {index,value: option.value}})
            const kitsuStatus = {
                "doujin": animangaStatus[0],
                "manga": animangaStatus[0],
                "manhua": animangaStatus[0],
                "novel": animangaStatus[0],
                "oel": animangaStatus[0],
                "oneshot": animangaStatus[1],
            }
            if(!Object.keys(kitsuStatus).includes(responseSubtype)){
                return animangaStatus[0]
            }
            return kitsuStatus[responseSubtype]
        }
        const setOptionByValue = (id,value) => {
            document.querySelectorAll(`${id} option`).forEach(option => {
                if(option.value === value){
                    option.selected = true
                }
            })
        }
        const setValueById = (value,id) => {document.getElementById(id).value = value}
        setValueById(kitsuResponse.name, "id_title")
        setValueById(kitsuResponse.synopsis, "id_description")
        setValueById(kitsuResponse.author, "id_author")
        setValueById(kitsuResponse.startDate, "id_release_date")
        setValueById(kitsuResponse.chapterCount ? kitsuResponse.chapterCount : 0, "id_total_chapters")
        setValueById(kitsuResponse.subtype, "id_subtype")
        setValueById(kitsuResponse.kitsuPage, "id_kitsu_link")
        setValueById(kitsuResponse.posterImage, "id_official_thumbnail")
        let status = getAnimangaStatus(kitsuResponse.status)
        setOptionByValue('#id_status',status.value)
        let subtype = getAnimangaSubtypes(kitsuResponse.subtype)
        setOptionByValue('#id_subtype',subtype.value)

        hideProgressBar(true)
    }

    const autoCompleteUrl = document.getElementById("id_auto_complete_url").value

    const kitsuInput = document.getElementById('id_kitsu_link')
    let kitsuValue = kitsuInput.value
    if(!kitsuValue || document.querySelector(".progress").style.display != "none") return

    const cookie = document.cookie
    const csrfToken = cookie.substring(cookie.indexOf('=') + 1)
    const btnAutoComplete = document.getElementById("id_auto_complete")
    btnAutoComplete.disabled = true
    kitsuInput.disabled = true
    hideProgressBar(false)

    $.ajax({
        url: autoCompleteUrl,
        type: "POST",
        data: JSON.stringify({kitsuLink:kitsuValue}),
        contentType: 'application/json; charset=utf-8',
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: (response) => {
            onsuccess(response)
            btnAutoComplete.disabled = false
            kitsuInput.disabled = false
        },
        error: (response) => {
            alert("Error: " + response.responseText)
            hideProgressBar(true)
        }
     });
}