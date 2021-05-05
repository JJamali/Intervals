import { get, post, patch } from "modules/app/xhr";

export function getUserId() {
    return get("/api/intervals/current_user/");
}

export function logout() {
    console.log("Logged out");
    return post("/api/intervals/logout/");
}

export function getUser(id) {
    return get(`/api/intervals/users/${id}/`);
}

export function getUserStats(id) {
    return get(`/api/intervals/users/${id}/stats/`);
}

export function getUserSettings(id) {
    return get(`/api/intervals/users/${id}/settings/`);
}

export function updateUserSettings(id, newSettings) {
    return patch(`/api/intervals/users/${id}/settings/`, newSettings);
}