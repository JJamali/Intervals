import React, { useEffect } from "react";
import { UserContext } from "modules/app/context/UserContext.js";
import { getQuestion, newQuestion, answerCheck } from "./adapter";


export default function QuizBl() {
    const { user, refreshUserData } = React.useContext(UserContext);
    const [question, setQuestion] = React.useState({});
    const [correctAnswer, setCorrectAnswer] = React.useState(undefined);
    const [answered, setAnswered] = React.useState(false);

    // Submits answer and gets response
    const handleSubmit = e => {
        const guess = e.currentTarget.value;
        console.log(e);
        console.log("Submitting", guess);
        answerCheck(user.id, guess)
            .then(res => {
                console.log("submit response", res);
                refreshUserData();
                setCorrectAnswer(res.data.correct_answer);
                setAnswered(true);
            });
        e.preventDefault();
    };

    const getNewQuestion = () => {
        newQuestion(user.id).then(response => {
            console.log('new question', response);
            getQuestion(user.id).then(question => {
                console.log('setting question', question);
                setQuestion(question);
            });
        });
    }

    const updateQuestion = () => {
        // get the current question from backend and get a new question if needed
        getQuestion(user.id).then(question => {
            console.log(question);
            if (question.answered) {
                getNewQuestion();
            } else {
                console.log('setting question', question);
                setQuestion(question);
            }
        }).catch(error => {
            if (error.response.status === 404) {
                getNewQuestion();
            } else {
                console.log(error);
            }
        });
    };
    useEffect(() => {
        console.log("Firing");
        updateQuestion();
    }, []);

    const goNext = e => {
        console.log("next");
        setAnswered(false);
        updateQuestion();
    }

    return { question, handleSubmit, correctAnswer, answered, goNext };
}
