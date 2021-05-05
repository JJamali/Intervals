import React, { useState, useEffect } from "react";
import { getUserId as apiGetUserId, getUser, logout } from "./adapter";
import { Redirect } from "react-router-dom";


export const UserContext = React.createContext();

const UserProvider = ({ children }) => {
    const [userId, setUserId] = useState(null);
    const [user, setUser] = useState(null);
    const [loggedIn, setLoggedIn] = useState(false);

    const getUserId = () => {
        apiGetUserId().then(response => {
            setUserId(response.data.id);
        })
        .catch(error => {
            console.log("Failed to log in", error);
            setLoggedIn(false);
        });
    };

    const refreshUserData = () => {
        getUser(userId).then(response => {
            let user = response.data;
            const recentResults = user.stats.recent.find(result => {
                return result.level === user.settings.current_level;
            });
            user.stats = {...user.stats,
                recentResults: recentResults,
                globalStats: calculateGlobalStats(user.stats.recent),
            };
            console.log('a user', user);
            setUser({...user, id: userId});
        });
    };

    const logoutUser = () => {
        logout();
        setLoggedIn(false);
    }

    // global stats are stats across all levels
    const calculateGlobalStats = (recents) => {
        let globalStats = {global_completed: 0, global_correct: 0};
        recents.forEach(r => {
            globalStats.global_completed += r.total_completed;
            globalStats.global_correct += r.total_correct;
        });
        return globalStats;
    }


    // the log in process sets the state in this order:
    // userId -> user -> loggedIn
    // the log out process sets the state in this order:
    // loggedIn -> user -> userId

    useEffect(() => {
        if (userId !== null) {
            refreshUserData();
        }
    }, [userId]);

    // log in when user object is set
    useEffect(() => {
        if (user === null) {
            setUserId(null);
        }
        if (user !== null) {
            console.log(user.profile);
            setLoggedIn(true);
        }
    }, [user]);

    // remove user when we log out
    useEffect(() => {
        if (!loggedIn) {
            setUser(null);
        }
    }, [loggedIn]);

    // try to log in on load
    useEffect(() => {
        getUserId();
    }, []);


    return (
        <>
            {loggedIn && <Redirect to="/login" />}
            <UserContext.Provider value={{ user, loggedIn, refreshUserData, getUserId, logout: logoutUser }}>
                {children}
            </UserContext.Provider>
        </>
    );
};

export default UserProvider;
