import React from 'react';

export const UserContext = React.createContext({
    user: {},
    updateUser: () => {}, // prompts app to get user data from backend
});
