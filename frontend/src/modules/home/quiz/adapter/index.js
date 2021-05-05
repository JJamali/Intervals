import { get, post } from "modules/app/xhr";

export const getQuestion = (id) => {
    return get(`/api/intervals/users/${id}/question/`)
        .then(response => response.data);
};

export const newQuestion = (id) => {
    return post(`/api/intervals/users/${id}/question/`, {})
        .then(response => response.data);
}

export const answerCheck = (id, guess) => {
    const data = {guess: guess};
    console.log('data', data);
    return post(`/api/intervals/users/${id}/answer/`, data);
};
