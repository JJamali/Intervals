import React, { useEffect } from "react";
import { UserContext } from "modules/app/context/UserContext.js";
import { getQuestion, answerCheck } from "./adapter";


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
        answerCheck(guess)
            .then(res => {
                console.log("submit response", res);
                refreshUserData();
                setCorrectAnswer(res.data.correct_answer);
                setAnswered(true);
            });
        e.preventDefault();
    };

    const updateQuestion = () => {
        getQuestion().then(question => {
            console.log('got question', question);
            setQuestion(question);
        });
    };
    useEffect(() => {
        updateQuestion();
    }, []);

    const recentResults = user.profile.recent_results;

    const goNext = e => {
        console.log("next");
        setAnswered(false);
        updateQuestion();
    }

    return { question, recentResults, handleSubmit, correctAnswer, answered, goNext };
}
