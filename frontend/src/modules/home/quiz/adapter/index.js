import { getAuthenticated, postAuthenticated } from "modules/app/xhr";

export const getQuestion = (access) => {
    return getAuthenticated("http://localhost:8000/api/intervals/question/", access)
        .then(response => response.data);
};

export const answerCheck = (question, guess, access) => {
    const data = {question: question, guess: guess};
    console.log('data', data);
    return postAuthenticated("http://localhost:8000/api/intervals/answer_check/", data, access);
};
