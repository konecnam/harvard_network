function edit_status() {

    // Show compose view and hide other views
    document.querySelector('#save_div').style.display = 'none';
    document.querySelector('#read_div').style.display = 'block';
    console.log('ja jedu')
}

function likes(heart) {
    const csfr_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const liked_post_id = heart.getAttribute('data-post-id');
    const data = { post_id: liked_post_id };
    fetch("{% url 'like' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csfr_token
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(result => {
            document.querySelector(`#likes-${liked_post_id}`).innerHTML = result.count_likes;
        });

    if (heart.innerHTML === '❤️') {
        heart.innerHTML = '🖤'; // změníme na černé srdíčko
    } else {
        heart.innerHTML = '❤️'; // změníme na červené srdíčko
    }
}