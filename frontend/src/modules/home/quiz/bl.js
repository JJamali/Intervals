import React, { useEffect } from "react";
import { UserContext } from "modules/app/context/userContext.js";
import { getQuestion, answerCheck } from "./adapter";


export default function QuizBl() {
    const { token, user, refreshUserData } = React.useContext(UserContext);
    const [question, setQuestion] = React.useState({});
    const [guess, setGuess] = React.useState("");

    // Submits answer and gets response
    const handleSubmit = e => {
        const guess = e.currentTarget.value;
        console.log(e);
        console.log("Submitting", guess);
        answerCheck(question, guess, token.access)
            .then(res => {
                refreshUserData();
            });
        e.preventDefault();
    };

    const updateQuestion = () => {
        getQuestion(token.access).then(question => {
            console.log('got question', question);
            setQuestion(question);
        });
    };
    useEffect(() => {
        updateQuestion();
    }, []);

    const recentResults = user.profile.recent_results;

    return { question, recentResults, handleSubmit };
}
