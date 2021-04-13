import { post } from "modules/app/xhr";

export function signup(username, password) {
    const data = {username: username, password: password};
    return post("/api/intervals/users/", data);
}
