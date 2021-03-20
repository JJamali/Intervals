import React, { Component } from 'react';
import Nav from './components/Nav';
import LoginForm from './components/LoginForm';
import SignupForm from './components/SignupForm';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayed_form: '',
      logged_in: false,//localStorage.getItem('token') ? true : false
      username: '',
      question:'',
      user: {profile: {}},
    };
  }

  componentDidMount() {
    if (this.state.logged_in) {
      fetch('http://localhost:8000/api/intervals/current_user/', {
        headers: {
          Authorization: `JWT ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(json => {
          this.setState({ username: json.user.username });
        });
    }
  }

  handle_login = (e, data) => {
    e.preventDefault();

    fetch('http://localhost:8000/api/token/', { // Handle login
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })

      .then(res => res.json())
      .then(json => {
        console.log(json);
        this.setState({jwt_token: json.access, jwt_token_refresh: json.refresh}); // Sets token
        this.setState({
          user: json.user,
          username: json.user.username,
          logged_in: true,
          displayed_form: '',
        });
      });
  };

  handle_signup = (e, data) => {
    e.preventDefault();
    fetch('http://localhost:8000/api/intervals/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        this.setState({jwt_token: json.token}); // Sets token
        this.setState({
          user: json.user,
          logged_in: true,
          displayed_form: '',
          username: json.username
        });
      });
  };

  handle_logout = () => {
    this.setState({ logged_in: false, username: '' });
  };

  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  get_question = (e, data) => {
    e.preventDefault();

    fetch('http://localhost:8000/api/intervals/question/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
.then(res => res.json())
      .then(json => {
        this.setState({
          displayed_form: '',
          question: json,
        });
      });
  };

  answer_check = (e, data) => {
    e.preventDefault();
    console.log(this.state.jwt_token);
    fetch('http://localhost:8000/api/intervals/answer_check/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.state.jwt_token}`
      },
      // body collects data (in the form of a dictionary) to be sent to backend
      body: JSON.stringify({question: this.state.question, guess: this.state.guess})
    })
    .then(response => response.json())
    .then(data => this.setState({ }));
  };

  handle_guess_change = (e) => {
    this.setState({guess: e.target.value})
  }


  render() {
    let form;
    switch (this.state.displayed_form) {
      case 'login':
        form = <LoginForm handle_login={this.handle_login} />;
        break;
      case 'signup':
        form = <SignupForm handle_signup={this.handle_signup} />;
        break;
      default:
        form = null;
    }

    return (
      <div className="App">
        <Nav
          logged_in={this.state.logged_in}
          display_form={this.display_form}
          handle_logout={this.handle_logout}
        />
        {form}
        <h3>
          {this.state.logged_in
            ? `Hello, ${this.state.username}`
            : 'Please Log In'}
        </h3>

        <form onSubmit={this.get_question}>
          <input type="submit" value="Get question" />
        </form>
        <div>
          Total correct: {this.state.user.profile.total_correct}

          Total answered: {this.state.user.profile.total_completed}
        </div>

        <form onSubmit={this.answer_check}>
          Question: {this.state.question.question}
          <input type="text" name="guess" onChange={this.handle_guess_change} />
          <input type="submit" value="Submit" />
        </form>
      </div>
    );
  }
}

export default App;