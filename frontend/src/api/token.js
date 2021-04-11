import { post } from "modules/app/xhr";

export function getToken(username, password) {
    const data = {username: username, password: password};
    return post("http://localhost:8000/api/token/", data)
        .then(res => res.data)
        .catch(error => {
            console.log("Unable to login:", error);
            return null;
        });
}


export function refreshToken(refresh) {
    return post("http://localhost:8000/api/token/refresh/", {refresh: refresh})
        .then(response => response.data)
        .catch(error => {
            console.log("Unable to refresh token:", error);
            return null;
        });
}
