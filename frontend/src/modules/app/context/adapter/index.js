import { get, post } from "modules/app/xhr";

export function getUser() {
    return get("/api/intervals/current_user/");
}

export function logout() {
    console.log("Logged out");
    return post("/api/intervals/logout/");
};
