import { get, post } from "modules/app/xhr";

export const getQuestion = () => {
    return get("/api/intervals/question/")
        .then(response => response.data);
};

export const answerCheck = (guess) => {
    const data = {guess: guess};
    console.log('data', data);
    return post("/api/intervals/answer_check/", data);
};

export const globalStats = () => {
    return get("/api/intervals/global_stats/")
        .then(response => response.data);
}