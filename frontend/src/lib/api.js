// FastAPI용 라이브러리
const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    // Svelte환경에서 .env의 환경변수는 무조건 VITE_로 시작해야 함
    let _url = import.meta.env.VITE_SERVER_URL + url
    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    if (method === 'get') {
        _url += "?" + new URLSearchParams(params)
    } else {
        options['body'] = body
    }

    fetch(_url, options).then(response => {
        // No content의 경우에도 success
        if (response.status === 204) {
            if (success_callback) {
                success_callback()
            }
            return
        }
        response.json().then(json => {
            if (response.status >= 200 && response.status < 300) {
                if (success_callback) {
                    success_callback(json)
                }
            } else {
                if (failure_callback) {
                    failure_callback(json)
                } else {
                    alert(JSON.stringify(json))
                }
            }
        }).catch(error => {
            alert(JSON.stringify(error))
        })
    })
}

export default fastapi