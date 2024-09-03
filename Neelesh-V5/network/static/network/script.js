document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.l-count').forEach(post => {
        fetch(`/count/${post.dataset.post}`)
            .then(response => response.json())
            .then(json => {
                post.innerHTML = json;
            })
    })

    
    document.querySelectorAll('.f-tab').forEach(tab => {

        let fed = document.getElementById('fed');
        let fing = document.getElementById('fing');
        let fbtn = document.getElementById('follow-btn');

        fetch(`/follow/${tab.dataset.id}`)
            .then(response => response.json())
            .then(json => {
                const details = json.split(',');
                console.log(details);
                if( document.getElementById('follow-btn')){
                if (details[0] == "False") {
                    fbtn.className = "btn btn-primary";
                    fbtn.setAttribute('value', "Follow");
                }
                else if (details[0] == 'True') {
                    fbtn.className = "btn btn-light";
                    fbtn.setAttribute('value', "Unfollow");
                }
            }
                fed.innerHTML = details[1];
                fing.innerHTML = details[2];
            })
        
        if( document.getElementById('follow-btn')){
        fbtn.addEventListener('click', () => {
            fetch(`/follow/${tab.dataset.id}`)
            .then(response => response.json())
            .then(json => {
                const details = json.split(',');
                let fedVal = fed.innerHTML;
                let fingVal = fing.innerHTML;
                if (details[0] == "True") {
                    fbtn.className = "btn btn-primary";
                    fbtn.setAttribute('value', "Follow");
                    fed.innerHTML = Number(fedVal) - 1;
                }
                else if (details[0] == 'False') {
                    fbtn.className = "btn btn-light";
                    fbtn.setAttribute('value', "Unfollow");
                    fed.innerHTML = Number(fedVal) + 1;
                }

                fetch(`/follow/${tab.dataset.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        follow: true ? (details[0] == "False") : (details[0] == "True")
                    })
                })
            })
        })
    }
    })
    

    document.querySelectorAll('.index-pi').forEach(btn => {
        btn.onclick = () => {
            address = window.location.search
            parameterList = new URLSearchParams(address)
            current = parameterList.get('page')

            if (current == null) {
                current = 1
            }

            val = btn.dataset.page

            if (val == "prev") {
                req = Number(current) - 1
            }
            else if (val == "next") {
                req = Number(current) + 1
                console.log(req)
            }

            fetch('?' + new URLSearchParams({
                page: req
            }))
                .then(response => response.json)
                .then(json => {
                    if ((location.href.indexOf('profile') == -1) && (location.href.indexOf('following') == -1)) {
                        location.href = `/?page=${req}`;
                    }
                    else if (location.href.indexOf('profile') == 22) {
                        var id = document.getElementById('pro-name').dataset.id;
                        location.href = `/profile/${id}?page=${req}`;
                    }
                    else if (location.href.indexOf('following') == 22){
                        location.href = `/following?page=${req}`
                    }
                })
        }
    })

    let lcount = document.querySelectorAll('.l-count');

    document.querySelectorAll('.like-btn').forEach(btn => {
        for (let count of lcount) {
            if (count.dataset.post == btn.dataset.post) {
                var cnt = count;
                break;
            }
        }

        fetch(`/like/${btn.dataset.post}`)
            .then(response => response.json())
            .then(json => {
                if (json == "True") {
                    btn.className = "like-btn fa-solid fa-heart fa-lg"
                }
                else if (json == 'False') {
                    btn.className = 'like-btn fa-regular fa-heart fa-lg'
                }
            })

        btn.addEventListener('click', () => {
            fetch(`/like/${btn.dataset.post}`)
                .then(response => response.json())
                .then(json => {
                    let val = cnt.innerHTML;
                    if (json == "True") {
                        btn.className = "like-btn fa-regular fa-heart fa-lg";
                        cnt.innerHTML = Number(val) - 1;
                    }
                    else if (json == 'False') {
                        btn.className = 'like-btn fa-solid fa-heart fa-lg';
                        cnt.innerHTML = Number(val) + 1;
                    }

                    fetch(`/like/${btn.dataset.post}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            like: true ? (json == "False") : (json == "True")
                        })
                    })
                })
        })
    })

    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            var eles = btn.parentNode.childNodes;
            for (let ele of eles){
                if(ele.className == "p-contents card-text"){
                    var contentEle = ele;
                    break;
                }
                if(ele.className == 'f-create'){
                    var editDiv = ele;
                    var children = editDiv.childNodes;
                    
                    for(child of children){
                        if(child.nodeName.toLowerCase() == 'textarea'){
                            var textArea = child;
                            break;
                        }
                    }
                    break;
                }
            }

                     
            if(btn.innerHTML == "Edit"){                           
                let editDiv = document.createElement('div');
                editDiv.classList.add('f-create');
                let textArea = document.createElement('textarea');
                let contents = contentEle.innerHTML;
                let saveBtn = document.createElement('btn');
                saveBtn.className = "btn btn-primary";
                saveBtn.innerHTML = 'Save'; 



                editDiv.appendChild(textArea);
                editDiv.appendChild(saveBtn);
                editDiv.style.margin = '10px';
                contentEle.replaceWith(editDiv);
                btn.innerHTML = "Cancel";
                textArea.setAttribute('value', contents);
                textArea.innerHTML = contents;

                saveBtn.addEventListener('click', () => {
                    let id = saveBtn.parentNode.parentNode.parentNode.dataset.post;
                    fetch(`/edit/${id}`, {
                        method: 'PUT',
                        body : JSON.stringify({
                            contents : textArea.value
                        })
                    })
                    .then(response => response.json())
                    .then(json => {
                        const result = JSON.parse(json);
                        console.log(result);

                        let post = result[0].fields;

                        let para = document.createElement('p');
                        para.className = 'p-contents card-text';
                        para.innerHTML = post.contents;
                        editDiv.replaceWith(para);
                        btn.innerHTML = "Edit";
                    })
                    
                })
            }
            else if(btn.innerHTML == "Cancel"){
                let para = document.createElement('p');
                para.className = 'p-contents card-text';
                para.innerHTML = textArea.value;
                editDiv.replaceWith(para);
                btn.innerHTML = "Edit";
            }
            // 
        })
    })
})