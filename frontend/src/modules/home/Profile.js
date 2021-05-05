import QuizBl from "./quiz/bl.js";
import {useState, useEffect} from "react";

export default function Profile({user}) {
    const recentResults = {};

    return (
        <div>
            <h2>Home</h2>
            <h3>Hello, {user.username}</h3>
            <div>
                <div>Level: {user.stats.level}</div>
                <div>Current level: {user.stats.current_level}</div>
                <div>Total completed: {user.stats.recentResults.total_completed}</div>
                <div>Total correct: {user.stats.recentResults.total_correct}</div>
                <div>Global completed: {user.stats.globalStats.global_completed}</div>
                <div>Global correct: {user.stats.globalStats.global_correct}</div>
            </div>
        </div>
    )
}
