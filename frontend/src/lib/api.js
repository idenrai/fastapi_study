import qs from "qs"
import { access_token, username, is_login } from "./store"
import { get } from 'svelte/store'
import { push } from 'svelte-spa-router'

// FastAPI용 라이브러리
const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    // 로그인 API 요청시(operation = login)에는 Header값 고정
    // OAuth2의 규칙 : content_type = 'application/x-www-form-urlencoded'
    if (operation === 'login') {
        method = 'post'
        content_type = 'application/x-www-form-urlencoded'
        body = qs.stringify(params)
    }

    // Svelte환경에서 .env의 환경변수는 무조건 VITE_로 시작해야 함
    let _url = import.meta.env.VITE_SERVER_URL + url
    let options = {
        method: method,
        headers: {
            "Content-Type": content_type
        }
    }

    // Q&A 등록 API가 인증을 필요로 하므로, Header에 Token을 함께 보내야 함
    const _access_token = get(access_token)
    if (_access_token) {
        options.headers["Authorization"] = "Bearer " + _access_token
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
            console.log(json)

            if (response.status >= 200 && response.status < 300) {
                if (success_callback) {
                    success_callback(json)
                }
            } else if (operation !== 'login' && response.status === 401) {
                // Token time out
                // Operation이 login이 아닌데 401에러가 발생하는 경우 = 로그인이 필요한 상황 (Question, Answer)
                access_token.set('')
                username.set('')
                is_login.set(false)
                alert("로그인이 필요합니다.")
                push('/user-login')
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