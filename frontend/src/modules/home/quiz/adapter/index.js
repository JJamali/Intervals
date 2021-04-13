import { getAuthenticated, postAuthenticated } from "modules/app/xhr";

export const getQuestion = (access) => {
    return getAuthenticated("/api/intervals/question/", access)
        .then(response => response.data);
};

export const answerCheck = (guess, access) => {
    const data = {guess: guess};
    console.log('data', data);
    return postAuthenticated("/api/intervals/answer_check/", data, access);
};

export const logout = (e) => {
    e.preventDefault();
    console.log("Logged out");
    return postAuthenticated("/api/intervals/logout/");
};