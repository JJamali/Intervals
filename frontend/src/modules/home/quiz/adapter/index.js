import { get, postAuthenticated } from "modules/app/xhr";

export const getQuestion = () => {
    return get("http://localhost:8000/api/intervals/question/").
        then(response => response.data);
};

export const answerCheck = (question, guess, access) => {
    const data = {question: question, guess: guess}
    return postAuthenticated("http://localhost:8000/api/intervals/answer_check/", data, access);
};
