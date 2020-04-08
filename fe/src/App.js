import React, { Component } from 'react';
import './App.css';

class App extends Component {

    state = {
        url: "",
        urls: []
    };

    componentDidMount () {
        this.getUrls();
    }

    getUrls = () => {
        return fetch('http://0.0.0.0:8000')
            .then(response => response.json())
            .then(({urls}) => this.setState({urls}));
    };

    postUrl = () => {
        return fetch('http://0.0.0.0:8000', {
            method: 'POST',
            headers: new Headers({'Content-Type': 'application/json'}),
            body: JSON.stringify({'long_url': this.state.url})
        });
    };

    handleChange = (e) => {
        this.setState({url: e.target.value});
    };

    handleSubmit = (e) => {
        e.preventDefault();
        this.postUrl().then(() => this.getUrls());
    };

    render () {
        return (
            <div>
                {this.state.urls.map(({short_url: shortUrl, long_url: longUrl}) => {
                    return (<div key={shortUrl}>
                        <span>{shortUrl}</span> <span>{longUrl}</span>
                    </div>);
                })}
                <br />
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Add new tiny URL:
                        <input type="text" required minLength={1} value={this.state.url} onChange={this.handleChange} />
                    </label>
                    <input type="submit" value="Submit" />
                </form>
            </div>

        );
    }
}

export default App;
