import { get, post, getAuthenticated } from "modules/app/xhr";

export function login(username, password) {
    const data = {username: username, password: password};
    return post("/api/intervals/login/", data);
}

export function getUser() {
    return get("/api/intervals/current_user/");
}
