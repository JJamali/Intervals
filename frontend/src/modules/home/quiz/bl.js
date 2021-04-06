import React, { useEffect } from "react";
import { UserContext } from "modules/app/context/userContext.js";
import { getQuestion, answerCheck } from "./adapter";


export default function QuizBl() {
    const { token, refreshUserData } = React.useContext(UserContext);
    const [question, setQuestion] = React.useState({});
    const [guess, setGuess] = React.useState("");

    // Submits answer and gets response
    const handleSubmit = e => {
        console.log("Submitting");
        answerCheck(question, guess, token.access)
            .then(res => {
                refreshUserData();
            });
        e.preventDefault();
    };

    const handleGuessChange = e => {
        setGuess(e.target.value);
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

    return { question, handleGuessChange, handleSubmit };
}
