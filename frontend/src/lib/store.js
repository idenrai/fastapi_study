import { writable } from "svelte/store";

// Store를 사용하여, 변수의 값을 전역적으로 저장
// https://svelte.dev/tutorial/writable-stores

// 브라우저 새로고침 시 store가 삭제되는 현상을 막기 위해, localStorage를 이용
const persist_storage = (key, initValue) => {
    // localStorage에서 key값을 받아옴
    const storedValueStr = localStorage.getItem(key)

    // localStorage에 값이 있을 경우, 해당 값을 사용
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)

    // localStorage에 store변수 저장
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

// Pagination
export const page = persist_storage("page", 0)

// Login
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)