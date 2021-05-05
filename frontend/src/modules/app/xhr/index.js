import Axios from "axios";

export function returnAxiosInstance() {
    const instance = Axios.create();
    instance.defaults.xsrfHeaderName = "X-CSRFToken";
    instance.defaults.xsrfCookieName = "csrftoken";
    instance.defaults.withCredentials = true;
    instance.defaults.baseURL = "http://localhost";
    return instance;
}

export function get(url) {
    const axios = returnAxiosInstance();
    return axios.get(url);
}

export function post(url, requestData) {
    const axios = returnAxiosInstance();
    return axios.post(url, requestData);
}

export function patch(url, requestData) {
    const axios = returnAxiosInstance();
    return axios.patch(url, requestData);
}

export function put(url, requestData) {
    const axios = returnAxiosInstance();
    return axios.put(url, requestData);
}
//
// export function getAuthenticated(url, access) {
//     const axios = returnAxiosInstance();
//     const config = {
//         headers: {
//             Authorization: `Bearer ${access}`
//         }
//     }
//     return axios.get(url, config);
// }
//
// export function postAuthenticated(url, requestData, access) {
//     const axios = returnAxiosInstance();
//     const config = {
//         headers: {
//             Authorization: `Bearer ${access}`
//         }
//     }
//     return axios.post(url, requestData, config);
// }
