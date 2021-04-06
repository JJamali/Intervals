import { post } from "modules/app/xhr";

export function signup(username, password) {
    const data = {username: username, password: password};
    return post("http://localhost:8000/api/intervals/users/", data)
        .then(res => res.data.token)
        .catch(error => {
            console.log("Unable to login:", error);
            return null;
        });
}
