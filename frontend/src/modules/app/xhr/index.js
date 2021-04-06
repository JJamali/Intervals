import Axios from "axios";

export function returnAxiosInstance() {
    const config = {};
    return Axios.create(config);
}

export function get(url) {
    const axios = returnAxiosInstance();
    return axios.get(url);
}

export function post(url, requestData) {
    const axios = returnAxiosInstance();
    return axios.post(url, requestData);
}

export function getAuthenticated(url, access) {
    const axios = returnAxiosInstance();
    const config = {
        headers: {
            Authorization: `Bearer ${access}`
        }
    }
    return axios.get(url, config);
}

export function postAuthenticated(url, requestData, access) {
    const axios = returnAxiosInstance();
    const config = {
        headers: {
            Authorization: `Bearer ${access}`
        }
    }
    return axios.post(url, requestData, config);
}
